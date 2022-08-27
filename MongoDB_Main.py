import datetime
import pymongo
from config.databaseconfig import Databaseconfig
import config.databaseconfig as dbc


class Document:

    def __init__(self):
        connection = Databaseconfig()
        connection.connect()
        self.db = dbc.client["IoT_Sensing"]

    def DB_Write(self, data, col):
        parameter = data
        collection = self.db[col]
        collection.insert_one(parameter)

    def DB_Read(self, col):
        collection = self.db[col]
        v = collection.find()
        list = []
        for i in v:
            value = i
            list.append(value)
        print(list)
        return list

    def Read_Document(self, col, DeviceID, filterField):
        collection = self.db[col]
        x = list(collection.find().sort(filterField, -1).limit(1))
        return x[0]

    def Write_Document(self, col, DeviceID, data):
        collection = self.db[col]
        myquery = {'DeviceID': DeviceID}
        x = collection.replace_one(myquery, data)
        updatedCount = x.matched_count
        print("documents updated in MongoDB.")
        # print(updatedCount, "documents updated.")
        return updatedCount

    def SpecificDate_Document(self, Timestamp: str, filterField: str, col):
        collection = self.db[col]
        date_time = datetime.datetime.strptime(
            Timestamp, "%Y-%m-%dT%H:%M:%S%z")
        from_date = datetime.datetime(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute,
                                      0, 000000)
        to_date = datetime.datetime(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute,
                                    0, 000000) + datetime.timedelta(minutes=10)
        criteria = {
            "$and": [{filterField: {"$gte": from_date, "$lte": to_date}}]}
        # criteria = {"$and": [{filterField: {"$gte": from_date, "$lte": to_date}}, {"machineID": machineID}]}
        objects_found = list(collection.find(
            criteria, {"_id": 0}).sort(filterField, pymongo.ASCENDING))
        series = []
        if len(objects_found) > 0:
            series.append(objects_found[0])
        return series

    def read_report(self, col):
        collection = self.db[col]
        data = collection.aggregate([
            {
                '$addFields': {
                    'convertedDate': {
                        '$toDate': '$last_updated_timestamp'
                    }
                }
            }, {
                '$project': {
                    'date': {
                        '$dateToString': {
                            'format': '%Y-%m-%d',
                            'date': '$convertedDate'
                        }
                    },
                    'sensor_data': '$sensor_data'
                }
            }, {
                '$addFields': {
                    'check': {
                        '$and': [
                            {
                                '$lte': [
                                    '2022-07-20', '$date'
                                ]
                            }, {
                                '$gte': [
                                    '2022-08-26', '$date'
                                ]
                            }
                        ]
                    }
                }
            }, {
                '$match': {
                    'check': True
                }
            }, {
                '$group': {
                    '_id': {
                        'date': '$date'
                    },
                    'data': {
                        '$first': '$sensor_data'
                    }
                }
            }, {
                '$addFields': {
                    'date': '$_id.date',
                    'sensor_data': '$data'
                }
            }, {
                '$project': {
                    '_id': 0,
                    'data': 0
                }
            }, {
                '$sort': {
                    'date': -1
                }
            }
        ])
        return list(data)
