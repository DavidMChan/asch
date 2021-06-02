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


class DownloadParticipantDataAPIRecource(Resource):

    @protected
    def get(self, user):
        if 'experiment' in request.args:
            finished_participants = list(filter(lambda x: x.finished, Participant.fetch_all(filter={'experiment': request.args['experiment']})))
        else:
            finished_participants = list(filter(lambda x: x.finished, Participant.fetch_all()))
        for f in finished_participants:
            f.populate_task_data()

        # Serve a JSON file with the data
        return Response(json.dumps([Participant.todict(f, json_safe=True) for f in finished_participants]),
                        mimetype='application/octet-stream; charset=UTF-8',
                        headers={'Content-Disposition': "attachment; filename=participant_data.json"})
