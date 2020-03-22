---
title: "Internet Structure"
date: 2020-03-04T19:39:10+11:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

Given millions of access ISPs, it is not feasible to connect all of them to each other, as it is not scalable.  
In fact, it would take O(n^2) connections.  

* Access ISPs connnect to Global ISPs.  
* Access ISPs may instead be connected to Regional ISPs, which are connected to Global ISPs.  
* Global ISPs interconnect via Internet Exchange Points (IXPs), and can also peer directly.  
* Content providers / CDNs may run their own ISP network. 

![](./Screenshot from 2020-03-04 19-49-32.png)