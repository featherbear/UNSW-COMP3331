---
title: "Lab 05 - TCP Congestion Control and Fairness"
date: 2020-04-05T18:36:40+10:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

# Exercise 0: Revision of TCP Congestion Control

![](tcp_cc.jpg)

## Name the loss events that occur at 1 and 2. Explain why the congestion window is changed differently in those two cases.  

At 1: Duplicate ACK received - Window halved - Improves throughput  
At 2: Timeout - Try again from start

## What phase of the TCP congestion control algorithm coincides with the circled segment marked by 3 and 4?  

At 3: Slow Start (exponential increase)  
At 4: AIMD (linear increase)

## Why is the congestion window increased more rapidly at 3 than at 4?

(3) increases at an exponential rate.

## What happens to the window after 2?

The slow start algorithm starts again

# Exercise 1: Understanding TCP Congestion Control using ns-2

**Using TCP Tahoe...**

File: [tpWindow.tcl](tpWindow.tcl)  
Usage: `ns tpWindow.tcl <max_cwnd> <link_delay>`

File: [Window.plot](Window.plot)  
Usage: `gnuplot Window.plot`

> Run the script with the max initial window size set to 150 packets and the delay set to 100ms (be sure to type "ms" after 100).  
In other words, type the following: `ns tpWindow.tcl 150 100ms`
&nbsp;  
> Then plot it with `gnuplot Window.plot`

![](Screenshot from 2020-04-05 18-59-23.png)

## What is the maximum size of the congestion window that the TCP flow reaches in this case?

The maximum size is `100`.

## What does the TCP flow do when the congestion window reaches this value? Why? What happens next?

When the congestion window reaches 100, the congestion window is set back to zero and the threshold is halved to 50 - the initial value where the TCP phase changes from a slow start algorithm to the AIMD (additive-increase / multiplicative-decrease) algorithm; so that the connection is kept in the congestion avoidance phase after a loss event.  

After the congestion window size is set to zero, it begins to increase again (Slow Start) until it reaches 50; where the algorithm changes to AIMD.  

## Calculate the average throughput (in packets/sec and bps)  

File: [WindowTPut.plot](WindowTPut.plot)  
Usage: `gnuplot WindowTPut.plot`

![](Screenshot from 2020-04-05 19-17-22.png)

The average throughput is around `185 packets per second`.  

Average throughput (bps) = `185 * (500 + 20 + 20) * 8 = 799200 bps` 

## Rerun the above script, each time with different values for the max congestion window size but the same RTT (i.e. 100ms).

> Find the value of the maximum congestion window at which TCP stops oscillating (i.e., does not move up and down again) to reach a stable behaviour.  

|150|100|60|51|**50**|49|40|
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
|![](Screenshot from 2020-04-05 19-33-59.png)|![](Screenshot from 2020-04-05 19-50-08.png)|![](Screenshot from 2020-04-05 19-30-07.png)|![](Screenshot from 2020-04-05 19-24-31.png)|![](Screenshot from 2020-04-05 19-25-20.png)|![](Screenshot from 2020-04-05 19-25-06.png)|![](Screenshot from 2020-04-05 19-29-50.png)|

The maximum stable congestion window size is `50`.

### How does TCP respond to the variation of this parameter?

Increasing the congestion window size past 100 results in no change to the graph, hence we can assume there are negligible effects to what happens to the connection.

As the congestion window size decreases, less packet loss is experiences, and at a window size of 50, no packet loss occurs, and TCP stops oscillating.

### What is the average throughput (in packets and bps) at this point?

At a congestion window size of 50, the average throughput is around `225 packets per second`, or `225 * (500 + 20 + 20) * 8 = 972000 bps`

### How does the actual average throughput compare to the link capacity (1Mbps)?  

At the average throughput rate at a window size of 50, the link is 97.2% utilised

# Exercise 1b: Using TCP Reno

> Create a congestion window graph and throughput graph for TCP Reno, using a max window size of 150, and delay of 150ms.  

![](Screenshot from 2020-04-05 19-51-04.png)

![](Screenshot from 2020-04-05 19-51-49.png)

## What is the maximum size of the congestion window that the TCP flow reaches in this case?

100

## What does the TCP flow do when the congestion window reaches this value? Why? What happens next?

The window size is decreased to half, but not zero (TCP Reno only goes to zero when there is a timeout or three duplicate ACKs), it then drops to one afterwards and then enters a slow start and into the AIMD phase.

## Calculate the average throughput (in packets/sec and bps)  

Average throughput is roughly `200 packets per sec`, which is `864000 bps`

## Compare the graphs for the two implementations and explain the differences.

> Hint: compare the number of times the congestion window goes back to zero in each case

|TCP Tahoe|TCP Reno|
|:-------:|:------:|
|![](Screenshot from 2020-04-05 18-59-23.png)|![](Screenshot from 2020-04-05 19-51-04.png)|
|![](Screenshot from 2020-04-05 19-17-22.png)|![](Screenshot from 2020-04-05 19-51-49.png)|
|Avg: 185 pkts/s|Avg: 200 pkts/s|
|Avg: 799200 bps|Avg: 864000 bps|

