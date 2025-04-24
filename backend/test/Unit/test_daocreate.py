import pytest
from unittest.mock import patch, MagicMock
from src.util.dao import DAO


#json validator based on todo schema
json_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["title", "description"],
        "properties": {
            "title": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
        "done": {
            "bsonType": "bool",
            "description": "must be a boolean and is required"
        }
        }
    }
}

@pytest.fixture
def sut():
    """Fixture to create a real DAO object with mocked dependencies."""
    with patch('src.util.dao.getValidator', autospec=True) as mocked_get_validator, \
         patch('pymongo.MongoClient', autospec=True) as mocked_mongo_client:
        
        # Mock the JSON validator
        mocked_get_validator.return_value = json_validator
        
        # Mock the MongoDB database and collection
        mocked_collection = MagicMock()
        mocked_collection.insert_one.return_value = MagicMock(inserted_id="mocked_id")  # Simulate insert_one behavior
        mocked_database = MagicMock()
        mocked_database.__getitem__.return_value = mocked_collection  # Simulate collection access
        mocked_mongo_client.return_value.edutask = mocked_database  # Simulate the 'edutask' database
        
        # Create the DAO instance
        dao = DAO(collection_name="test_collection")
        dao.collection = mocked_collection  # Inject the mocked collection
        
        yield dao



def test_valid_input(self, sut):
    """Test the create method with valid input."""
    # Mock the input data
    data = {
        "title": "Test Todo",
        "description": "This is a test todo",
        "done": False
    }

    # Call the create method
    result = DAO.create(data)

    # Verify that the create method interacts with the database

    # Check if the result is as expected
    assert result == data