
from typing import Union, Optional, Dict, Any
import pymongo
import bson

from asch.config import Config

class ResultLog():

    _db = pymongo.MongoClient(Config.get_or_else('database', 'CONNECTION_STRING', None)).asch

    def __init__(self,
                 _id = None,
                 task = None,
                 participant = None,
                 data = None):
        self._id = _id
        self.task = task
        self.participant = participant
        self.data = data or {}

    def todict(self, json_safe: bool = False) -> Dict[str, Any]:
        output = {
            'task': self.task,
            'participant': self.participant if not json_safe else str(self.participant),
            'data': self.data,
        }
        if self._id:
            output.update({'_id': self._id if not json_safe else str(self._id)})
        print(output)
        return output

    @classmethod
    def fromdict(cls, input_dict):
        return cls(**input_dict)

    @classmethod
    def new(cls, log: Optional['ResultLog'] = None) -> 'ResultLog':
        new_log = log or ResultLog()
        inserted_doc = cls._db.result_logs.insert_one(new_log.todict())
        new_log._id = inserted_doc.inserted_id
        return new_log

    @classmethod
    def remove(cls, log_id: bson.ObjectId) -> None:
        # Remove a Log
        cls._db.result_logs.remove({'_id': log_id})

    @classmethod
    def get(cls, log_id: Union[str, bson.ObjectId]) -> 'ResultLog':

        if isinstance(log_id, str):
            log_id = bson.ObjectId(log_id)

        Log = cls._db.result_logs.find_one({'_id': log_id})
        if Log is None:
            return None
        return ResultLog.fromdict(Log)
