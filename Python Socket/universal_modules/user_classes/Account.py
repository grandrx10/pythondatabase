"""
This is an account
"""


class Account:
    """
    Contains username and password
    """

    def __init__(self):
        self._username = None
        self._password = None
        self._logged_in = False

    def create_new_account(self):
        """
        Create a new username and password
        """
        print("Username: ")
        self._username = input()
        print("Password: ")
        self._password = input()

    def log_in(self):
        """
        Enter a username and password to log into the account
        """
        print("Username: ")
        self._username = input()
        print("Password: ")
        self._password = input()

    def set_logged_in(self, status: bool) -> None:
        """
        Set logged in status
        """
        self._logged_in = status

    def get_logged_in(self) -> bool:
        """
        :return: whether the account is logged in or not
        """
        return self._logged_in

    def get_username(self) -> str:
        """
        :return: a string containing the username of the account
        """
        return self._username

    def get_password(self) -> str:
        """
        :return: a string containing the password of the account
        """
        return self._password
