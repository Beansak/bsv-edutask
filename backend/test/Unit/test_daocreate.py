import pytest
from unittest.mock import patch, MagicMock
from src.util.dao import DAO

# JSON validator based on the todo schema
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
def mocked_dao():
    """Fixture to mock the DAO class and its __init__ method."""
    with patch.object(DAO, '__init__', return_value=None) as mocked_init:
        # Create a DAO instance (this will not call the real __init__)
        dao = DAO(collection_name="test_collection")

        # Mock the collection attribute
        dao.collection = MagicMock()

        yield dao

        # Verify that the mocked __init__ was called
        mocked_init.assert_called_once_with(collection_name="test_collection")

class TestDAOCreate:

    @pytest.mark.unit
    def test_valid_input(self, mocked_dao):
        """Test the create method with valid input."""
        # Mock the input data
        data = {
            "title": "Test Todo",
            "description": "This is a test todo",
            "done": False
        }

        # Mock the insert_one method
        mocked_dao.collection.insert_one.return_value.inserted_id = "mocked_id"

        mocked_dao.collection.find_one.return_value = {
            "_id": "mocked_id",
            "title": "Test Todo",
            "description": "This is a test todo",
            "done": False
        }

        # Call the real create method
        result = DAO.create(mocked_dao, data)

        print(f"Result of create method: {result}")

        # Verify that the create method interacts with the database
        mocked_dao.collection.insert_one.assert_called_once_with(data)

        # Check if the result is as expected
        assert result is not None
        assert result["_id"] == "mocked_id"
        assert result["title"] == data["title"]
        assert result["description"] == data["description"]
        assert result["done"] == data["done"]