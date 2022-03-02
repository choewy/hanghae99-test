from pymongo import MongoClient
from bson.objectid import ObjectId


# mongodb://root:password@localhost:7000/admin

class MongoDB:
    def __init__(self, db="dbsparta") -> None:
        self.client = MongoClient(
            "mongodb://root:password@172.0.0.2:27017/admin")
        self.db = self.client[db]["memo"]

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
