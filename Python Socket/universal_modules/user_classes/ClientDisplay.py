"""
This is class has control over what the client sees as a reaction to messages
from the server
"""
from typing import Any


class ClientDisplay:
    """
    Contains username and password
    """

    def __init__(self, account: Any):
        self.account = account

    def notify_status_of_log_in(self, message: tuple[bool, str]) -> None:
        """
        With a given message from the server, notify the user of the status of their log in

        Possible Statuses:
        False -> invalid username, invalid password, already_logged_in
        True -> None
        """
        status = message[0]  # This is a bool stating whether or not the account actually logged in
        given_message = message[1]  # if it failed to log in, this is the error message

        if given_message == "invalid_username":
            print("Failed to log in. The username is incorrect.")
            return
        elif given_message == "invalid_password":
            print("Failed to log in. The password is incorrect.")
            return
        elif given_message == "already_logged_in":
            print("Failed to log in. Account is already logged in on another device.")
            return

        self.account.set_logged_in(True)
        print("Successfully logged in! Welcome, " + self.account.get_username())

    def notify_status_of_account_creation(self, message: tuple[bool, str]) -> None:
        """
        With a given message from the server, notify the user of the status of their log in

        Possible Statuses:
        False -> duplicate_username, password_length_invalid, username_length_invalid
        True -> None
        """
        status = message[0]  # This is a bool stating whether or not the account actually logged in
        given_message = message[1]  # if it failed to log in, this is the error message

        if given_message == "duplicate_username":
            print("Failed to create the account. Someone already has that username.")
            return
        elif given_message == "password_length_invalid":
            print("Failed to create the account. Your password must at least 3 characters long.")
            return
        elif given_message == "username_length_invalid":
            print("Failed to create the account. Your username cannot be empty.")
            return

        print("Account has been created!")
