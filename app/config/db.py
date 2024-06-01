import os
from pymongo import MongoClient, errors
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
load_dotenv()
class DB:
    """
    A class representing a MongoDB database connection.

    Attributes:
        uri (str): The connection URI for the MongoDB database.
        client (pymongo.MongoClient): The MongoDB client object.

    Methods:
        __init__(): Initializes a new instance of the DB.
        get_collection(collection_name: str): Retrieves a collection from the database.
        close_connection(): Closes the MongoDB connection.
    """

    def __init__(self):
        self.uri = os.getenv("MONGO_URL")
        if not self.uri:
            raise ValueError("No MongoDB URI found in environment variables")
        try:
            self.client = MongoClient(self.uri)
            # Verify connection
            self.client.admin.command('ping')
            self.db = self.client.chatters_db
            print("Connected to MongoDB")
        except errors.ConfigurationError as e:
            raise ConnectionError(f"Could not connect to MongoDB: {e}")

    def get_collection(self, db_name: str, collection_name: str):
        """
        Retrieves a collection from the database.

        Args:
            db_name (str): The name of the database.
            collection_name (str): The name of the collection.

        Returns:
            pymongo.collection.Collection: The MongoDB collection object.
        """
        return self.client[db_name][collection_name]

    def close_connection(self):
        """
        Closes the MongoDB connection.
        """
        self.client.close()
        print("MongoDB connection closed")
