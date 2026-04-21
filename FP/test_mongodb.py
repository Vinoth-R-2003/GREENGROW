"""
Test MongoDB Atlas Connection
"""
import sys
from decouple import config

def run_test():
    print("="*60)
    print("Testing MongoDB Atlas Connection")
    print("="*60)

    # Try to load environment variables
    try:
        MONGODB_URI = config('MONGODB_URI')
        print("[OK] Successfully loaded MongoDB URI from .env file")
    except Exception as e:
        print(f"[ERROR] Error loading .env file: {e}")
        sys.exit(1)

    # Test pymongo connection
    print("\n1. Testing pymongo connection...")
    try:
        from pymongo import MongoClient
        from pymongo.server_api import ServerApi
        
        # Create a new client and connect to the server
        client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
        
        # Send a ping to confirm a successful connection
        client.admin.command('ping')
        print("[OK] Successfully connected to MongoDB Atlas!")
        
        # Get database info
        db_name = config('MONGODB_DB_NAME', default='farmers_platform')
        db = client[db_name]
        
        print(f"\n2. Database Information:")
        print(f"   Database Name: {db_name}")
        
        # List collections
        collections = db.list_collection_names()
        print(f"   Collections: {len(collections)}")
        if collections:
            for col in collections:
                print(f"     - {col}")
        else:
            print("     (No collections yet - database is empty)")
        
        # Test write operation
        print(f"\n3. Testing write operation...")
        test_collection = db['test_connection']
        result = test_collection.insert_one({"test": "connection", "status": "success"})
        print(f"[OK] Successfully inserted test document (ID: {result.inserted_id})")
        
        # Test read operation
        print(f"\n4. Testing read operation...")
        doc = test_collection.find_one({"test": "connection"})
        print(f"[OK] Successfully read test document: {doc}")
        
        # Clean up test document
        test_collection.delete_one({"test": "connection"})
        print(f"[OK] Cleaned up test document")
        
        client.close()
        
        print("\n" + "="*60)
        print("SUCCESS: MongoDB Atlas is working correctly!")
        print("="*60)
        print("\nNext steps:")
        print("1. Install djongo: pip install djongo==1.3.6")
        print("2. Update Django settings to use MongoDB")
        print("3. Run migrations")
        
    except ImportError:
        print("[ERROR] pymongo is not installed")
        print("\nPlease install required packages:")
        print("  pip install pymongo dnspython python-decouple")
        sys.exit(1)
        
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
        print("\nPossible issues:")
        print("- Check your MongoDB URI in .env file")
        print("- Verify network connectivity")
        print("- Ensure MongoDB Atlas cluster is running")
        print("- Check firewall/IP whitelist settings")
        sys.exit(1)

if __name__ == '__main__':
    run_test()
