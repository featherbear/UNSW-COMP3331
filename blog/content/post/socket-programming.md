---
title: "Socket Programming"
date: 2020-03-22T20:24:23+11:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

# UDP (User Datagram Protocol)

* No connection setup between client and server
  * No hand shaking
  * The sender explicitly attaches their sending port from the packet
    * The receiver reads this value in the packet to determine who 'sent' it
* Fire and forget - no certainty that the data is received correctly, in correct order, or if received at all.
* The server might not even be on at all!

## Pseudo Code

* Create socket
  * Bind port (Server)
* Loop
  * Send UDP datagram to known port
  * Read UDP datagram
* Close socket

# TCP (Transmission Control Protocol)

* Client contacts the server to establish a connection.
* Server then creates a new socket to communicate with the client - **Different socket for welcoming than for connection**
* Reliable - Packets will arrive in order, and if packets are lost, they will be retransmitted

## Pseudo Code

* Create socket
* Connect to server (Client only)
* Bind port (Server only) 
* Listen for requests (Server only)
  * Accept request
* Communicate
* Close

## Concurrent TCP Servers

Connection requested are performed in a fork, rather than the main process, so the main process can continue to wait for new connections.