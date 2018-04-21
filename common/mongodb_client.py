from pymongo import MongoClient

MONGO_DB_HOST = "localhost"
MONGO_DB_PORT = "27017"
DB_NAME = "tap-news"

client = MongoClient("%s:%s" % (MONGO_DB_HOST, MONGO_DB_PORT))

def get_db(db=DB_NAME):
    db = client[db]
    return db

if __name__ == '__main__':
    db = get_db('test')
    db.demo.drop()
    assert db.demo.count() == 0
    db.demo.insert({'test':123})
    assert db.demo.count() == 1
    db.demo.drop()
    assert db.demo.count() == 0
    print 'test_basic passed!'
