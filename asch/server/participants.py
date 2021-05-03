
import pymongo

from asch.config import Config


class Participant():

    def __init__(self,):
        pass

    def todict(self,):
        



class ParticipantRegistry():

    def __init__(self,):
        # Connect to the database, and figure out the details
        self._db = pymongo.MongoClient(Config.get_or_else('database', 'connection_string', None)).asch

    def new(self):
        # Get a new particpant ID by reserving the document
        inserted_doc = self._db.participants.insert_one({})
        return inserted_doc.inserted_id


PARTICIPANT_REGISTRY = ParticipantRegistry()
