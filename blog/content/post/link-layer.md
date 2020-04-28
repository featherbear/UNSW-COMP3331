---
title: "Link Layer"
date: 2020-04-26T18:43:23+10:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

# Services

* Framing and Link Access
* Flow Control
* Error Detection
* Error Correction
* Half Duplex / Full Duplex


# Ethernet

* Connectionless - No handshaking
* Unreliable - No ACKs or NACKs
* Unslotted CSMA/CD with Binary Backoff

## MAC Addresses

> aka LAN address / physical address / Ethernet address

MAC addresses are unique 48-bit addresses that are written into the ROM of the network adapter. Being in the ROM they cannot be changed (usually).  

Compared to IP addresses, MAC addresses are hard-coded addresses, and have a flat name space.  
IP addresses on the other hand, are dynamically assigned (DHCP), and operate hierarchically.

## Framing

* Preamble - seven bytes of `0b10101010`
* Start Frame Delimiter (`SFD`) - `0b10101011`
* End of Frame - Absence of transition in Manchester encoded signal
* GAP - 12 bytes (96 bits) worth of idling

Preamble (7 bytes) | SFD (1 bytes) | Destination MAC (6 bytes) | Source MAC (6 bytes) | Type/Length (2 bytes) | Payload (46-1500) bytes | CRC (4 bytes) | GAP

# Error Detection

> EDC - Error Detection and Correction.  
The more EDC bits, the higher the detection and correction rate of bit-errors

## Possible Algorithms

* Two copies of the same message
  * Can detect 3 errors
  * Cannot correct them though (unsure which bit was flipped)
  * 50% overhead

* `n`-bit even parity
  * Every `n` bits add an extra bit to make the number of 1's even (or odd if using odd parity)
  * Can detect but not correct

* 2D Parity
  * Split bits into rows and columns
  * Parity in rows, and also in columns
  * Can detect and correct a single bit

* Checksums
  * Add up data in N-bit words
  * Can now detect all burst errors up to `N`
  * Cannot correct

* Cyclic Redundancy Check (CRC)
  * Cannot correct
  * ![](Screenshot from 2020-04-26 19-00-22.png)
  * ![](Screenshot from 2020-04-26 19-01-04.png)

# Multiple Access Links

* Point To Point - One device to another device
* Broadcast - Shared medium

* Old - Bus network - Single cable that all devices share
  * Needs CSMA/CD
* New - Star network - Each device connects to a switch device
  * Does not need CSMA/CD

* Collision occurs if two or more signals are received at the same time
* Protocols are set in place to determine how nodes take turns to transmit

* Channel Partitioning
  * Allocating time / frequency / coding ranges to each device
  * TDMA (Time Division Multiple Access)
    * Limits time
  * FDMA (Frequency Division Multiple Access)
    * Limits bandwidth
* Taking Turns - Wait for the current transmitting device to finish
  * Polling - Master / Slave configuration
    * Polling overhead, latency, single point of failure (master is down)
  * Token
    * Token overhead, latency, single point of failure (lost token)
* Random Access
  * Don't try at all to avoid collision, just attempt to send
  * Delay the retransmit for a period of times
  * i.e [CSMA/CD](#csma) and [CSMA/CA](#csma)

## Slotted ALOHA

> ALOHA because, it was done in Hawaii...

* Wait for free slot then transmit
* If slot was not free, transmit on next slot

* Con - Slots are wasted (idle slots)
* Con - Requires some sort of synchronisation clock
* Only 37% efficiency (1/e = 0.37) - maths.

## Unslotted ALOHA

* No synchronisation clock
* 1/2e = 0.18 = 18% efficiency

## CSMA

> Carrier Sense Multiple Access - Listen before transmission!

When multiple devices transmit over the same line (bus), corruption and interference will occur.  

NOTE: This applies only to mediums that are shared - ie WiFi, or old network busses.  
With modern wired Ethernet, each line is connected to a switch - and there is only ever one device communicating over the Ethernet cable.  
(There are two pairs of Ethernet cables - one for receiving and one for transmitting)

### Collision Detection

* NIC receives datagram from network layer, create fram,e
* NIC senses channel business
  * If idle - transmit
  * If busy - wait
* While transmitting, if another transmission is detected; abort and send jam signal
  * Wait for a random amount of time before attempting to retransmit
  * Binary backoff (exponential) - m'th time will choose K at random from {0, 1, 2, 4, 2^m - 1}, and wait for K * 512 bits

### Collision Avoidance

...


# ARP - Address Resolution Protocol

The ARP protocol is used to map IP addresses to MAC addresses, as like how DNS servers map hostnames to IP addresses.  

As the ARP protocol operates on the Link Layer - there is no known structure to the current network.  
A device will broadcast an `ARP Query` to the entire network (Using the broadcast destination address `FF:FF:FF:FF:FF:FF`).  
This query contains the IP address of a target MAC address.  

All devices on the network will receive this ARP Query packet, but only the device whose IP address matches will reply - directly back to the requestor (unicast).

When the reply arrives, it will be cached for a period of time, before that IP-to-MAC entry expires

## ARP Connectivity

When packets are transmitted, they are regularly encapsulated (IP frame being wrapped in an Ethernet frame) and de-encapsulated (Ethernet frame removed, leaving the IP frame). When a network interface receives a packet, it will de-encapsulate the packet - giving the IP packet.  
It can then be processed, and if need be - transmitted to another device.  

At each step, the MAC source and destination of the packet is different. However the underlying IP packet remains the same.

## ARP Poisoning

### Denial of Service (DoS)

A malicious device replies to ARP Queries with fake MAC addresses.  
The requesting device will receive this query, and attempt to send a packet to a non-existent device

### Man In The Middle (MITM)

A malicious device replies to an ARP Query with its own MAC.  
The requesting device will receive the malicious device's MAC, and send all its data to the malicious device.  
The malicious device then has access to the data being transmitted and received from the requesting device.  

# Ethernet Switches

Ethernet switches are link-layer devices that store and forward Ethernet frames to the right place.  
They provide each host connected with a dedicated full-duplex Ethernet link.  
To hosts on the network, switches are transparent.  

They store entries of requested MAC addresses and the correct link interface in a **switch table**.  
When frame is received, the MAC address and link interface of the frame is compared against its table to see where to forward the frame to.  

* For frames that need to be forwarded to the link interface where they just came from - they are dropped
* For frames that need to be forwarded to another link interface - they are forwarded
* For frames that do not match any entry in the switch table - They are flooded / transmitted to all other interfaces

![](Screenshot from 2020-04-28 21-57-19.png)

_Note: Ethernet hubs are link-layer devices that store and forward Ethernet frames to every interface it is connected to._