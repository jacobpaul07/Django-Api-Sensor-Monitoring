import os
import pymongo
client = None
db = None


class Databaseconfig:
    """Used for managing interactions between worker process and mongo database"""

    @staticmethod
    def connect():
        """Connects to database"""
        global client, db

        try:
            connectionString: str = os.environ["MONGO_CONNECTION_STRING"]
            client = pymongo.MongoClient(connectionString)
            client.admin.command('isMaster')

        except Exception as inst:
            print('Exception occurred while connecting to database', inst)
            if client is None:
                raise Exception('Mongo db not connected')
            db = client['admin']
