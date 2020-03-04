---
title: "Switching"
date: 2020-02-19T16:51:54+11:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

# Circuit Switching

/logical/ channel - guaranteed bandwidth, guaranteed performance
dedicated

* Frequency Division Multiplexing
* Time Division Multiplexing

Time needed for Circuit Establishment.  
Time needed for Circuit Teardown

## Cons

* Inefficient
  * Modern resource requests are very intermittent.
  * Cannot be shared
* Fixed data rate
  * Even if no other user is using a shared circuit, you only have access to a division of it.
* Connection state maintenance
  * Communication state needs to be maintained (map overhead)

# Packet Switching

Data is sent as **packets** (chunks of formatted bits).  

Each packet has a **header** and a **payload**.

> In the OSI Network Layer, packets often contain packets from higher levels.

Switches "forward" packets depending on the contents of their headers. 

Switches have a negligible time for processing the packets.

## Cons

* Delay
* Latency

## Cut Through Switches

Switches that start transmitting as soon as the header has been processed

Unable to verify integrity of payload data.

## Store and Forward Switches

Switches that transmits their packets after it has been received entirely.

Able to verify the integrity of payload data

## Statistical Multiplexing

Relies on the assumption that not all flows burst at the same time.  
No determinalistic rate of transmittion.  

<!-- No link resources are reserved in advance.   -->

Consider three pieces of data being transmitted.  
Ideally, we would partition the bandwidth of the link into thirds, and assign each piece a third of the bandwidth.  

If three different blocks of data have transmision rates whose rate exceeds their allocated third of the bandwidth, we experience overloading.  

We address this with the concept of queueing and buffering.  
When two packets enter a switch at the same time, one of the packets is added into a queue. In time, the contents of that queue will be transmitted.

If there is persistent overload, packets will eventually be dropped.

### Statistical Multiplexing Gain

![](Screenshot from 2020-03-04 19-26-54.png)

F(k; n, p) = P(X <= k) = \Sum_(i=0)^floor(k) (n;i) p^i (1-p)^(n-i)

---

<!-- # Providing circuit-like behaviour whilst using packet switching -->

