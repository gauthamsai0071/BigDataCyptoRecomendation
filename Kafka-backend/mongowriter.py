from pymongo import MongoClient
import sys
import kafkareader


def init(database, collection):

    try:
        client = MongoClient("mongodb+srv://bigdata:BigDataGroup4@big-data-project.ekwaj.mongodb.net/?retryWrites=true&w=majority")
        print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB")

    # connecting or switching to the database
    db = client.database

    # creating or switching to demoCollection
    collection = db.collection
    client.close()

def write_messages(dbs, collection, group):
    try:
        client = MongoClient("mongodb+srv://bigdata:BigDataGroup4@big-data-project.ekwaj.mongodb.net/?retryWrites=true&w=majority")
        print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB")

    try:
    # connecting or switching to the database
        db = client[dbs]

        # creating or switching to demoCollection
        cllctn = db[collection]
        messages = kafkareader.read_kafka(collection, group)
        if messages:
            cllctn.insert_many(messages)
        else:
            print("Nothing to write to Mongo")
    finally:
        client.close()

def write_messages_trade(dbs, collection, group):
    try:
        client = MongoClient("mongodb+srv://bigdata:BigDataGroup4@big-data-project.ekwaj.mongodb.net/?retryWrites=true&w=majority")
        print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB")

    try:
    # connecting or switching to the database
        db = client[dbs]

        # creating or switching to demoCollection
        cllctn = db[collection]
        messages = kafkareader.read_kafka_trade(collection, group)
        if messages:
            cllctn.insert_many(messages)
        else:
            print("Nothing to write to Mongo")
    finally:
        client.close()



if __name__ == "__main__":
    database = sys.argv[1]
    collection = sys.argv[2]
    group = sys.argv[3]
    trade = sys.argv[4]
    print("database: " + database)
    print("collection: " + collection)
    print("group: " + group)
    print("trade: "+ trade)
    init(database, collection)
    if(trade == "trade"):
        write_messages_trade(database, collection, group)
    else:
        write_messages(database, collection, group)
    