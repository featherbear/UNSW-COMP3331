---
title: "TCP Protocol"
date: 2020-04-25T00:30:51+10:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

* Stream of bytes that will arrive in the right order

# Segments

A large TCP packet is split into segments to allow it to be transmitted over the wire.  

The largest packet size, according to the Ethernet protocol is 1500 bytes; this is known as the MTU.  

IP layer requires at least 20 bytes for its header.  
TCP layer requires at least 20 bytes for its header.  
As OSI layers encapsulate each other, the maximum size of a TCP packet is 1460 bytes.  

* **Maximum Transmission Unit (MTU)** - Up to 1500 bytes with Ethernet
* **Maximum Segment Size (MSS)** - Up to 1460 bytes (MTU - 20 - 20)

# Structure

**Header**

* 2 bytes - Source port
* 2 bytes - Destination port
* 4 bytes - Sequence number
* 4 bytes - Acknowledgement
* 2 bytes - Flags
* 2 bytes - Receive Window
* 2 bytes - Checksum
* 2 bytes - Urgent Pointer
* Optional n bytes - Options

**Payload**

# Sequence Number

The sequence number of a TCP segment is the position of the first byte in the segment.  

SeqNo = ISN + K

# ACK Sequence Number

The acknowledgement number is the **next byte** the client accepting from the other host

ACKNo = SeqNo + Length

If a packet is lost and later packets arrive, the receiving will keep sending the ACK for the byte number of the lost packet. [Refer to TCP Packet Buffer](#tcp-packet-buffer)

---

**Example**  

![](Screenshot from 2020-04-25 00-39-35.png)

`Seq=42, ACK=79, data='C'` -> This packet is byte #42, I am next expecting the reply with `Seq=79`

# Packet Piggybacking

Multiple packet payloads within the same packet.  

_i.e. Response + ACK_

# TCP Packet Buffer

![](Screenshot from 2020-04-25 00-45-46.png)

## RTT Time and Timeout

![](Screenshot from 2020-04-25 00-54-04.png)

- If timeout too short - premature timeout, unnecessary retransmission
- If timeout too long - slow reaction to segment loss and lower throughput

Solution: Maths.  

SampleRTT - Time from segment transmission until last ACK receipt (ignore retransmission).  

**EstimatedRTT = (1-alpha) * EstimatedRTT + alpha*SampleRTT**

The timeout interval is calculated to be **Timeout Interval = EstimatedRTT + 4*DevRTT**.  

Where there is a safety margin to allow for deviations in the EstimatedRTT.

**DevRTT = (1-beta)\*DevRTT + B\*|SampleRTT-EstimatedRTT|)**

* `alpha == 0.125`
* `beta == 0.25`

# TCP Fast Retransmit

Duplicate ACKs to trigger early retransmission.

Trigger: Triple Duplicate ACK - When the same ACK is received 4 times (3 times extra).  

This mechanism bypasses the timeout (Which is often relatively long)

# Flow Control

Sockets usually have a `RcvBuffer` value of 4096 bytes.  
This controls the size of the buffer.

The **Receive Window** (`rwnd`) value in the TCP header field of receiver-to-sender segments is the free space of the RcvBuffer.

By sending the size of the free space in the buffer, the sender will be ensured that the next data they transmit will not overflow the receiver's buffer

# Connection Management

* Handshake - Agreement on connection and connection parameters.

## Three Way Handshake

* Client sends `TCP SYN` (contains initial sequence number `x`)
* Server sends `TCP SYNACK` (contains their own initial sequence number `y`) `ACKNo=x+1`
* Client sends `TCP ACK` `ACKNo=y+1`

## Lost `SYN` packets

There is a timer (usually 3 seconds) that waits for a SYNACK.  
It will retransmit if needed.  

A SYN could also be transmitted quickly by creating a new connection

## Closing Connections

When the FIN bit in a packet is sent, the host can no longer transmit data _(*)_.  
It can however, still receive data  

_*: ACK packets are not counted as data, and can still be sent_

* A sends TCP segment with `FIN=1`
* B sends `ACK` and possibly its own `FIN`
* A sends `ACK`

## Abrupt Termination

* A sends a reset packet `RST` to B to tell B to stop communicating
* B does not acknowledge the `RST` packet
* A will keep transmitting `RST` packets for each reply it keeps receiving from `B`

# TCP SYN Attack (SYN Flooding)

The SYN Flooding attack causes a server to accept spoofed connections, wasting server resources.  
Whilst the server will eventually close and garbage collect the socket, large numbers of spoofed SYN packets will overwhelm the server, increasing server load.

## Mitigation Techniques

* Increase connection queue size
* Decrease timeout time for the 3 way handshake
* Firewalls
* TCP SYN Cookies

# TCP SYN Cookies

The initial sequence number (hash of source and destination IP and ports) is used as a secret key for a hash.  

When receiving a `SYN`, the server will reply with a `SYNACK` containing this initial sequence number (key).  
The client will then have to reply with an `ACK`, checking that the ACK is equal to the initial sequence number + 1.  
Only if this check is true will the server create the connection.  

This stops attackers from sending many SYN packets - instead they must wait for the server's `SYNACK`, and send a second packet (ACK) with the right details

# Congestion Control

Congestion increases delivery latency, loss rate, and leads to retransmissions.  

![](Screenshot from 2020-04-25 23-49-37.png)

* Knee Point - Point where throughput increases slowly, decay increases fast
* Cliff Point - Point where throughput drops to zero (Congestion collapse), decay approaches infinity

* End to End Congestion Control
  * Congestion inferred from observed loss and delay
* Network-asssited Congestion Control
  * Feedback from networking infrastructure
  * DNA, DECbit, TCP/IP ECN, ATM
  * Authoritative transmission rate

* TCP Send Rate is roughly (cwnd / RTT) (bytes/sec)

* Congestion Window (`cwnd`) - How many bytes can be sent without overflowing routers
  * Computed by the sender using algorithms
* Receive Window (`rwnd`) - How many bytes can be sent without overflowing the receiver's buffers
  * Determined by the receiver (notified to the sender)
* Sender-size window: `min(cwnd,rwnd)`

## Rate Adjustment

* When ACK (of new data) is received, increase rate
* When loss is detected, decrease rate


TCP incorporates two algorithms, TCP Slow Start then AIMD.

## TCP Slow Start (Bandwidth Discovery)

Increase transmission rate exponentially (doubled) until the first loss event.  

* Initial rate slow, but ramps up exponentially

## Additive Increase Multiplicative Decrease (`AIMD`)

* Additive Increase - Increases `cwnd` every RTT (ACK received) until loss detected
* Multiplicative Decrease - Half the `cwnd`

---

## Steady State Threshold (`ssthresh`)

The steady state threshold is the `cwnd` value which will trigger the protocol to change from TCP Slow Start to AIMD.  
This is often set to some high value, and is decreased (by means of halving) on loss

## TCP Reno (New)

* cwnd = 1 on timeout
* cwnd = cwnd/2 on triple duplicate ACK (TCP fast retransmit)

## TCP Tahoe (Old)

* cwnd = 1 on timeout and triple duplicate ACK