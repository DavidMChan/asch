import copy
import random
import string

from datetime import datetime,tzinfo,timedelta
from collections import OrderedDict
from typing import Any, Dict, List, Optional, Union

import bson
import pymongo

from asch.config import Config
from asch.server.logs import ResultLog


def random_string(length: int) -> str:
    return ''.join(random.sample(string.ascii_uppercase, length))

class Zone(tzinfo):
    def __init__(self,offset,isdst,name):
        self.offset = offset
        self.isdst = isdst
        self.name = name

    def utcoffset(self, dt):
        return timedelta(hours=self.offset) + self.dst(dt)

    def dst(self, dt):
        return timedelta(hours=1) if self.isdst else timedelta(0)

    def tzname(self,dt):
        return self.name

PT = Zone(-7,False,'PT')

class Participant():

    _db = pymongo.MongoClient(Config.get_or_else('database', 'CONNECTION_STRING', None)).asch

    def __init__(
        self,
        _id=None,
        name=None,
        experiment=None,
        condition=None,
        mturk_data=None,
        tasks=None,
        _last_seen=None,
    ):

        # Base information
        self._id = _id
        self.name = name or '_PLACEHOLDER_NAME'
        self._experiment = experiment or '_PLACEHOLDER_EXPERIMENT'
        self.condition = condition or '_PLACEHOLDER_CONDITION'
        self._last_seen = _last_seen or 'Never'

        # Initialize results data
        if isinstance(tasks, list):
            self.tasks = OrderedDict()
            for i, t in enumerate(tasks):
                if isinstance(t, (list, tuple)):
                    self.tasks[t[0]] = t[1]
                else:
                    self.tasks[str(i)] = t  # For people who are lazy and just give a list of tasks
        elif isinstance(tasks, OrderedDict):
            self.tasks = OrderedDict()
            for k, v in tasks.items():
                self.tasks[k] = v

        # Setup information on mechanical turk
        if mturk_data is None:
            self.mturk_data = {
                'completion_code': random_string(6),
            }
        else:
            if 'completion_code' not in mturk_data:
                raise AssertionError('Completion code must be specified if initializing mturk data.')
            self.mturk_data = mturk_data

    def get_id(self,):
        if self._id is None:
            raise AssertionError('Cannot perform ID ops on a participant that has not been committed')
        return self._id

    @property
    def experiment(self,):
        # Convenience function for getting the experiment
        from asch.server.experiments import EXPERIMENT_TYPES
        if self._experiment in EXPERIMENT_TYPES:
            return EXPERIMENT_TYPES[self._experiment]
        return None

    @property
    def finished(self,) -> bool:
        return all(v.get('_finished', False) for v in self.tasks.values())

    # Serialization
    def todict(self, json_safe=False):

        if json_safe:
            tasks = {}
            for k, v in self.tasks.items():
                vv = copy.copy(v)
                if '_result' in vv:
                    vv['_result'] = str(vv['_result'])
                tasks[k] = vv
        else:
            tasks = [(k, v) for k, v in self.tasks.items()]  # Preserve the ordered dictionary component

        output = {
            'name': self.name,
            'experiment': self._experiment,
            'condition': self.condition,
            'mturk_data': self.mturk_data,
            'tasks': tasks,
            '_last_seen': self._last_seen,
        }
        if self._id is not None:
            output.update({'_id': self._id if not json_safe else str(self._id)})
        return output

    # Ops for finishing, and managing next tasks
    def next_task(self,) -> Dict[str, Any]:
        unfinished_tasks = [(k, v) for (k, v) in self.tasks.items() if not v.get('_finished', False)]
        if not unfinished_tasks:
            return {'_finished': True, '_remaining': 0}
        next_task_id, next_task = unfinished_tasks[0]
        next_task.update({'_id': next_task_id, '_finished': False, '_remaining': len(unfinished_tasks)})
        return next_task

    def finish_task(self, task_id: str, data: Dict[str, Any] = None) -> bool:
        if task_id in self.tasks:
            data = self.experiment.on_finished(data)  # Hook for post-processing data
            # Upload the data to the server
            log_elem = ResultLog.new(log=ResultLog(participant=self.get_id(), task=task_id, data=data))
            self.tasks[task_id]['_result'] = log_elem._id
            self.tasks[task_id]['_finished'] = True

            # Commit the new participant data
            Participant.update(self)  # Kinda weird to do it like this, but there's not much that's better
            return True
        return False

    def populate_task_data(self,) -> None:
        # TODO: This is pretty bad - since it's a method which has side effects. We should keep this pure, but #effort
        for k, v in self.tasks.items():
            if '_result' in v and v['_result'] is not None:
                self.tasks[k]['_data'] = ResultLog.get(v['_result']).todict(json_safe=True)

    @classmethod
    def fromdict(cls, input_dict):
        return Participant(**input_dict)

    @classmethod
    def new(cls, participant: Optional['Participant'] = None) -> 'Participant':
        new_participant = participant or Participant()
        participant._last_seen = datetime.now(PT).isoformat()
        inserted_doc = cls._db.participants.insert_one(new_participant.todict())
        new_participant._id = inserted_doc.inserted_id
        return new_participant

    @classmethod
    def update(cls, participant: 'Participant') -> 'Participant':
        participant._last_seen = datetime.now(PT).isoformat()
        cls._db.participants.replace_one({'_id': participant._id}, participant.todict())
        return True

    @classmethod
    def remove(cls, participant_id: bson.ObjectId) -> None:
        # Remove a participant
        cls._db.participants.delete_one({'_id': bson.ObjectId(participant_id)})

    @classmethod
    def get(cls, participant_id: Union[str, bson.ObjectId]) -> 'Participant':

        if isinstance(participant_id, str):
            participant_id = bson.ObjectId(participant_id)

        participant = cls._db.participants.find_one({'_id': participant_id})
        if participant is None:
            return None
        return Participant.fromdict(participant)

    @classmethod
    def fetch_all(cls, filter={}) -> List['Participant']:
        return [Participant.fromdict(p) for p in cls._db.participants.find(filter)]
