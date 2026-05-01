from pymongo import MongoClient
import sys

def test_connection():
    try:
        # Attempt to connect to local MongoDB
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
        
        # Trigger a server check
        client.server_info()
        
        print("SUCCESS: Your project is successfully connected to MongoDB Localhost!")
        print("Database: blood_donation_db")
        print(f"Collections detected: {client.blood_donation_db.list_collection_names()}")
        
    except Exception as e:
        print("ERROR: Could not connect to MongoDB.")
        print(f"Reason: {e}")
        print("\nMake sure MongoDB Service is running on your computer.")

if __name__ == "__main__":
    test_connection()
