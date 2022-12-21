"""
Program By Richard Yang
"""
# https://stackoverflow.com/questions/12362542/python-server-only-one-usage-of-each-socket-address-is-normally-permitted
import socket
import threading  # allows for multiple threads to be used (does not require other clients to wait)
import pickle
from Database import Database
from public.client_modules.Account.Account import Account

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


def handle_client(conn, addr, database) -> None:
    """
    Handle a client's connection and communications
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
            print(msg)
            # store the message

            # if the disconnect message is recieved
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            conn.send("Msg recieved".encode(FORMAT))

    conn.close()  # close the connection when the client leaves


def start() -> None:
    """
    the main loop of the server
    """
    server.listen()
    print(f"Server is listening on {server}")

    # Create the database connection here
    database = Database()

    while True:
        conn, addr = server.accept()
        # this waits for a new connection to the server
        # when a connection occurs, we will store the connection and address
        thread = threading.Thread(target=handle_client, args=(conn, addr, database))
        # run handle_client() in a separate thread with arguments conn, addr
        thread.start()
        print(f"[Active Connections] {threading.active_count() - 1}")
        # print out how many active threads are running


print("server is starting")
start()
