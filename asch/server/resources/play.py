import bson
import pymongo
from flask import request
from flask_restful import Resource

from asch.server.experiments import EXPERIMENT_TYPES
from asch.server.participants import Participant


class PlayAPIResource(Resource):

    def get(self,):
        participant = None
        if 'pid' in request.args:
            # Fetch the participant based on the PID
            participant = Participant.get(request.args['pid'])
            if participant is None:
                return {'error': 'Could not create or find participant.'}, 404
        elif 'experiment' in request.args:
            if request.args['experiment'] not in EXPERIMENT_TYPES:
                return {'error': 'Unknown Experiment'}, 404
            exp = EXPERIMENT_TYPES[request.args['experiment']]
            if 'condition' in request.args:
                if request.args['condition'] in exp.conditions():
                    participant = exp.new_participant(condition=request.args['condition'])
                else:
                    return {'error': 'Unknown condition, but condition specified'}, 400
            else:
                participant = exp.new_participant()
        else:
            return {'error': 'Could not create or find participant.'}, 404

        if participant.experiment is None:
            return {'error': 'Participant is created, but has no experiment'}, 400

        # Now that the participant is created or fetched, we just need to return the info
        return {
            'experiment': {
                'build_path': participant.experiment.build_path(),
                'name': participant.experiment.name(),
            },
            'id': str(participant.get_id()),
            'mturk_data': participant.mturk_data,
            '_finished': participant.finished,
        }


class UnityTaskAPIResource(Resource):

    def get(self,):
        if 'pid' not in request.args:
            return {'error': 'Could not create or find participant.'}, 404
        participant = Participant.get(request.args['pid'])
        if participant is None:
            return {'error': 'Could not create or find participant.'}, 404
        return participant.next_task()

    def post(self,):
        if 'pid' not in request.args:
            return {'error': 'Could not create or find participant.'}, 404
        if 'tid' not in request.args:
            return {'error': 'Could not find task'}, 404
        participant = Participant.get(request.args['pid'])
        if participant is None:
            return {'error': 'Could not create or find participant.'}, 404

        if participant.finish_task(task_id=request.args['tid'], data=request.get_json()):
            return participant.next_task()
        return {'error': 'Failed to complete task'}, 400
