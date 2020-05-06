---
title: "Transport Layer"
date: 2020-03-23T15:44:56+11:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

* Provides logical communication between application processes running on different hosts
* Breaks application messages into segments
  * When received, the segments are reassembled back into messages and passed to the application layer

# Multiplexing

The network is a shared resource, used by many devices, applications and programs.  
When messages are split into segments, **headers** are added to the eventual packets, so they can be delivered to the correct socket later.

i.e. with UDP packets - When the host receives the UDP segment, it checks what the destination port of the packet is, then passes it to the right port.

For TCP sockets, they are identified by a 4-tuple of the source's IP and port, as well as the destination's IP and port

# UDP - User Datagram Protocol

* Connection-less - No handshaking
  * Therefore can be considered faster, as there is less delay
* Smaller header size
* No congestion control - no rate limiting
* Each UDP segment is handled independently from other segments

## Segment Structure

In Order:

* Source Port (2 bytes)
* Destination Port (2 bytes)
* Length (2 bytes)
* Checksum (optional) (2 bytes) | Payload

## Checksum

Attempt to detect errors in transmitted segments.  
They can be caused by router memory errors, driver bugs, or even electromagnetic interference.  

The checksum is equal to the one's complement addition of the segment contents.  
**If the MSB overflows, a wraparound increment occurs, and the LSB is increased by one.**

_In other words: Add all of the 16 bit sequences, adding a wraparound if needed. Then take the one's complement (flip all bits)_

When a segment is received, the received bits are also added to this checksum, for a result that should be 1111 1111 1111 1111.  
If this is not the case, then an error has occurred.

# Reliable Data Transfer

## Issues of &quot;Best Effort&quot; transport

* Corruption
* Lost packets
* Delayed packets
* Out of order packets
* Duplicate packets

The characteristics of the unreliable channel determines how complex the reliable data transfer protocol needs to be.

# RDT1.0 - Reliable Transfer over a Reliable Channel

Nothing is needed to be done

# RDT2.0 - Channel with Bit Errors

![](Screenshot from 2020-03-23 16-28-59.png)

* Bits may be flipped while in transmission
* Checksum is sent along with the data - **error detection**
* The receiver sends back an **acknowledgement** to the sender
  * `ACK` - Acknowledgement - OK
  * `NAK` - Negative acknowledgement - Not OK
  * Sender can then **retransmit**

!! Acknowledgements can also get corrupted

# RDT2.1 - Channel with Bit Errors. Sequence number bit in packets

![](Screenshot from 2020-03-23 16-35-32.png)

* Sender adds a sequence number (`0`/`1`) to the packet
* Receiver checks if the next packet has the right expected sequence number
  * If the sequence number is received twice, mark as duplicate and ignore
    * Still sends ACK or NACK

# RDT2.2 - Channel with Bit Errors. Sequence number and only ACKs

![](Screenshot from 2020-03-23 16-38-34.png)

* Same RDT2.1
* ACK contains the sequence number of the last successfully received packet

# RDT3.0 - Channel with Bit Errors and Packet Loss

|no loss|packet loss|ACK packet loss|premature timeout / delay|
|:---:|:---:|:---:|:---:|
|![](Screenshot from 2020-03-23 16-53-36.png)|![](Screenshot from 2020-03-23 16-53-42.png)|![](Screenshot from 2020-03-23 16-53-47.png)|![](Screenshot from 2020-03-23 16-53-52.png)|
* Sender waits for some time to receive an ACK
* Retransmits the packet if no ACK was received
* If the packet eventually receives the receiver, and the retransmitted packet is also received, the receiver will discard the retransmitted packet (Handling of duplicate sequence numbers)

## Stop-and-Wait Operation

![](Screenshot from 2020-03-23 18-44-56.png)

U_sender = L/R / (RTT + L/R)

## Pipelining

* Increases the utilisation of the available resources :)
* Allows multiple packets to be sent at the same time
* Increases the range of usable sequence numbers
* Implements buffers at the sender and receiver

|Without Pipelining|With Pipelining|
|:----------------:|:-------------:|
|![](Screenshot from 2020-03-23 18-48-07.png)|![](Screenshot from 2020-03-23 18-48-14.png)|

* `window size = U * (R/L*RTT + 1)`

### Go-Back-N

![](Screenshot from 2020-03-23 19-14-26.png)

* Sender can have up to `N` un-ACK'd packets in the pipeline
* The sender has **one single timer** for the oldest un-ACK'd packet
  * If this timer elapses - then ALL un-ACK'd packets are retransmitted
  * When the ACK for the oldest packet is received, the countdown timer is reset to its initial wait time
* Receiver has no buffer
  * Out of order packets are discarded
  * Only sends **cumulative ACK** - does not acknowledge out of order packets
* **Receiver Window Size = 1**
* **Sender Window Size < 2^m**

* If `size (N) = 2^m`
  * If all of the packets were received
    * The sliding window would move to the next `0 - n` sequences
    * If all ACKs were lost, the sender would retransmit all of the first packets
    * The receiver would then consider these retransmitted packets as the _next_ `0 - n` packets
  * ![](Screenshot from 2020-03-23 19-41-14.png)
  * [Source](https://www.eit.lth.se/fileadmin/eit/courses/etsf15/vt16/Problems/ComNet-FramingProblems.pdf)

### Selective Repeat

![](Screenshot from 2020-03-23 19-16-30.png)

* Sender can have up to `N` un-ACK'd packets in the pipeline
* Each packet has its own timer
* Receiver has a buffer, and accepts out of order packets

#### Window Size Consideration

* **Receiver Window Size <= 2^(m-1)**
* **Sender Window Size <= 2^(m-1)**

The sender window size should be less than or equal to HALF the sequence number space.  
Otherwise, if an ACK was lost, a successfully-received but not successfully-acknowledged packet might be retransmit, and considered to be a packet in the next sliding window.

