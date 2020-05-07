---
title: "Quiz Questions"
date: 2020-05-06T12:26:52+10:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams:
  enable: false
  options: ""
---

# What is meant by the term statistical multiplexing?

Opposed to circuit switching - dedicated bandwidth per user; statistical multiplexing allows multiple users to utilise the same link, with proportioned bandwidths

[Read](../switching/#statistical-multiplexing)

# Consider two hosts, A and B, connected by a single link of rate R bps.

> Suppose that the two hosts are separated by m meters, and suppose the propagation speed along the link is s meters/sec.  
> Host A is to send a packet of size L bits to Host B.

## Express the propagation delay, d_prop in terms of m and s.

`d_prop = m / s`

_Remember: Only <u>processing delay</u> and <u>transmission delay</u> are affected by packet size_

[Read](../delay/#d-prop-propagation-delay)

## Determine the transmission time of the packet, d_trans in terms of L and R.

`d_trans = L / R`

## Ignoring the processing and queuing delays, obtain an expression for the end-to-end delay.

`delay = d_prop + d_trans`  
`delay = m/s + L/R`

## Suppose Host A begins to transmit the packet at time t=0. At time t=dtrans, where is the last bit of the packet?

About to leave Host A.

_Remember: The transmission delay is the time it takes for the device to push it onto the link_

## Suppose d_prop is greater than d_trans. At time t=d_trans, where is the first bit of the packet?

Somewhere on the link

## Suppose d_prop is less than d_trans. At time t=d_trans, where is the first bit of the packet?

At host B

# It takes a single bit ten times longer to propagate over a 10Mb/s link than over a 100Mb/s link. True or False?

Propagation -> `d_prop = m/s`.  
Megabits/s is a measure of bandwidth; so the propagation speed is not affected.

Hence False

# Suppose users share a 1Mbps link. Also suppose each user requires 100 Kbps when transmitting, but each user transmits only 10 percent of the time.

## When circuit switching is used, how many users can be supported?

10 users can be supported, by partitioning the bandwidth into ten 100 Kbps links

## Suppose packet switching is used for the rest of the problem. Find the probability that a given user is transmitting.

Statistically from the question: "10 percent of the time".

`p = 0.1`

## Suppose there are 40 users. Find the probability that at any given time, exactly n users are transmitting simultaneously.

> Note: You should simply express this as an expression rather than computing the exact probability value

Binomial probability: `40Cn * 0.1^n * 0.9^(40-n)`

# Suppose there is exactly one packet switch between a sending host and the receiving host...

> Assume that the transmission speed of the links between the sending host and the switch and the switch and the receiving host are R1 and R2 respectively.  
> Assuming that the switch uses store-and-forward packet switching, what is the total end-to-end delay to send a packet of length L?  
> Ignore queuing, propagation and processing delays.

`d_trans_1 = L/R1`  
`d_trans_2 = L/R2`

`d_lay (hahahahaha...) = L/R1 + L/R2`

# Consider sending a large file of F bits from Host A to Host B.

> There are two links (and one router) between A and B, and the links are uncongested (that is, no queuing delays). Host A segments the file into segments of S bits each and adds 40 bits of header to each segment, forming packets of L=40+S bits. Each link has a transmission rate of R bps. Find the value of S that minimizes the delay of moving the file from Host to Host B. Disregard propagation delay.

A -> Router -> B

- `L = 40+S`
- Time for packets to arrive = `L/R * (F/S + 1)`

- First packet takes `2*L/R` to arrive (over two links)
- Each packet then arrives `L/R` time after

- Derivative (dS) --> `S = sqrt(40*F)`

# End-to-End Arguments in System Design

> This question is centered around the fundamental paper "End-to-end Arguments in System Design" which is available [here](http://web.mit.edu/Saltzer/www/publications/endtoend/endtoend.pdf) - Saltzer

> Consider that we wish to implement a reliable file transfer protocol.  
> A. One approach is to make each step of the file transfer reliable and string them together to make the end-to-end process reliable.
>
> B. The other approach is to not worry about implementing reliability along each step but rather to make use of an end-to-end check (simple error detection at the receiver followed by feedback to the sender) and retransmit if necessary.
>
> Which approach would you pick and why?

For a **reliable file transfer protocol**, where all packets must arrive correctly, Approach A would be better, as to the application, only valid data needs to be parsed and processed on. However, there will be more work for the OS kernel, which may delay the operation and activities of other tasks.

Approach B would be good for a more universal protocol, where applications have the choice to discard or attempt to correct or use the imperfect packets.

# Consider the figure below for which there is an institutional network connected to the Internet

> Suppose that the average object size is 900,000 bits and that that the average request rate from the institution’s browsers to the origin server is 1.5 requests per second.  
> Suppose that the amount of time it takes from when the router on the Internet side of the access link forwards an HTTP request until it receives the response in two seconds on average.  
> Model the total average response time as the sum of the average access delay and the average Internet delay.  
> For the average access delay, use `A/(1-AB)` where A is the average time required to send an object over the access link and B is the arrival rate of objects to the access link.  
> You can assume that the HTTP request messages are negligibly small and thus create no traffic on the network or the access link.

![](cache.png)


`B = 1.5 requests/second`  
Average of 900000*1.5 = 1350000 bits per second being transferred

`delay_response = delay_access + delay_internet`  
`delay_access = A/(1-AB) = L/R / (1 - BL/R)`  
`delay_internet = 2 seconds`

## Find the total average response time?

...

## Now suppose a cache is installed in the institutional LAN. Suppose the cache hit rate is 0.4. Find the total response time.

`delay_response = 0.4 * tc + 0.6 * (delay_access + delay_internet)`  

Where `tc` is a negligible time for the cache to be hit and return a response

# Among the following, in which case would you get the greatest improvement in performance with persistence HTTP as compared to non-persistence HTTP? 

**a) Low throughput network paths (irrespective of distance)**  
b) High throughput network paths (irrespective of distance)  
c) Long distance network paths (irrespective of throughput)  
d) High throughput, short-distance network paths  
e) High throughput, long-distance network paths

