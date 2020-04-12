---
title: "Lab 06 - Throughput, IP Fragmentation and Routing"
date: 2020-04-12T21:18:52+10:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

# Exercise 1: Setting up NS2 simulation for measuring TCP throughput

* File: [exercise2.tcl](./exercise2.tcl)
* File: [throughput.plot](./throughput.plot)

![](Picture1.png)

* FTP/TCP Source n0 -> TCP Sink n5 : start time: 0.5 sec End time: 8.5 sec
* FTP/TCP Source n3 -> TCP Sink n5 : start time: 2.0 sec End time: 9.5 sec
* FTP/TCP Source n7 -> TCP Sink n0 : start time: 3.0 sec End time: 9.5 sec
* FTP/TCP Source n7 -> TCP Sink n3 : start time: 4.0 sec End time: 7.0 sec 

|nam|gnuplot|
|:---:|:---:|
|![](Screenshot from 2020-04-12 23-41-57.png)|![](Screenshot from 2020-04-12 23-50-52.png)|


## Why is the throughput achieved by flow tcp2 higher than tcp1 between time span 6 sec to 8 sec?

![](Screenshot from 2020-04-13 00-04-06.png)
_Visualisation of traffic at 6-8s_

* TCP1 flows from 0-1, 1-2, 2-4, 4-5
* TCP2 flows from 3-2, 2-4, 4-5
* TCP3 flows from 7-6, 6-1, 1-0
* TCP4 flows from 7-6, 6-1, 1-2, 2-3

***<u>NOTE: I am only considering the 2.5Mbps links as there are no issues on the 10Mbps links...</u>***

At the time span from 6 to 8 seconds, TCP1 must share the link bandwidth of 1-2 with TCP4
It must also share the link bandwidth of 2-4 with TCP2

At the time span from 6 to 8 seconds, TCP2 only needs to share the link bandwidth of 2-4 with TCP1.

* The RTT for TCP1 is `2 x (10 + 40 + 40 + 10) = 200ms`  
* The RTT for TCP2 is `2 x (10 + 40 + 10) = 120ms`  

As RTT2 has a lower RTT, it is allocated a higher portion of the bandwidth, hence the throughput achieved by flow TCP2 is higher

## Why is the throughput for flow tcp1 fluctuating between time span 0.5 sec to 2 sec?

At the time span from 0.5 to 2 seconds, flow TCP1 is performing the TCP Slow Start mechanism to check the available bandwidth

## Why is the maximum throughput achieved by any one flow capped at around 1.5Mbps? 

The maximum throughput is the capacity of the smallest link - in this case 2.5Mbps.  
As TCP1 performs a Slow Slart algorithm, by the time it reaches a window of 1.5Mbps, TCP2 starts its activity; which prevents TCP1 from acquiring any further bandwidth.

Hence flow TCP1, and the other flows will never be able to utilise 2.5Mbps on their own, and are capped at 1.5Mbps

# Exercise 2: Understanding IP Fragmentation

File: [ip_frag.pcapng](./ip_frag.pcapng)

## Which data size has caused fragmentation and why?

![](Screenshot from 2020-04-13 00-32-41.png)

The data size of 2000 bytes (and consequently 3000 bytes) has caused fragmentation, as the default MTU for an Ethernet frame is 1500 bytes.  
As the packet was larger than the MTU, it was split up.

### Which host/router has fragmented the original datagram?

The source (`192.168.1.103`) fragmented the original datagram.

### How many fragments have been created when data size is specified as 2000?

`2 fragments` were created for each ping with data sizes of 2000 bytes.  

For example, packet 16 and packet 17.  
Whilst only packet 16 says "Fragmented IP Protocol", packet 17 is the other fragment, which gets combined.  

## Did the reply from the destination 8.8.8.8. for 3500-byte data size also get fragmented? Why or why not?

Yes, the reply for the ping of 3500 byte data size was also fragmented (into 3), as all packets must adhere to the Ethernet MTU of 1500 bytes.

i.e. packets 42, 43 and 44

## Give the ID, length, flag and offset values for all the fragments of the first packet sent by 192.168.1.103 with data size of 3500 bytes?

