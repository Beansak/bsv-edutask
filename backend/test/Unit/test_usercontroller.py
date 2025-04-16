import pytest
import warnings
from unittest.mock import patch, MagicMock
from src.controllers.usercontroller import UserController


class TestUserController:
    @pytest.mark.unit

    def test_invalid_email_adress(self):
        """Test the get_user_by_email method with an invalid email address.
        """

    #Mock the email object
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

    def test_valid_email_multiple_users(self, capsys):
        user1 = {'firstName': 'Jane', 'lastName': 'Doe', 'email': 'jane.doe@gmail.com'}
        user2 = {'firstName': 'John', 'lastName': 'Doe', 'email': 'jane.doe@gmail.com'}
        email = "jane.doe@gmail.com"
        mockedDAO = MagicMock()

        mockedDAO.find.return_value = [user1, user2] 

        uc = UserController(dao=mockedDAO)

        assert uc.get_user_by_email(email) == user1

        captured = capsys.readouterr()
        warnings.warn(captured.out.strip(), UserWarning)