* Both implementations of congestion control reach the maximum congestion window size of 100.
* Both implementations of congestion control, at some point, fill up the buffer queue.
* Both implementations of congestion control oscillate
* TCP Tahoe has large recorded dips in instantaneous throughput - TCP Reno dips in instantaneous throughput by much less
* The congestion window size in TCP Tahoe goes to zero 7 times, while only once with TCP Reno
* TCP Reno has a higher average throughput of 200 packets per second than TCP Tahoe (185 packets per second)

# Exercise 2: Flow Fairness with TCP 

File: [tp_fairness.tcl](tp_fairness.tcl)  
Usage: `ns tp_fairness.tcl`

File: [fairness_pkt.plot](fairness_pkt.plot)  
Usage: `gnuplot fairness_pkt.plot`

![](Screenshot from 2020-04-05 20-08-26.png)

## Does each flow get an equal share of the capacity of the common link (i.e., is TCP fair)?

> Explain which observations lead you to this conclusion.

Each share **does** get an equal share of the capacity of the link.  
We can deduce this as all of the lines of the graph are closely clustered together.

In more detail, at `t=0` to `t=5s`, flow (2-3) is the sole activity in the link, and having 100% of the link capacity, we can assume the capacity of the link to be the recorded throughput of around 120 packets per second.  

After _t=25s_, the average lines for all of the flows vary around the throughput rate of around 25.  
Dividing 120 packets per second by 5 flows, `120 / 5 = 24 packets per second` per flow.  

Hence, as each flow has an average throughput (~25 packets per second) around this equally portioned capacity (24 packets per second), we can conclude that each flow gets an equal share of capacity, and that TCP is fair.

## What happens to the throughput of the pre-existing TCP flows when a new flow is created? Explain the mechanisms of TCP which contribute to this behaviour. Argue about whether you consider this behaviour to be fair or unfair. 

**Note: Modifying the number of flows from 5, to 10**

![](Screenshot from 2020-04-05 20-26-58.png)

* When a new flow is created, the throughput of other existing flows are negatively affected (throughput decreases).  
* Some flows are unable to transmit, as seen by the throughput rate being recorded at 0 packets per second.  
* Each flow no longer has an average throughput of the previous 24 pkts/s, rather they now have an average throughput of around 16 pkts/s
* As the number of flows increase, the average throughput will decrease.  

TCP packets may be purposely dropped to allow packets to be received from other nodes.  

This behaviour can be considered **fair to the new flow** (everyone - including the new flow - is able to transmit, even if only a little bit), **but unfair to existing flows** (throughput decreases).

# Exercise 3: TCP competing with UDP

File: [tp_TCPUDP.tcl](tp_TCPUDP.tcl)  
Usage: `ns tp_TCPUDP <link_capacity>`

File: [TCPUDP_pps.plot](TCPUDP_pps.plot)  
Usage: `gnuplot TCPUDP_pps.plot`

## How do you expect the TCP flow and the UDP flow to behave if the capacity of the link is 5 Mbps?

* TCP packets will assess the current free capacity of the link and rate control its packets.
* UDP packets will dominate the link capacity, and will bombard the link without considering its rate.
* UDP packets will be sent at a much faster rate than TCP packets will.

## Test your hypothesis

> Run the command: `ns tp_TCPUDP.tcl 5Mb` and `gnuplot TCPUDP_pps.plot`

![](Screenshot from 2020-04-05 20-53-13.png)

The <span style="color:red">RED</span> packets can be identified as UDP packets, as they are transmitted continuously in masses.  
The <span style="color:blue">BLUE</span> packets can be identified as TCP packets, as they are transmitted sparingly.

![](Screenshot from 2020-04-05 20-49-37.png)

Yep. UDP packets are being sent out, with throughput in the range of 900-1100 pkts/s.  
TCP packets are only being transmitted at an average rate of around 130 pkts/s.

## Why does one flow achieve higher throughput than the other? Try to explain what mechanisms force the two flows to stabilise to the observed throughput. 

The TCP protocol implements congestion control, using its slow start and AIMD algorithms to find a stable transmission rate. The UDP protocol however, does not implement rate controlling, and hence it does not care about congestion in the link, and simply fires as many packets as it can; regardless if the link is full or not. This is why UDP packets are being transmitted at a higher throughput than the TCP packets.

Factors contributing towards the stabilisation of the throughput for the flows (rather than there being an infinite throughput), is the size of the transmission buffer, and the rate at which data can be modulated and transmitted over the wire.

## List the advantages and the disadvantages of using UDP instead of TCP for a file transfer, when our connection has to compete with other flows for the same link. What would happen if everybody started using UDP instead of TCP for that same reason? 

### Advantages | UDP for file transfer

* Higher throughput (more data transmitted)
* Doesn't consider other activity in the network, so doesn't limit the rate of transmission ("priority")
* Fast!

### Disadvantages | UDP for file transfer

* Packets may not be sent
* Packets may be lost
* No bit error correction - packet needs to be retransmitted
* Will need to implement a structure to manage the order of file segments
* Will need to implement a structure to manage which file segments have [not] been received ([n]ACK)

---

If everyone used UDP instead of TCP, we would run into a lot of packet loss.  
The link will probably still be heavily utilised, but many more packets will be dropped from each user, and the individual throughput of each user will decrease
