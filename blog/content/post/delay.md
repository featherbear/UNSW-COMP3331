---
title: "Delay"
date: 2020-03-04T19:53:56+11:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

Too much delay == problem.  
Too much loss == problem.  

Queue overflow == loss.  

Q: Why don't we just have a larger buffer?  
A: Computation costs. If we need to perform operations on the buffer (searching, sorting), it will take longer.  
Larger queue == Larger average delay

---

Packets queue in router buffers.  
This occurs when packet arrival rates to link (temporarily) exceeed output link capacity

# Types of Packet Delay

## d_proc - Processing Delay

* Time it takes for the router/switch to process the packet

* Checking for bit errors
* Determine output link
* Typically < msec

AFFECTED BY PACKET SIZE

## d_queue - Queueing Delay

* Time it takes for the packet to leave the queue and be transmitted
* Depends on the congestion of the router

## d_trans - Transmission Delay

Time it takes to transmit the entire packet

_Data is transmitted in a serial fashion (one at a time)_

* `L` - packet length (bits)
* `R` - link bandwidth (bits per second)
* `d_trans` = `L/R`

AFFECTED BY PACKET SIZE

## d_prop - Propagation Delay

Time taken for a single bit to reach the destination.

* `d` - length of physical link
* `s` - propagation speed
* `d_prop` = `d/s`

# Queueing Behaviour

**Traffic Intensity = aL/R**  
`a` - packet arrival rate (packets/sec)  
`L` - packet length (bits)  
`R` - link bandwidth (bits/sec)


* Traffic intensity ~= 0 - Small queueing delay
* Traffic intensity == 1 (Burst) - L(N-1)/2R
* Traffic intensity == 1 (Continuous) -  0 (!!!?)
* Traffic intensity > 1 - Average queueing delay of infinity.

<!-- # End to End Delay -->

# Throughput

Throughput is the rate at which bits are transferred between sender/receiver.  
