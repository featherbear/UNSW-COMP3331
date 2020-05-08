---
title: "Harmony"
date: 2020-05-08T10:03:13+10:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

Harmony  
  
Audio used alongside WiFi to solve contention  
40% gain in throughput; 27% for dense networks  
Limitations of audio - frequency, penetration  
Software based  
  
1) Contention resolution over acoustic channel  
2) Data transmission over wifi  
  
Random Tone is generated - lowest tone first, while also listen  
Contention resolution  
Wait for DIFS  
Transmit / Wait  
Then repeat simultaneously  
  
Losers subtract their RNG number by the winner   
  
Shared flag to lock and unlock  
  
# Single Acoustic Domain  
  
16 - 21 kHz  
  
Reasons:   
  
Majority of background noises go up to 12 KHz  
Smart devices have high acoustic sensitivity, can capture up to 21 KHz  
  
# Propagation Delay  
  
Takes a while to decide who wins.  
Allow multiple packets to be sent  
  
Also decide the order of the next few senders  
  
Round-robin - parallel  
  
* WAIT FOR DIFS -> Waits for given period of silence  
  
# Collision  
  
Same acoustic tone, tone number  
  
* double round  
  
- length  
- tone  
  
* Mechanical artifacting from sudden speaker movement  
  
Amplitude fade-in and fade-out, 5 milliseconds  
  
Increase frequency set  
gaps between frequency tone - 200 Hz gaps  
26 frequencies  
  
double round if collision occurs!! -------------- 26 devices isn't that much though  
  
---  
  
Kernel space  
  
A-PHY - DMA; generateTone()  
A-MAC - Get tone number, run Harmony, get rank, DIFS  
  
20 meter Harmony pax  
  
Transition  
Hidden nodes  
  
  