import pymongo

url='YOUR_MONGODB_URL'
client=pymongo.MongoClient(url)

db=client['FakeNews']