> The longer the distance, the longer a connection will take to establish.  
> The smaller the throughput, the more connections would need to be created.  


# DNS Delays

> Suppose within your Web browser you click on a link to obtain a web page.  
> The IP address for the associated URL is not cached in your local host, so a DNS lookup is necessary to obtain the IP address.  
> Suppose that `n` DNS servers are visited before your host receives the IP address from DNS and that iterative queries are used.  
> Let the successive visits to the DNS servers incur an RTT of RTT1, ..., RTTn.  
> Further suppose that the webpage associated with the link contains exactly one object, consisting of a small amount of HTML text.  
> Let RTT0 denote the RTT between the local host and the server containing the object.  
> Assuming zero transmission time of the object, how much time elapses from when the client clicks on the link until the client receives the object?

Given that the client does not have the entry cached, and that there is no local DNS cache.

Best Case scenario - The first DNS server has the entry.  
Time = (Query to DNS server 1 + Answer) + TCP Connection Setup + Request = RTT1 + 2x RTT0

Worst Case Scenario - The last DNS server has the entry.  
Time = (Query to DNS server 1 + Answer) + (Query to DNS server 2 + Answer) + ... + (Query to DNS server n + Answer) + TCP Connection Setup + Request = RTT1 + RTT2 + ... + RTTn + 2x RTT0


---

# Week One

## Q1. Packet switching, instead of circuit switching, is generally used to transfer data in the Internet.

**True** or False?

## Q2. Propagation delay depends on the size of the packet.

True or **False**?

## Q3. Which of the following delays is significantly affected by the load in the network?

A. Processing delay  
**B. Queuing delay**  
C. Transmission delay  
D. Propagation delay  

> A packet can only transmit if the network has capacity to carry the packet, otherwise it will wait.

