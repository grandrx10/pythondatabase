"""
Program By Richard Yang
"""
import socket
import threading  # allows for multiple threads to be used (does not require other clients to wait)
import pickle
from typing import Any

# Import Classes
from server_modules.Database import Database
from universal_modules.user_classes.Account import Account  # Import this or pickle will not understand

HEADER = 64
# The first message to the server is going to be a header of length 64 informing the server
# of how many bytes are going to come next
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())  # socket.gethostbyname(socket.gethostname())
# gethostbyname() gets the ip of the computer input
# socket.gethostname() gets the name of the host computer
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
# when the server recieves this message from the client, disconnect them

server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
# socket.socket() creates a new socket
# family controls what type of address are we accepting connections for
# SOCK_STREAM streaming data through the socket
server.bind(ADDR)
# we are binding our socket to our address


def handle_client(conn, addr) -> None:
    """
    Handle a client's connection and communications. Contains the main loop for the handling
    of the client's connection.
    """
    print(f"New Connection {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)  # every time messages are sent, it is encoded, so must decode
        # Recieve messages from the client. This is a blocking piece of code, that stops this thread
        # We can choose how many bytes we recieve. We need a protocol (algorithm) to determine the amount we should
        # recieve.
        if len(msg_length) > 0:
            msg_length = int(msg_length)
            # find the length of the next message
            msg = pickle.loads(conn.recv(msg_length))
            # store the message

            # Disconnect the user when the disconnect message is recieved
            if msg["function_to_run"] == DISCONNECT_MESSAGE:
                connected = False
            else:
                # put the return msg into the proper format
                return_msg = str_to_function[msg["function_to_run"]](msg["parameter"])
                # Send the return message to the client
                send(function_to_run=return_msg["function_to_run"], parameter=return_msg["parameter"], conn=conn)

    conn.close()  # close the connection when the client leaves


def start() -> None:
    """
    the main loop of the server
    """
    server.listen()
    print(f"Server is listening on {server}")

    while True:
        conn, addr = server.accept()
        # this waits for a new connection to the server
        # when a connection occurs, we will store the connection and address
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        # run handle_client() in a separate thread with arguments conn, addr
        thread.start()
        print(f"[Active Connections] {threading.active_count() - 1}")
        # print out how many active threads are running


def send(function_to_run: str, parameter: Any, conn) -> None:
    """
    Send a message to a specific client
    """
    # Construct the message that we will send
    msg = {"function_to_run": function_to_run, "parameter": parameter}
    # Encode the message into bytes
    message = pickle.dumps(msg)
    # Find the length of the message we are sending
    msg_length = len(message)
    # Encode the length of the message
    send_length = str(msg_length).encode(FORMAT)
    # Pad the length of the message until it is of the proper length HEADER
    send_length += b' ' * (
            HEADER - len(send_length))  # b' ' is byte representation of blank (This is for padding)
    # Send the length of the message
    conn.send(send_length)
    # Send the message itself
    conn.send(message)


# Create the database connection here
database = Database()
# This dictionary is a mapping of strings to their function counterparts
str_to_function = {
    "create_account": database.create_account
}

print("server is starting")
start()
