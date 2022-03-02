from pymongo import MongoClient
from bson.objectid import ObjectId


class MongoDB:
    def __init__(self, uri) -> None:
        self.client = MongoClient(uri)
        self.db = self.client.test["memo"]

    def insert_one(self, doc: dict) -> None:
        self.db.insert_one(doc)

    def find_many(self, setting: dict = None) -> list:
        setting = {'_id': True} if setting else {}
        rows = list(self.db.find({}, setting))

        for row in rows:
            if '_id' in row.keys():
                row['_id'] = str(row['_id'])

        return rows

    def delete_one(self, _id: str) -> None:
        _id = ObjectId(_id)
        self.db.delete_one({'_id': _id})
