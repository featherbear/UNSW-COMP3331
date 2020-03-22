---
title: "Application Communication"
date: 2020-03-10T20:23:15+11:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

We need our applications to interact with other computers and end devices.

# Interprocess Communication

For process on a single machine, there exists various methods to pass data between processes.

For example, shared memory, or a 'pipe'.

However, when communicating between machines, we need another way to pass data.

# Sockets

Processes send and receive messages to and from its socket.

# IP addresses and Ports

When connected to a LAN network, each end device (for an IPv4 system) will have a 32-bit IPv4 address, which is unique to all of the devices in that network.

We can communicate to another device on the same network by addressing that device's IP address.

## Ports

Several processes can run on the same machine, so there is a need to be able to address different processes from other devices - These means are known as ports.

Ports are associated to processes on a machine, and provide the means of communication to and from a given process.

# Network Application Architecture

## Client-server architecture

**Server**

* Provides well-defined interfaces that serve requests and responses
* Long-lived process that waits for requests

The server application often runs on a machine that is always on (high availability), and on one that often ha a permanent/fixed IP address.

**Client**

* Short-lived processes that make requests
* The user-side of the application
* Initiates the communication to the server

## Peer-to-Peer

* Each device is both a client and a server
* Does not require a machine that is always on
* Self scability - each client adds extra capacity
* Parallelism, less contention (resource access conflict)
* Redundancy

There are some cons though:

* Action uncertainty - authorisation
* State uncertainty
* Algorithm complexity

# Application Layer

Defines the types of messages, the syntax of messages, the semantics of messages, rules.

## Requirements for the transport layer

* Data integrity - reliable data transfer
* Timing - low delay?
* Throughput
* Security

## TCP vs UDP

TCP provides reliable tarnsport, flow control, congestion control; but is also connection-oriented; requiring setup betweem the client and server.

UDP does not guarantee successful delivery, but does not contain other overheads that TCP has.

