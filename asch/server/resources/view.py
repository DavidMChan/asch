import json

import bson
import pymongo
from flask import Response, request
from flask_restful import Resource

from asch.server.auth import protected
from asch.server.participants import Participant


class ParticipantViewAPIResource(Resource):

    @protected
    def get(self, user):
        if 'experiment' in request.args:
            return [f.todict(json_safe=True) for f in filter(lambda x: x.finished, Participant.fetch_all(filter={'experiment': request.args['experiment']}))]
        # Return a list of all participants, their conditions, and their completion codes.
        return [f.todict(json_safe=True) for f in filter(lambda x: x.finished, Participant.fetch_all())]

    @protected
    def delete(self, user):
        if 'id' in request.args:
            Participant.remove(request.args['id'])
            return Response(status=200)
        return Response(status=400)


class DownloadParticipantDataAPIResource(Resource):

    @protected
    def get(self, user):
        if 'experiment' in request.args:
            finished_participants = list(filter(lambda x: x.finished, Participant.fetch_all(filter={'experiment': request.args['experiment']})))
        else:
            finished_participants = list(filter(lambda x: x.finished, Participant.fetch_all()))
        if 'id' in request.args:
            finished_participants = list(filter(lambda x: str(x._id) == str(request.args['id']), finished_participants))

        for f in finished_participants:
            f.populate_task_data()

        # Serve a JSON file with the data
        return Response(json.dumps([Participant.todict(f, json_safe=True) for f in finished_participants]),
                        mimetype='application/octet-stream; charset=UTF-8',
                        headers={'Content-Disposition': "attachment; filename=participant_data.json"})

class ParticipantFinishedAPIResource(Resource):

    def get(self,):
        if 'pid' in request.args:

            participant = Participant.get(request.args['pid'])
            if participant is None:
                return {'error': 'Participant not found'}, 404
            return {'finished': participant.finished}, 200
