---
title: "Lab 04 - Exploring TCP"
date: 2020-03-29T22:09:58+11:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

# Exercise 1: Understanding TCP using Wireshark

File: [tcp-ethereal-trace-1](./tcp-ethereal-trace-1)

## What is the IP address of gaia.cs.umass.edu?

`gaia.cs.umass.edu` has an IP address of `128.119.245.12`.

## On what port number is it sending and receiving TCP segments for this connection?

The server is using port `80` for its communication.  

## What is the IP address and TCP port number used by the client computer (source) that is transferring the file to gaia.cs.umass.edu?

The source computer has an IP address of `192.168.1.102`, and is using port `1161`

## What is the sequence number of the TCP segment containing the HTTP POST command?

> Note that in order to find the POST command, you’ll need to dig into the packet content field at the bottom of the Wireshark window, looking for a segment with a “POST” within its DATA field. 

Sequence number `232129013` (Packet #4) is the TCP segment which contains the POST command

## Consider the TCP segment containing the HTTP POST as the first segment in the TCP connection.  

* What are the sequence numbers of the first six segments in the TCP connection (including the segment containing the HTTP POST) sent from the client to the web server?
  * Do not consider the ACKs received from the server as part of these six segments.
* At what time was each segment sent?  
* When was the ACK for each segment received?  
* Given the difference between when each TCP segment was sent, and when its acknowledgement was received, what is the RTT value for each of the six segments? 
* What is the EstimatedRTT value (see relevant parts of Section 3.5 or lecture slides) after the receipt of each ACK?
  * Assume that the initial value of EstimatedRTT is equal to the measured RTT ( SampleRTT ) for the first segment, and then is computed using the EstimatedRTT equation for all subsequent segments.
  * Set alpha to 0.125

|#|Seq no|Time Sent|Time ACKd|ACK #|Sample RTT|Estimated RTT|Packet Length|Payload Length|
|--:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|4|`232129013`|0.026|0.053|6|0.027|0.027|619|565|
|5|`232129578`|0.041|0.077|9|0.036|0.028|1514|1460|
|7|`232131038`|0.054|0.124|12|0.070|0.04|1514|1460|
|8|`232132498`|0.056|0.169|13|0.113|0.049|1514|1460|
|10|`232133958`|0.077|0.217|15|0.140|0.0.06|1514|1460|
|11|`232135418`|0.078|0.267|16|0.189|0.07|1514|1460|

Note: The Estimated RTT can be calculated from the formula:  
`eRTT = (1-a) * last_eRTT + a * sampleRTT`

## What is the length of each of the first six TCP segments? 

See above.

## What is the minimum amount of available buffer space advertised at the receiver for the entire trace? 

Packet #2 suggests that the minimum amount of buffer space available is `5840` (Calculated window size).  

## Does the lack of receiver buffer space ever throttle the sender?

No, the sender sends at most only 1514 bytes at a time, which is under the minimum buffer space

## Are there any retransmitted segments in the trace file? What did you check for (in the trace) in order to answer this question?

We can look for repeated segment numbers (seq and ack pair) to find if there are any segments that were retransmitted.  
No repeated segment numbers were found, so we can assume that there are **no retransmitted segments**.

## How much data does the receiver typically acknowledge in an ACK? 

> Can you identify cases where the receiver is ACKing every other received segment (recall the discussion about delayed acks from the lecture notes or Section 3.5 of the text). 

Typically the receiver acknowledges `1460` bytes.  

There is a case where packets 54, 55 and 56 are all acknowledged by the single ACK packet 60.  
This may happen if all three packets arrive simultaneously, and so there is no need to acknowledge each received packet.

## What is the throughput (bytes transferred per unit time) for the TCP connection?  

We can get the throughput of this connection by calculating the sequence number delta, and dividing it by the time delta.  

Note: We will look at the POST exchange from segment 4 to segment 206, and ignore the beginning connection setup.

### To calculate size: sequence number delta

The start of the data is segment 4 - seq no 232129013.  
The end of the server response is segment 206 - seq no 232293103.

There were 232293103 - 232129013 = 164090 bytes transmitted

### To calculate time: delta

Segment 4 was transmitted at 0.026s.  
Segment 206 was transmitted at 5.6511s.

The time delta is 5.6511 - 0.026 = 5.557 seconds.

### To calculate throughput

164090 bytes / 5.557 seconds is `29528.52 bytes/second`

# Exercise 2: TCP Connection Management 

![](Screen_Shot_2018-08-28_at_8.06.30_pm.png)

## What is the sequence number of the TCP SYN segment that is used to initiate the TCP connection between the client computer and server?

`2818463618`

## What is the sequence number of the SYNACK segment sent by the server to the client computer in reply to the SYN?

`1247095790`

### What is the value of the Acknowledgement field in the SYNACK segment? How did the server determine that value?  

The acknowledge number is `2818463619`.  

The server determines it to be the `SYN value + 1`.  
Hence `2818463618 + 1 = 2818463619`

## What is the sequence number of the ACK segment sent by the client computer in response to the SYNACK?

`2818463619`

### What is the value of the Acknowledgment field in this ACK segment? Does this segment contain any data? 

`1247095791`

_Which is `1247095790 + 1`_

It doesn't contain any user data

## Who has done the active close - client or the server?

* How you have determined this?
* What type of closure has been performed?
  * 3 Segment (FIN/FINACK/ACK)
  * 4 Segment (FIN/ACK/FIN/ACK)
  * Simultaneous close

The client initiated the active close as seen by segment 304.  
Segment 305 is a response to the active close, as seen by the acknowledgement of sequence number 2818463652 (segment 304).  

This looks like a `simultaneous close`, as the server sends its own FINACK before it receives the client's FINACK (FINACK from the server has an acknowledgement number of the packet that it will (but hasn't yet) receive from the client).

|Handshake Close|Simultaneous Close|
|:--:|:--:|
|![](http://www.tcpipguide.com/free/diagrams/tcpclose.png)|![](http://www.tcpipguide.com/free/diagrams/tcpclosesimul.png)|

## How many data bytes have been transferred from the client to the server and from the server to the client during the whole duration of the connection?  

> What relationship does this have with the Initial Sequence Number and the final ACK received from the other side?  

The `final ACK - initial seq number` is equal to the number of bytes transferred.

`2818463653 - 2818463618 = 35` bytes
