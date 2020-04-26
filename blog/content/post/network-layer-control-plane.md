---
title: "Network Layer - Control Plane"
date: 2020-04-26T17:35:24+10:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

* Intra-domain Routing Protocol
  * Link State - i.e. Open Shortest Path First (OSPF)
  * Distance Vector - i.e. Routing Information Protocol (RIP)

* Inter-domain Routing Protocol
  * Path Vector i.e. Border Gateway Protocol (BGP)

# Routing Algorithms

## Link State (Global)

All routers have knowledge of the costs of each router to their peers.

When a new link state message is received, the router forwards the message to its peers.

Dijkstra's Algorithm - Find best route via costs

By using Dijkstra's algorithm, a **forwarding table** can be constructed which tells the router which peer to send a packet to next, to best deliver that packet to a node.

### Issues

* Scalability - Requires O(nodes * edges) complexity
* Scalability - O(N^2) operation for Dijkstra's Algorithm
* Transient Disruptions - Network failures
  * All routers may not have the same shared best path, and may send back to the previous host
* Incorrect link cost may be advertised

## Distance Vector (Decentralised)

Each router only has knowledge of its adjacent peers.  

* Bellman-Ford equation
  * ![](Screenshot from 2020-04-26 17-56-34.png)

* Each router maintains its shortest distance to every destination via its neighbours
* Each router computes its shortest distance to every destination via any of its neighbours

***Distance vector is created and shared between routers - like a shared table, as opposed the link state where each router makes calls to every other router***

This is a better method as:

* Distributed - Shared distance vector
* Asynchronous - Only happens when a cost changes

* Initialise with immediate peers
* Kth simultaneous rounds - Best K+1 hop paths

### Issues

* Count to Infinity Problem
  * Negative changes to the network update slowly (because all devices prefer to use the best-case/shortest link)
  * Solution - **Poisoned Reverse Rule**
    * `A` -> `B` -> `C`
    * `A` tells `B` that `A->C` is infinity, so that B won't route back to `A`
* Advertise incorrect path cost

# Internet Control Message Protocol (`ICMP`)

Used by hosts and routers to communicate network level information.

It uses IP datagrams

* Error reporting - unreachable network, host or port
* Echo requests and replies

Message: Type, Code, IP Header, First 8 bytes of IP datagram payload (containing TCP/UDP port numbers)


|Type|Code|Description|
|:---:|:---:|:--------|
|0|0|echo reply (ping)|
|3|0|destination network unreachable|
|3|1|destination host unreachable|
|3|3|destination port unreachable|
|3|4|fragmentation needed - DF (Do-not-fragment) flag was set|
|8|0|echo request (ping)|
|11|0|TTL expired|
|11|1|fragment reassembly time expired|
|12|0|bad IP header|

The n-th set of UDP segments has `TTL=n`.

When the n=th set reaches the n'th router, TTL expire is returned, along with the IP address of the router