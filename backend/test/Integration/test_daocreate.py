#Run with docker
#Start docker with docker-compose up
#In a new terminal run "docker exec -it edutask-backend bash"
#Run the tests with "pytest -s -m (your mark)" its unit for me
#Every time you change the code, you have to go to the docker desktop and delete the backend container in the container tab
#Then go to the images tab and delete the backend image
#Docker backend remembers the last image and container, so you have to delete them to run the new code
#After every change, you have to run docker-compose up again

import pytest
from unittest.mock import patch, MagicMock
from src.util.dao import DAO
from pymongo import MongoClient
from pymongo.errors import WriteError
from pymongo.errors import DuplicateKeyError

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



class TestDAOCreate:

    @pytest.fixture
    def mocked_dao(self):
        """Fixture to mock the DAO class and its __init__ method."""
            # Create a DAO instance (this will not call the real __init__)
        with patch("src.util.dao.getValidator", autospec=True) as mockedgetvalidator:
            mockedgetvalidator.return_value = json_validator

            client = MongoClient("mongodb://root:root@edutask-mongodb:27017")
        # Mock the collection attribute
            
            dao = DAO(collection_name="test")

        # Mock the MongoDB collection
            dao.collection.delete_many({})

        # ⚡ CREATE UNIQUE INDEX ON 'title' FIELD
        dao.collection.create_index("title", unique=True)

        yield dao

        # Cleanup after the test
        dao.collection.delete_many({})
        # Close the client connection
        client.close()


    @pytest.mark.unit
    def test_valid_input(self, mocked_dao):
        """Test the create method with valid input."""
        # Mock the input data
        data = {
            "title": "Test Todo",
            "description": "This is a test todo",
            "done": False
        }

        # Call the real create method
        result = mocked_dao.create(data)

        # Verify that the create method interacts with the database

        # Check if the result is as expected
        assert result is not None
        assert result["title"] == data["title"]
        assert result["description"] == data["description"]
        assert result["done"] == data["done"]

    @pytest.mark.unit
    def test_wrong_field_type(self, mocked_dao):
        """Test the create method with invalid input."""
        # Mock the input data
        data = {
            "title": False, # Invalid type for title
            "description": "This is a test todo",
            "done": False,
        }
        
        # Call the create method and expect an exception


        # Verify that the exception is raised
        with pytest.raises(WriteError):
            mocked_dao.create(data)

    @pytest.mark.unit
    def test_missing_required_field(self, mocked_dao):
        """Test the create method with invalid input."""
        # Mock the input data
        data = {
            "description": "This is a test todo",
            "done": False,
        }
        
        # Call the create method and expect an exception


        # Verify that the exception is raised
        with pytest.raises(WriteError):
            mocked_dao.create(data)

    @pytest.mark.unit
    def test_value_out_of_range(self, mocked_dao):
        """Test the create method with invalid input."""
        # Mock the input data
        data = {
            "title": "Test Todo",
            "description": "This is a test todo",
            "done": False,
            "extra_field": 12345678901234567890  # Out of range value
        }
        
        # Call the create method and expect an exception


        # Verify that the exception is raised
        with pytest.raises(OverflowError):
            mocked_dao.create(data)

    @pytest.mark.unit
    def test_extra_field(self, mocked_dao):
        """Test the create method with valid fields plus an extra field."""
        data = {
            "title": "Test Todo",
            "description": "This is a test todo",
            "done": False,
            "extra_field": "extra value" 
        }

        result = mocked_dao.create(data)

        # Check the inserted document contains the extra field
        assert result["extra_field"] == "extra value"

    @pytest.mark.unit
    def test_duplicated_value(self, mocked_dao):
        """Test that inserting a document with a duplicated value raises a DuplicateKeyError."""
        data = {
            "title": "Unique Title",
            "description": "This is a test todo",
            "done": False
        }

        # Insert the first document
        with patch('re.fullmatch') as mockfullmatch:
            mockfullmatch.return_value = True
            result1 = mocked_dao.create(data)
        
        assert result1["title"] == data["title"]

        # Try inserting the same document again
        with pytest.raises(DuplicateKeyError):
            mocked_dao.create(data)

