#!/usr/bin/python3

public_dir = "public"

"""
In this exercise, you will learn the basics of TCP socket programming: how to create a socket, bind it to a specific address and port, as well as send and receive an HTTP packet. You will also learn some basics of HTTP header format. You will develop a web server that handles one HTTP request at a time. Specifically, your web server should do the following:

(i) create a connection socket when contacted by a client (browser).
(ii) receive HTTP request from this connection. Your server should only process GET request. You may assume that only GET requests will be received.
(iii) parse the request to determine the specific file being requested.
(iv) get the requested file from the server's file system.
(v) create an HTTP response message consisting of the requested file preceded by header lines.
(vi) send the response over the TCP connection to the requesting browser.
(vii) If the requested file is not present on the server, the server should send an HTTP “404 Not Found” message back to the client.
(viii) the server should listen in a loop, waiting for next request from the browser.

You don't have to deal with any other error conditions. 

You should write the server so that it executes with the following command: 
$> python WebServer.py <port>

where <port> is the port No your Web server will be listening on.  
Specify a non-standard port number (other than 80 and 8080, and > 1024).
We will use this port number in the URL while issuing requests from the web browser.
"""
import sys, os

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <port>")
    sys.exit()

PORT = int(sys.argv[1])

import mimetypes

import socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("", PORT))
server.listen(1)

print(f"Server listening on port {PORT}")

baseDir = os.path.normpath(os.path.join('./', public_dir)) + "/"
  
while True:
    (sock, addr) = server.accept()
    def _(sock, addr):
        rawData = sock.recv(1024)
        data = rawData.decode().strip().split("\r\n")

        # literally ignore everything in the request but the request line
        requestLine = data[0]
        print(addr, requestLine)

        METHOD, PATH, PROTOCOL = requestLine.split(" ")
        
        # Handle only GET requests
        if METHOD != "GET":
            sock.send("".join([
                f'{PROTOCOL} 501 Not Implemented\r\n',
                'Content-Type: text/html\r\n\r\n',
                '<html><head></head><body>501 Not Implemented</body></html>'
            ]).encode())
            return
        
        # Sanitise - prevent directory traversal
        filepath = os.path.normpath(baseDir + PATH).lstrip(baseDir)

        # Default to index.html
        if filepath == "":
            filepath = "index.html"
        
        # Check if file exists
        if not os.path.exists(filepath):
            sock.send("".join([
                f'{PROTOCOL} 404 Not Found\r\n',
                'Content-Type: text/html\r\n\r\n',
                '<html><head></head><body>404 Not Found</body></html>'
            ]).encode())
            return

        # Unimplemented directory traversal
        if os.path.isdir(filepath):
            sock.send("".join([
                f'{PROTOCOL} 501 Not Implemented\r\n',
                'Content-Type: text/html\r\n\r\n',
                '<html><head></head><body>501 Not Implemented</body></html>'
            ]).encode())
            return

        # Send the file
        with open(filepath, "rb") as f:
            sock.send("".join([
                f'{PROTOCOL} 200 OK\r\n',
                'Content-Type: {mimetypes.guess_type(filepath)[0]}\r\n\r\n',p
            ]).encode())
            sock.send(f.read())

    try:
      _(sock, addr)
    except Exception as e:
      print(e)

    sock.close()

