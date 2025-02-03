import pymongo

url='mongodb+srv://priyanshu23:s52q1IZArxh0pq6Z@cluster0.o8h17.mongodb.net/'
client=pymongo.MongoClient(url)

db=client['FakeNews']