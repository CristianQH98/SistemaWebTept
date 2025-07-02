from pymongo import MongoClient

mongo_uri = "mongodb://localhost:27017/"
client = MongoClient(mongo_uri)
db = client['SistemaTEPT']
reportes_collection = db['reportes_tept']
