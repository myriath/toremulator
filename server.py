import signal
import socket
import sys
import time
from socket import getaddrinfo
import threading

"""
* https://github.com/jerrinss5/Multi-threaded-Proxy-Server/blob/master/server.py#L289

https://medium.com/@gdieu/build-a-tcp-proxy-in-python-part-1-3-7552cd5afdfe
https://levelup.gitconnected.com/how-to-build-a-super-simple-http-proxy-in-python-in-just-17-lines-of-code-a1a09192be00
https://ohyicong.medium.com/how-to-create-tor-proxy-with-python-cheat-sheet-101-3d2d619a1d39
"""


class Proxy:
    def __init__(self, config):
        signal.signal(signal.SIGINT, self.shutdown)
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocket.bind((config['HOST_NAME'], config['BIND_PORT']))
        self.serverSocket.listen(10)
        self.logInfo(f"Listening at {config['HOST_NAME']}:{config['BIND_PORT']}...\n")

    def listen(self):
        while True:
            (clientSocket, clientAddress) = self.serverSocket.accept()

            client_details_log = "******************** Client Details:- ********************\n"
            client_details_log += "Client host name: " + str(clientAddress[0]) + "\nClient port number: " + str(
                clientAddress[1]) + "\n"
            client_socket_details = getaddrinfo(str(clientAddress[0]), clientAddress[1])
            client_details_log += "Socket family: " + str(client_socket_details[0][0]) + "\n"
            client_details_log += "Socket type: " + str(client_socket_details[0][1]) + "\n"
            client_details_log += "Socket protocol: " + str(client_socket_details[0][2]) + "\n"
            client_details_log += "Timeout: " + str(clientSocket.gettimeout()) + "\n"
            client_details_log += "********************************************************\n"
            self.logInfo(client_details_log)

            d = threading.Thread(name=str(clientAddress),
                                 target=self.proxyThread,
                                 args=(clientSocket, clientAddress),
                                 daemon=True)
            d.start()

    def proxyThread(self, sock, clientAddress):
        print(f"sock:{sock}; args:{args}")
        startTime = time.time()
        request = sock.recv(1024)
        if request:
            reqLength = len(request)
            self.logInfo(f"Client {clientAddress[0]}: request length {reqLength}\n")
            self.logInfo(f"Client {clientAddress[0]}: requested {str(request).splitlines()[0]}\n")

            reqParts = requests.split(' ')
            if reqParts[0] == 'GET':
                httpPart = reqParts[1]

        else:
            sock.send("")
            sock.close()
            self.logInfo(f"Client {clientAddress[0]}: connection closed\n")
        return

    def shutdown(self, signal, frame):
        print(f"signal:{signal}; frame:{frame}")
        self.serverSocket.close()
        exit(0)

    def logInfo(self, msg):
        with open('log.txt', 'a') as f:
            f.write(msg)


def main():
    # clear log file
    f = open('log.txt', 'w')
    f.close()

    proxy = Proxy({"HOST_NAME": "localhost", "BIND_PORT": 12345})
    proxy.listen()


if __name__ == "__main__":
    main()
