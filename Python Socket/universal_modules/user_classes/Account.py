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

    def to_msg(self) -> dict[str, str]:
        """
        Gives a dictionary representation of this class
        """
        return {"username": self._username, "password": self._password}

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