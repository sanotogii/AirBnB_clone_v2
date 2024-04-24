import os
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from dotenv import load_dotenv

load_dotenv()

storage_type = os.environ['HBNB_TYPE_STORAGE']
# Check if the database connection parameters are available
if storage_type == 'db':
    # Initialize database storage
    storage = DBStorage()
    # Try to connect to the database
    try:
        storage.reload()
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        # If connection fails, fall back to file storage
        storage = FileStorage()
else:
    # If database connection parameters are not available, use file storage
    storage = FileStorage()

# Update the storage singleton instance
storage.reload()