## Q4. Consider a packet that has just arrived at a router. What is the correct order of the delays encountered by the packet until it reaches the next-hop router?

A. Transmission, processing, propagation, queuing  
B. Propagation, processing, transmission, queuing  
**C. Processing, queuing, transmission, propagation**  
D. Queuing, processing, propagation, transmission  

> Process -> Queue -> Transmit -> Propagate

## Q5. As an application developer, what measure would you take to reduce the total delay involved in transferring image files across the Internet?  

_Hint: You do not have control on the core of the network i.e., route taken, bandwidth etc._  

Image compression and encoding

## Q6. Is it possible to increase the upstream data rate while using ADSL? If yes how? 

Yes, allocate more bandwidth to the upstream

# Week 2

## Q1. In the Internet, which layer has only one choice of protocol

A. Physical  
**B. Network**  
C. Transport  
D. Application  

> For Internet usage, the Ethernet protocol is the only allowed network protocol.

## Q2. Which layer is NOT implemented in Internet routers

A. Physical  
B. Data link  
C. Network  
**D. Transport**  

## Q3. Do a quick search on the Internet on "firewall" (some information about firewall is also available in your text on page 376, 7th Ed., for example). Why do you think that firewall violates the layering principle?

It looks at the type of Transport and Application layer protocol.  
i.e. Deep Packet Inspection (DPI)

## Q4. Find about about "TCP Splitting" from the Internet. Your text also contains some information about TCP Splitting on page 303, 7th Ed., for example. What is the motivation for TCP Splitting to break the layering principle?

> Extra TCP connections are made between hops, in hopes to achieve lower RTTs.

A. Security  
B. Performance in terms of reducing the packet header size  
**C. Performance in terms of reducing the end-to-end delay**  
D. Performance in terms of reducing the queueing delay in the routers  

## Q5. Network applications run on

A. network core devices, such as routers and switches  
**B. end hosts, such as smartphones and desktops**  
C. access routers or gateways, such as wireless routers  
D. all of the above  

> "Software routers" that have network applications, are considered to be end-hosts themselves when viewed for their applications.  
> But then there's DPI inspection ... which we don't include in the scope of this course

## Q6. If two processes on the same machine want to communicate with each other, they 

A. must send messages to each other  
**B. do not have to send messages to each other, but can simply share some common memory space within the same machine**  
C. must use TCP  
D. could use FTP  

> IPC!

## Q7. The client process must use a well-known port number for its socket.  

True or **False**?

> Ports are arbitrary, however some ports are commonly used as a standard.

## Q8. Client-Server architecture can only be implemented with TCP at the transport layer.

True or **False**?

## Q9. HTTP belongs to

A. Transport layer  
**B. Application layer**  
C. Network layer  
D. Physical layer  

# Q10. To send the number 256, HTTP will consume  

A. 1 byte  
B. 2 bytes  
**C. 3 bytes**  
D. 4 bytes  

> HTTP sends all data as ASCII -> hence 256 is sent as `32` `35` `36`.

## Q11. We could achieve some of the things achieved with cookies today if HTTP was 'stateful' (i.e., NOT stateless)

**True** or False?

## Q12. If SMTP only allows 7-bit ASCII, how do we send pictures/videos/files via email?

A. We use a different protocol instead of SMTP  
**B. We encode these objects as 7-bit ASCII**  
C. We’re really sending links to the objects, rather than the objects themselves  
D. We don't!! You have been lied to!! :) 

## Q13. Which of the following is NOT true?

A. HTTP is pull-based, SMTP is push-based  
B. HTTP uses a separate header for each object, SMTP uses a multipart message format  
C. SMTP uses persistent connections  
**D. HTTP uses client-server communication but SMTP does not**  

# Week 3

## Q1. If a local name server has no clue about where to find the address for a hostname then

A. Server asks its adjacent name server  
**B. Server asks its root name server**  
C. Request is not processed  
D. Server explodes  

## Q2. Which of the following is an example of a Top Level Domain?

