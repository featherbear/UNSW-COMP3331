---
title: "Mid-semester Exam"
date: 2020-05-06T17:14:57+10:00

hiddenFromHomePage: true
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

# In DHT, a hash function converts

a. 32-bit IP addresses into 4-bit node identifiers  
**b. A string of ASCII characters to an integer X**  
c. 7-bit ASCII characters to 8-bit ASCII characters  
d. Real numbers to integer numbers  

# Suppose 3 packets arrive simultaneously to a link at which no packets are currently being transmitted or queued. Each packet of length 250 bytes and the link has transmission rate 2Mbps. What is the average queuing delay for the three packets?

a. 3ms  
**b. 1ms**  
c. 2ms  
d. None of these  

> (0t + 1t + 2t) / 3 = 1t

# Suppose that a webpage has four referenced objects all residing on the same server. How many RTTs the client will have to wait to see all objects on the page if it uses non-persistent HTTP?

a. 12  
**b. 10**  
c. 9  
d. 8  

> Webpage: Connection + request = 2 RTT  
> Resource: Connection + request = 2 RTT  
> Webpage + 4x Resource = 10 RTT

# Suppose that a webpage has four referenced objects all residing on the same server. How many RTTs the client will have to wait to see all objects on the page if it uses persistent HTTP with pipelining?

**a. 3**  
b. 1  
c. 4  
d. 2  

> Webpage: Connection + request = 2 RTT  
> 4x Resources (persistent + pipelining): 1 RTT
> Webpage + 4x Resource = 3 RTT

# A DNS resource record has “cse.unsw.edu.au” for the name field and “dns.cse.unsw.edu.au” for the value field. The type field is likely to contain which of the following texts?

a. A  
b. CNAME  
c. MX  
**d. NS**  

> NS records indicate the authoritative servers for a domain

# An enterprise LAN that is connected to the Internet using a gateway. The average request rate from the enterprise browsers to the Internet origin servers is 15/sec and the average object size is 100 Kbits. If the gateway has a 1.5 Mbps access link, what is the traffic intensity at the access link?

a. 10%  
**b. 100%**  
c. 15%  
d. None of these  

> 15 requests a second * 100 Kbits = 1500 Kbits / second = 1.5 Mbps

# A UDP socket is uniquely identified by

a. a 2-tuple consisting of a destination IP address and a source port number  
**b. a 2-tuple consisting of a destination IP address and a destination port number**  
c. a 4-tuple consisting of a source IP address, a destination IP address, a source port number, and a destination port number  
d. a 2-tuple consisting of a source IP address and a destination port number

> I would argue it should be _a 2-tuple consisting of a **source** IP address and a **source** port number_

# A TCP socket is uniquely identified by

a. a 4-tuple consisting of a source IP checksum, a destination IP checksum, a source port number, and a destination port number  
b. None of these  
c. a 2-tuple consisting of a destination IP address and a destination port number  
**d. a 4-tuple consisting of a source IP address, a destination IP address, a source port number, and a destination port number**  

# UDP is better suited (compared to TCP) for which of the following applications?

a. Applications involving short query and responses, such as DNS  
**b. All of these**  
c. Video on demand  
d. Teleconferencing  

> All of the above choices would benefit from UDP's stateless and ACK-less protocol

# Which of the following statements is not true?

**a. It is not possible for an application to have reliable data transfer when using UDP**  
b. It is possible for an application to have reliable data transfer when using UDP  
c. Applications are expected to enjoy reliable data transfer when using TCP  
d. Both TCP and UDP uses checksum to detect bit errors  

> Application-level UDP reliability

# Host A sends a 256-byte TCP segment carrying a sequence number of 200 to Host B. Host B receives it correctly and sends an ACK to Host A. What is the acknowledgement number in the ACK?

a. 455  
b. 201  
**c. 456**
d. None of these

