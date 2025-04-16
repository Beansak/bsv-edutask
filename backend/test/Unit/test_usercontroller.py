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

        with patch('src.util.dao.DAO') as mockedDAO:
            mock = MagicMock()
            mockedDAO.return_value = mock
            uc = UserController(dao=mockedDAO)
            with pytest.raises(ValueError, match="Error: invalid email address"):
                uc.get_user_by_email(email)

    def test_valid_email_adress(self):
        """Test the get_user_by_email method with a valid email address.
        """

        user = {'firstName': 'Jane', 'lastName': 'Doe', 'email': 'jane.doe'}
        email = "jane.doe@email.com"
        mockedDAO = MagicMock()
        mockedDAO.find.return_value = [user]  # Simulate the DAO's find() method
        # Mock the DAO to return a simulated user
        uc = UserController(dao=mockedDAO)
        # Mock the user object
        # Patch the fullmatch method of the regex library
        # Mock the fullmatch method to always return True
        
        assert uc.get_user_by_email(email) == user