A. yoda.jedi.starwars.com  
B. jedi.starwars.com  
C. starwars.com  
**D. .com**  

## Q3. A web browser needs to contact www.cse.unsw.edu.au. The minimum number of DNS requests sent is:

**A. 0**  
B. 1  
C. 2  
D. 3  

> Caching!

## Q4. The role of the CDN provider’s authoritative DNS name server in a content distribution network basically is

A. to provide an alias address for each browser access to the "origin server" of a CDN website  
**B. to map the query for each CDN object to the CDN server closest to the requestor (browser)**  
C. to provide a mechanism for CDN “origin servers” to provide paths for clients (browsers)  
D. none of the above, CDN networks do not use DNS  

## Q5. When web-based email is used, two mail servers communicate with each other using HTTP.

True or **False**?

## Q6. P2P networks must have servers to help new peers find other peers.

True or **False**?

> Not a necessity, consider circular DHT where a peer is known.

## Q7. P2P networks must maintain trackers to help new peers join the network.

True or **False**?

> Not a necessity, consider circular DHT where a peer is known.

## Q8. The 'rarest first' is a P2P networking policy to select

A. the next peer to download chunks from  
**B. the next chunk to download**  
C. the tracker to query for other peers  
D. the file to download  

## Q9. The 'rarest first' policy helps

A. download precious files  
B. download chunks that no other peers have  
**C. duplicate chunks in the P2P network so even if a peer disappears, other peers will contain the chunks**  
D. remove chunks from the network that are rarely used  

## Q10. In BitTorrent, Peer A will never send chunks to Peer B if Peer B is not in Peer A's top 4 list.

True or **False**?

## Q11. In DHT, a hash function converts

A. an integer to a real number  
B. an a real number to an integer  
C. an integer to a string  
**D. a string to an integer**  

## Q12. Which of the following will help address the 'peer churn' (i.e. a peer disappearing) problem?

A. each peer knows its two immediate predecessors  
B. each peer knows its two immediate successors  
C. each peer knows its immediate successor and two immediate predecessors  
**D. each peer knows its immediate predecessor and two immediate successors**  

> ehh

# Week 4

## Q1. A transport layer protocol implements timer to address the loss problem. The timer cannot expire if there is no loss.

True or **False**?

> Packets may not be delivered in time due to network congestion

## Q2. A reliable transport protocol must implement both ACK and NAK if it wants to address bit errors as well as packet loss problems.

True or **False**?

## Q3. Stop-and-Wait

A. receiver buffers packets  
**B. has only 1 bit for the sequence number**  
C. requires a large sequence number space  
D. requires more than 1 bit for the sequence number  

## Q4. Stop-and-Wait cannot provide reliability.

True or **False**?

## Q5. For short distances, Stop-and-Wait is always efficient, but it fails to support high throughput only when the distance between the client and server is large.

True or **False**?

## Q6. Pipelining increases throughput (compared to stop-and-wait) linearly with the window size (number packets the sender can have in the pipeline without having to stop and wait for the ACK).  

**True** or False?

## Q7. In Go-Back-N, the sender window cannot be equal to the sequence number space.  

**True** or False?

> `size < 2^m`

## Q8. For a 4-bit sequence number field in the packet header, the maximum possible window size for Selective Repeat is

A. 15  
B. 16  
**C. 8**  
D. 7  

> `size <= 2^(m-1)`

## Q9. To speed up file transfers, a Selective Repeat implementation is using a window size of 8. The sequence number field in the packet header must be at least

A. 8-bit long  
**B. 4-bit long**  
C. 3-bit long  
D. 16-bit long  

