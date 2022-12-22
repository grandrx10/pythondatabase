"""
This is the client for the python socket
"""
import socket
import pickle  # Use this to send objects and such
from typing import Any

# import classes the client needs
from universal_modules.user_classes.Account import Account
from universal_modules.user_classes.ClientDisplay import ClientDisplay


HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

SERVER = "192.168.0.31"  # socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (SERVER, PORT)

client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
client.connect(ADDR)


def send(function_to_run: str, parameter: Any) -> None:
    """
    Encode and send a message to the server.
    """
    msg = {"function_to_run": function_to_run, "parameter": parameter}
    message = pickle.dumps(msg)  # Encode the message first
    msg_length = len(message)  # The first message sent must be the length of the message
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))  # b' ' is byte representation of blank (This is for padding)
    client.send(send_length)
    client.send(message)

    # Recieve a message from the server here
    # First recieve the length of the next message
    msg_length = client.recv(HEADER).decode(FORMAT)
    # Next recieve the actual message itself to the exact length
    if len(msg_length) > 0:
        msg_length = int(msg_length)
        # find the length of the next message
        msg = pickle.loads(client.recv(msg_length))
        str_to_function[msg["function_to_run"]](msg["parameter"])
    # This is a blocking piece of code (Maybe run an update once every few milliseconds?)


def start() -> None:
    """
    The main loop of the client
    """
    # This loop will run until the user is logged in.
    while not account.get_logged_in():
        print("Create a new account or log in?")
        user_input = input()

        if user_input == "create":
            account.create_new_account()
            send("create_account", account)
        elif user_input == "log in":
            account.log_in()
            send("log_in", account)

    send(DISCONNECT_MESSAGE, account)  # Disconnect when finished


# create the account the client is using
account = Account()
# create the client display, which will control what the client can see
client_display = ClientDisplay(account)

# This dictionary is a mapping of strings to their function counterparts
str_to_function = {
    "notify_status_of_log_in": client_display.notify_status_of_log_in,
    "notify_status_of_account_creation": client_display.notify_status_of_account_creation
}

start()
