"""
This is the client for the python socket
"""
import socket
import pickle  # Use this to send objects and such
from public.client_modules.Account.Account import Account
from typing import Any


HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

SERVER = "192.168.0.31"  # socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (SERVER, PORT)

client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg: (str, Any)) -> None:
    """
    Encode and send a message to the server.
    """
    message = pickle.dumps(msg)  # Encode the message first
    msg_length = len(message)  # The first message sent must be the length of the message
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))  # b' ' is byte representation of blank (This is for padding)
    client.send(send_length)
    client.send(message)
    # print(client.recv(2048).decode(FORMAT))  # Replace this with some form of protocol
    # This is a blocking piece of code (Maybe run an update once every few milliseconds?)


def start() -> None:
    """
    Start the client
    """
    account = Account()
    print("Create a new account or log in?")
    user_input = input()

    if user_input == "create":
        account.create_new_account()
        send(("new_account", account))

    # send(input())
    send(DISCONNECT_MESSAGE)  # Disconnect when finished


start()


"""
pickle.dump()
pickle.dumps() <- byte strings
pickle.load()
pickle.loads()
"""
