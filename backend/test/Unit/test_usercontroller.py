import pytest
from unittest.mock import patch, MagicMock
from src.controllers.usercontroller import UserController


class TestUserController:
    @pytest.mark.usercontroller
    def test_invalid_email_adress(self):
        """Test the get_user_by_email method with an invalid email address.
        """
        
        # Mock the email object
        email = 'jane.doe'
        # Mock the DAO to return a simulated user
        mockedDAO = MagicMock()
        
        uc = UserController(dao=mockedDAO)
        with pytest.raises(ValueError, match="Error: invalid email address"):
            uc.get_user_by_email(email)

    def test_valid_email_adress(self):
        """Test the get_user_by_email method with a valid email address.
        """

        user = {'firstName': 'Jane', 'lastName': 'Doe', 'email': 'jane.doe@gmail.com'}
        email = "jane.doe@gmail.com"
        mockedDAO = MagicMock()
        mockedDAO.find.return_value = [{'firstName': 'Jane', 'lastName': 'Doe', 'email': 'jane.doe@gmail.com'}]  # Simulate the DAO's find() method
        # Mock the DAO to return a simulated user
        uc = UserController(dao=mockedDAO)
        # Mock the user object
        
        with patch('re.fullmatch') as mockfullmatch:
            mockfullmatch.return_value = True
            assert uc.get_user_by_email(email) == user