![](Screenshot from 2020-04-13 00-47-07.png)

***<u>NOTE: Length is given by the payload length (ICMP data)</u>***

|Packet Number|`ip.id`|IP Length|Payload Length|Flag|Offset|
|:---:|:---:|:---:|:---:|:---:|:---:|
|39|0x7a7b|1500|1480|More Fragments|Fragment offset 0|
|40|0x7a7b|1500|1480|More Fragments|Fragment offset 185|
|41|0x7a7b|568|548|-|Fragment offset 370|

## Has fragmentation of fragments occurred when data of size 3500 bytes has been used? Why and why not?

No, fragments were not re-fragmented.  

It is the sender's responsibility to split the original packet into the right fragment sizes that are at most 1500 bytes long.  
Therefore fragments will not be refragmented

## What will happen if for our example one fragment of the original datagram from 192.168.1.103 is lost? 

If one fragment is lost, all fragments will need to be retransmitted.

<!-- "If any fragment of a packet is lost, the reassembly will timeout and the entire set of fragments needs to be sent again. Timeouts vary, 15 seconds is suggested to start with."

http://users.cis.fiu.edu/~vince/cgs4285/class13.html -->

# Exercise 3: Understanding the Impact of Network Dynamics on Routing 

File: [tp_routing-step1.tcl](./tp_routing-step1.tcl)  
File: [tp_routing-step2.tcl](./tp_routing-step2.tcl)  
File: [tp_routing-step3.tcl](./tp_routing-step3.tcl)  
File: [tp_routing-step4.tcl](./tp_routing-step4.tcl)  
File: [tp_routing-step5.tcl](./tp_routing-step5.tcl)  

![](Screen_Shot_2016-09-06_at_5.43.33_PM.png)

## Which nodes communicate with which other nodes? Which route do the packets follow? Does it change over time? 

* Node 0 communicates with Node 5 via 0-1-4-5
* Node 2 communicates with Node 5 via 2-3-5

The route doesn't change over the duration of the simulation

## What happens at time 1.0 and at time 1.2? Does the route between the communicating nodes change as a result of that?  

At time 1.0s, the link 1-4 is disabled - the data coming from node 0 is lost, as the data is not rerouted nor retransmitted.  

At time 1.2s, the link 1-4 is enabled - the data coming from node 0 is passed along to node 4 and then to node 5.  

Node 2's communication to Node 5 remains unaffected throughout the simulation

## Did you observe any additional traffic when rtproto was set to DV? How does the network react to the changes that take place at time 1.0 and time 1.2 now? 

> As the simulation starts, node 0 sends out some data to node 1.  
A short while after node 2 sends out some data to node 1 and node 3.  
&nbsp;  
Nodes 1 then transmits some data to nodes 0 and 4,  
and node 3 transmits some data to node 5 and 2.
&nbsp;  
Each node then transmits some data along each of its links.

This occurs frequently.

At time 1.0s, when link 1-4 is disabled, this behaviour is also seen.  
The network reacts by rerouting the packets from 0-1-4-5 to 0-1-2-3-5.  

At time 1.2s, link 1-4 is enabled, and routes the packets from node 0 back to the original path of 0-1-4-5.

## When the cost of link 1-4 is set to 3, how does this change affect the routing? Explain why. 

All of the packets sent from node 0 are no longer routed through node 4, but instead follow the path 0-1-2-3-5.  
This is because node 1 has decided that it is cheaper to get to node 5 via 1-2-3-5 (cost = 3), rather than 1-4-5 (cost = 4).

## When the cost of link 1-4 is set to 2, and link 3-5 is set to 3, describe what happens and deduce the effect of `Node set multiPath_ 1`

Data from node 0 travels to node 5 via the route 0-1-4-5.  
Data from node 2 travels to node 5 via alternating routes 2-3-5 (first), then 2-1-4-5.

* When the cost of link 1-4 is 2; route 2-1-4-5 will have a cost of 4.  
* When the cost of link 3-5 is 3; route 2-3-5 will have the same cost of 4.

The `Node set multiPath_ 1` option allows nodes to load balance their traffic unto multiple routes, such as what node 2 is doing.
