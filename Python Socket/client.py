"""
This is the client for the python socket
"""
import socket
import pickle  # Use this to send objects and such
from universal_modules.user_classes.Account import Account
from typing import Any


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
        print(msg)  # Replace this with some form of protocol
    # This is a blocking piece of code (Maybe run an update once every few milliseconds?)


def start() -> None:
    """
    The main loop of the client
    """
    account = Account()
    print("Create a new account or log in?")
    user_input = input()

    if user_input == "create":
        account.create_new_account()
        send("create_account", account)

    # send(input())
    send(DISCONNECT_MESSAGE, None)  # Disconnect when finished


start()
