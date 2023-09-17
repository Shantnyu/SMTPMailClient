# import socket module
from socket import *
# In order to terminate the program
import sys


def webServer(port=13331):
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # Prepare a server socket
    serverSocket.bind(("", port))

    # Listen for incoming connections
    serverSocket.listen(1)

    print(f"Server is listening on port {port}")

    while True:
        # Establish the connection
        print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()  # Accept incoming connections

        try:
            message = connectionSocket.recv(1024).decode()  # Receive the HTTP request from the client
            filename = message.split()[1]

            # Open the client requested file
            f = open(filename[1:], "rb")  # Open the file in binary mode

            outputdata = f.read()  # Read the content of the file

            # Send HTTP headers for a valid request (200 OK)
            response_headers = "HTTP/1.1 200 OK\r\n"
            response_headers += "Content-Type: text/html; charset=UTF-8\r\n"
            response_headers += "\r\n"  # Blank line to indicate the end of headers

            # Send the headers to the client
            connectionSocket.send(response_headers.encode())

            # Send the content of the requested file to the client
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i:i + 1])

            connectionSocket.close()  # Close the connection socket

        except IOError:
            # Send response message for invalid request due to the file not being found (404 Not Found)
            response_headers = "HTTP/1.1 404 Not Found\r\n"
            response_headers += "\r\n"  # Blank line to indicate the end of headers

            # Send the headers to the client
            connectionSocket.send(response_headers.encode())

            # Send a custom error message as the content
            error_message = "<html><body><h1>404 Not Found</h1></body></html>"
            connectionSocket.send(error_message.encode())

            connectionSocket.close()  # Close the connection socket


if __name__ == "__main__":
    webServer(13331)
