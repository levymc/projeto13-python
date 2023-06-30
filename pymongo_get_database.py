from pymongo import MongoClient

def get_database():
    # Fornecer a URL do MongoDB Atlas para conectar o Python ao MongoDB usando o PyMongo
    CONNECTION_STRING = "mongodb://localhost:27017/test"

    # Criar uma conexão usando o MongoClient
    client = MongoClient(CONNECTION_STRING)

    return client

if __name__ == "__main__":
    db = get_database()