> `size <= 2^(m-1)`  
> `8 == 2^3 == 2^(4-1)

# Week 5

## Q1. TCP receiver may intentionally delay the acknowledgement of a correctly received packet.

**True** or False?

## Q2. A TCP receiver receives an in-order segment with expected sequence number, but it has one other segment with pending ACK. Which of the following is a possible action for this receiver if it is using the delayed ACK mechanism?

A. It sends 2 ACKs one after the other  
B. It sends 3 ACKs one after the other  
**C. It sends one cumulative ACK acknowledging both segments**  
D. It sends a Duplicate ACK.  

> Wording abit off. Translation: It has transmitted an ACK that has not been received by the sender; so the receiver can send a cumulative ACK to account for both ACKs

## Q3. TCP is never allowed to retransmit unless there is a timeout.  

True or **False**?

> Fast Retransmit

## Q4. During slow start, congestion window increases:

A. Linearly  
**B. Exponentially**  
C. Logarithmically  
D. Does not grow  

## Q5. Maximum segment size (MSS) refers to the number of bytes in a TCP segment including its header.  

True or **False**?

## Q6. A TCP connection is using an MSS=1460 bytes. At the start of slow start, how many bytes the TCP sender can transmit without having to wait for ACK?

A. 1400  
**B. 1460**  
C. 1500  
D. 3000  

## Q7. A TCP sender could still reduce its window size even if there was no triple duplicate ACK or timeout.  

**True** or False?

> Receiver buffer may be full, so the receiver window in the ACK has a low value

# Week 6

## Q1. If a TCP implementation decided to halve its congestion window when it received triple duplicate ACK, it was a Tahoe implementation.

True or **False**?

> TCP Tahoe sets the congestion window to 1 for timeouts and triple duplicate ACKs.

## Q2. If a TCP implementation decided to reduce its congestion window to 1 MSS when it received triple duplicate ACK, it was definitely a Tahoe implementation.  

True or **False**?  

> Answers say True, but a TCP Reno implementation with its congestion window set to 2 MSS would set its congestion window to 2/2 = 1 MSS on a triple duplicate ACK as well...

## Q3. If a TCP implementation decided to reduce its congestion window to 1 MSS when it experienced a time out, it could be either a Tahoe or Reno (we cannot tell).

**True** or False?

> Both TCP Reno and Tahoe set its cwnd to 1 during a timeout

## Q4. A TCP Reno would halve its congestion window upon receiving a triple duplicate ACK.

**True** or False?

## <s>Q5. A TCP New-Reno would halve its congestion window upon receiving a triple duplicate ACK.</s>

<s>True or **False**?</s>

## Q6. TCP sets a very large value for ssthresh each time it switches to slow start.

True or **False**?

## Q7. A router performs routing when a data packet arrives.  

True or **False**?

> Ehh

## Q8. A router performs forwarding when a packet arrives.

**True** or False?

> Ehh

## Q9. To perform forwarding, a router needs to perform routing first.

**True** or False?

> Ehh

# Week 7

## Q1. To perform forwarding, a router must inspect the source address in the arriving packet's header.  

True or **False**?

> Only the destination address needs to be known

## Q2. IP packet fragmentation

A. helps speed up data delivery in the Internet  
B. cannot be avoided  
**C. can be avoided by controlling TCP segment size based on path MTU discovery**  
D. can be avoided by configuring the maximum transfer unit (MTU) of the underlying link layer.  

## Q3. Each network interface of a host must be configured with an IP address.  

**True** or False?

## Q4. Two hosts connected to the same subnet can reach each other without the help of a router.

**True** or False?

## Q5. In the original "classful" addressing scheme, the network address part of the 32-bit IP address could have a maximum of

A. 8 bits  
B. 10 bits  
C. 16 bits  
**D. 24 bits**  

## Q6. In today's CIDR addressing scheme, the subnet part of the 32-bit IP address

A. can only have 24 bits  
B. must be at least 8 bits long  
C. can have maximum length of 28 bits  
**D. can have any arbitrary length (<= 32 bit)**  

## Q7. CIDR addressing scheme could work without the help of subnet masks.

True or **False**?

> Subnet masks are required to define the layout of the network

## Q8. How many IP addresses belong to the subnet 128.119.254.0/26?

A. 16  
B. 32  
**C. 64**  
D. 128  

> 2^(32-26) == 2^6

## Q9. What are the IP addresses at the two end-points of the subnet 128.119.254.0/26?

**A. 128.119.254.0 and 128.119.254.63**  
B. 128.119.254.0 and 128.119.254.128  
C. 128.119.254.63 and 128.119.254.128  
D. 128.119.254.0 and 128.119.254.64  

## Q10. Without DHCP, a host cannot be configured with an IP address.

True or **False**?

> Static IP!

## Q11. From IP address, one can guess the geographic location of the device.  

**True** or False?

> Yes for WAN IPs

## Q12. The two subnets 128.119.245.128/25 and 128.119.245.0/26 have overlapping IP addresses.  

True or **False**?

## Q13. One of the advantages of NAT is that the organisation can change addresses of the devices within its local network without notifying the outside world.

**True** or False?

## Q14. NAT violates layering principle.  

**True** or False?

> NAT looks at the TCP headers, even though it is in the network layer

## Q15. For NAT to work, we need at least two public IP addresses.

<s>True or False?</s>

> What? On the host, for both networks???

# Week 8

## Q1. A domain is only run by a single administrator.

**True** or False?

> One administrative entity

## Q2. A Border Router is connected to more than one ISP.  

**True** or False?

## Q3. Each ISP must run intra-domain routing protocols to route packets within its domain.  

**True** or False?

> i.e RIP protocol

## Q4. In graph abstraction of communication networks, edges represent routers.  

True or **False**?

> Edges represent links

## Q5. In graph representation of communication networks, all links must have identical costs/weights. 

True or **False**?

## Q6. Shortest path represents the path with minimum number of hops:

**A. when all links have equal cost**  
B. in any communication networks  
C. when each hop has at least 1 ms of delay at minimum  
D. when most hops are heavily loaded  

# Q7. In link state routing, routers must flood the network with any changes in its links.  

**True** or False?

## Q8. Distance Vector scales better than Link State because it generally exchanges smaller size update packets with its neighbours.

True or **False**?

> Distance Vector packets are actually larger, but are transmitted less frequently

## Q9. With Distance Vector routing, each router must have the knowledge of the complete network topology.

True or **False**?

## Q10. For a network with 10 routers, the loop in Dijkstra's algorithm will be executed:

A. only once  
B. 9 times  
**C. 10 times**  
D. 11 times  

# Week 9

## Q1. LAN address is also known as:

A. TCP address  
B. IP address  
**C. MAC address**  
D. Virtual address  

## Q2. LAN address is usually written in:

**A. Hexadecimal notation**  
B. Binary notation  
C. Decimal notation  
D. in words  

## Q3. ARP is used to resolve:

A. the IP address of a domain name  
B. the next hop address for an arriving packet  
**C. the associated LAN address of an IP address**  
D. the associated IP address of a LAN address  

## Q4. A network admin is needed to configure an ARP table.  

True or **False**?

> ARP tables are constructed automatically, and dynamically

## Q5. Which of the following is an example of link layer protocol?

A. RIP  
B. OSPF  
**C. Ethernet**  
D. TCP  

## Q6. One of the advantages of using bus-based Ethernet is that collisions can be completely avoided.

True or **False**?

> Bus-based Ethernet _causes_ collisions as all devices must use the same bus/link

## Q7. Switching tables in LAN switches are typically configured by network admin.  

True or **False**?

## Q8. In a LAN switch, packets

A. are never flooded  
B. are always flooded  
**C. can be flooded sometimes**  
D. are flooded only when reliable service is required  

## Q9. If a LAN switch has flooded a packet, it means the switch did not know which LAN segment the packet came from.  

True or **False**?

> The switch will know where the packet came from.

## Q10. If a LAN switch has flooded a packet, it means the switch did not know which LAN segment the packet destination is connected to.  

True or **False**?

> Answers say True, but - a switch can flood if the packet is a broadcast packet, if it is functioning as a hub, or if it does not have a valid route
