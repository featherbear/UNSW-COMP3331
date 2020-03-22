---
title: "P2P Communication"
date: 2020-03-22T19:50:10+11:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

# Peer-to-Peer

* Each device is both a client and a server
* Does not require a machine that is always on
* Self scability - each client adds extra capacity
* Parallelism, less contention (resource access conflict)
* Redundancy

There are some cons though:

* Action uncertainty - authorisation
* State uncertainty
* Algorithm complexity

---

## Architecture

* No server needs to be always on
* Arbitrary end-systems communicate directly to each other
* Peers are intermittently connected (known as churn)
* Peers have changing IP addresses

## File Distribution Comparison

![](Screenshot from 2020-03-22 19-52-01.png)
![](Screenshot from 2020-03-22 19-52-08.png)
![](Screenshot from 2020-03-22 19-53-00.png)

## BitTorrent

Files are divided into 256 KB chunks.

**Trackers** are servers which maintain a list of **peers** which are associated with a file resource.

Periodically, each peer asks the other peers for a list of chunks that the peer has. The requesting peer would then ask for the rarest chunk from all the lists of chunks.

**Tit-for-tat** - The top four peers that are sending chunks to a given peer, will be sent chunks back. The top 4 peers are reevaluated every 10 seconds.

Every 30 seconds, a random peer is selected to send chunks to - Prevents a peer from being choked - unable to receive chunks as they are not transmitting themselves.

## Distributed Hash Tables

Hash Table where the data is stored and distributed between peers.

Key of a file/resource is determined by a hashing algorithm.  
For an `n`-bit hash function, there can be up to `2^n` peer IDs (`0` - `2^n - 1`).  

Assigning keys - closest ID -> immediate successor

## Circular DHT

Each peer is only aware of its immediate successor and predecessor.

### Circular DHT shortcuts

**Number of Neighbours vs Number of Messages**

The smaller the number of neighbours to maintain, the larger the number of messages have to be sent

2 neighbours, 6 messages  
Worst case: N messages  
Average: N/2 messages

If we increase the number of _neighbours_ (ie second successor, second predecessor), we can reduce the number of messages that may need to be sent around the network.

## Peer Churn

Each peers knows the address of two of its successors, so if the immediate successor is unreachable (leaves, disconnected, etc), then the second successor will take the place as the first.
