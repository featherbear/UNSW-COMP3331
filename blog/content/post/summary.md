---
title: "Summary"
date: 2020-05-05T17:25:15+10:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

# [CRC](../crc)

Bitwise XOR the data bits with the generator bit.  
Remainder should be 0, for a successful transmission.  

# Window Size

## [Go Back N](../transport-layer/#go-back-n)

* Receiver Window Size = 1
* Sender Window Size < 2^m

## [Selective Repeat](../transport-layer/#selective-repeat)

* Receiver Window Size <= 2^(m-1)
* Sender Window Size <= 2^(m-1)

# [Channel Utilisation (RDT)](../transport-layer/#pipelining)

## Without Pipelining

`U_sender = L/R / (RTT + L/R)`

## With Pipelining

`U_sender = nL/R / (RTT + L/R)`  

To calculate window size: `window size = U * (R/L*RTT + 1)`