> ACK contains the next byte number ready to be received.  
> Host A sends 256 bytes (#200 to #255) to Host B

# Which of the following statements is true?

**a. With Fast Retransmit, TCP would retransmit after receiving three Duplicate ACKs**  
b. TCP would retransmit as soon as it receives a NAK.  
c. TCP would retransmit if it receives the same ACK twice.  
d. TCP would never retransmit unless there is a timeout.


# TCP uses flow control to ensure that the

a. Internet does not get congested  
b. sender’s buffer does not overflow  
**c. receiver’s buffer does not overflow**  
d. None of these  

# Two hosts located at two ends of a continent are trying to transfer data using a window-based (for pipelining purposes) reliable transport protocol. Suppose that the one-way propagation delay between the hosts is 15 millisec. If the hosts are using packets of length 1500 bytes over a 1 Gbps transmission link, how big the window size has to be for the channel utilization to be greater than 98%?

**a. Approximately 2,500 packets**  
b. Approximately 500 packets  
c. Approximately 20,000 packets  
d. Approximately 10,000 packets  

> L = 1500 bytes  
> R = 1 Gbps  
> d_prop = 15 ms = d/s  
> `window size = U * (R/L*RTT + 1) = 0.98 * (10^9/8 / 1500 * 2*0.015 + 1) = 2450.98`  

# What is the maximum size of a file that can be transmitted over a TCP connection without exhausting the TCP sequence numbers?

a. Approximately 100 MB  
**b. Approximately 4.2 GB**  
c. Approximately 4 MB  
d. Approximately 4.9 GB  

> The sequence number is 4 bytes long, so 4x 8 bits = 32 bits  
> 2^32 = 4294967296 bytes = 4 GB

# To speed up file transfers, a Go-back-N implementation uses a window size of 3. The sequence number field in the packet header must have at least

a. 4 bits  
b. 1 bit  
c. 3 bits  
**d. 2 bits**  

> For GBN - `window size < 2^m`  
> 3 </ 2^1  
> 3 < 2^2

# For a 8-bit sequence number field in the packet header, the maximum window size for Selective Repeat is

a. 256  
b. 32  
**c. 128**  
d. 64  

> For SR - `window size < 2^(m-1)  
> 2^(8-1) == 2^7 = 128  

# A TCP sender sets its retransmission timeout interval to 500 ms. If the estimated deviation of RTT from the estimated RTT is 10 ms, what was the value of estimated RTT?

a. 450 ms  
b. 400 ms  
**c. 460 ms**  
d. 490 ms  

> `eRTT = ?`  
> `devRTT = 10 ms`  
> `Timeout = 500ms`
>  
> `Timeout = eRTT + 4x devRTT`  
> `500ms = eRTT + 40ms`  
> `eRTT = 460ms`

# A TCP Sender maintains an EstimatedRTT of 100 ms and a DevRTT of x ms. What value of x would cause the timeout interval to remain unchanged (neither increase nor decrease) if the next SampleRTT is 108 ms?

a. 11  
b. 10  
c. 9  
**d. 8**  

> `eRTT = 100`  
> `devRTT = x`  
> `sampleRTT = 108`  
>  
> `new_eRTT = (0.875 * 100) + (0.125 * 108)`  
> `new_eRTT = 101ms`  
> `new_devRTT = (0.75 * x) + (0.25 * (108-101))`  
> `new_devRTT = 0.75x + 1.75`  
>  
> `old_timeout = 100 + 4x`  
> `new_timeout = 101 + 4 * new_devRTT`  
> `new_timeout = 101 + 4 * (0.75x + 1.75)`  
> `new_timeout = 108 + 3x`  
>  
> `old_timeout = new_timeout`  
> `100 + 4x = 108 + 3x`  
> `x = 8`  

# Which of the following statement is NOT true?

**a. To protect against SYN Flooding attack, a TCP receiver must create a connection state as soon as it receives a SYN packet.**  
b. TCP implements a 3-way handshake for establishing new connections  
c. At connection set up, TCP always negotiates an initial sequence number  
d. TCP can no longer send data after it has sent a FIN packet  
