---
title: "Quiz Questions"
date: 2020-05-05T17:26:52+10:00

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
Host A is to send a packet of size L bits to Host B.

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

* `L = 40+S`
* Time for packets to arrive = `L/R * (F/S + 1)`

* First packet takes `2*L/R` to arrive (over two links)
* Each packet then arrives `L/R` time after

* Derivative (dS) --> `S = sqrt(40*F)`