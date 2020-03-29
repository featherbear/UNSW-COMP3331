#!/usr/bin/python3

'''
Your Task: Implementing Ping Client

You should write the client (called PingClient.java or PingClient.c or PingClient.py) such that it sends 10 ping requests to the server.
Each message contains a payload of data that includes the keyword PING, a sequence number, and a timestamp.
After sending each packet, the client waits up to one second to receive a reply.
If one second goes by without a reply from the server, then the client assumes that its packet or the server's reply packet has been lost in the network. 

You should write the client so that it executes with the following command:
$> python PingClient.py host port
where host is the IP address of the computer the server is running on and port is the port number it is listening to. In your lab you will be running the client and server on the same machine. So just use 127.0.0.1 (i.e., localhost) for host when running your client. In practice, you can run the client and server on different machines.

The client should send 10 pings to the server. Because UDP is an unreliable protocol, some of the packets sent to the server may be lost, or some of the packets sent from server to client may be lost. For this reason, the client cannot wait indefinitely for a reply to a ping message. You should have the client wait up to one second for a reply; if no reply is received, then the client should assume that the packet was lost during transmission across the network. It is important that you choose a reasonably large value, which is greater than the expected RTT (Note that the server artificially delays the response using the AVERAGE_DELAY parameter). In order to achieve this your socket will need to be non-blocking (i.e. it must not just wait indefinitely for a response from the server). If you are using Java, you will need to research the API for DatagramSocket to find out how to set the timeout value on a datagram socket (Check: http://java.sun.com/javase/6/docs/api/java/net/Socket.html ). If you are using C, you can find information here: http://www.beej.us . Note that, the fcntl() function is the simplest way to achieve this.

Note that, your client should not send all 10 ping messages back-to-back, but rather sequentially. The client should send one ping and then wait either for the reply from the server or a timeout before transmitting the next ping. Upon receiving a reply from the server, your client should compute the RTT, i.e. the difference between when the packet was sent and the reply was received. There are functions in Java Python and C that will allow you to read the system time in milliseconds. The RTT value should be printed to the standard output (similar to the output printed by ping; have a look at the output of ping for yourself). An example output could be:

ping to 127.0.0.1, seq = 1, rtt = 120 ms

We prefer that you show the timeout requests in the out put. Only replace the 'rtt=120ms' in the above example with 'time out'. You will also need to report the minimum, maximum and the average RTTs of all packets received successfully at the end of your program's output.

Message Format

The ping messages in this lab are formatted in a simple way. Each message contains a sequence of characters terminated by a carriage return (CR) character (\r) and a line feed (LF) character (\n). The message contains the following string:

PING sequence_number time CRLF

where sequence_number starts at 0 and progresses to 9 for each successive ping message sent by the client, time is the time when the client sent the message, and CRLF represent the carriage return and line feed characters that terminate the line. 
'''

# ping to 127.0.0.1, seq = 1, rtt = 120 ms

import sys

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} host port")
    sys.exit()
_, HOST, PORT = sys.argv
PORT = int(PORT)

from socket import socket, AF_INET, SOCK_DGRAM
from select import select
from time import time

client = socket(AF_INET, SOCK_DGRAM)

RTTs = []

for seq in range(10):
    startTime = int(time()*1000)
    client.sendto(f"PING {seq} {startTime}\r\n".encode(), (HOST, PORT))
    if select([client], [], [], 1)[0]:
        data = client.recvfrom(1024)[0]
        rtt = int(time()*1000) - startTime
        response = f"rtt = {rtt}ms"
        RTTs.append(rtt)
    else:
        response = "time out"
    print(f"ping to {HOST}, seq = {seq}, {response}")

if len(RTTs) == 0:
    print("\nAll ping requests timed out")
else:
    print(f"\nMinimum RTT: {min(RTTs)}ms")
    print(f"Maximum RTT: {max(RTTs)}ms")
    print(f"Average RTT: {sum(RTTs)/len(RTTs)}ms")