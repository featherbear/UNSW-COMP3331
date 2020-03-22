---
title: "Protocol Layering"
date: 2020-03-10T19:50:38+11:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

# Issues

* May duplicate lower level functionality
* Performance affected
* Header size
* Layer violations - gains too great to resist
* Layer violations - networks don't trust ends

# Routers

Implement the physical, datalink and network layer.  
Transport and application layers are not handled, and are passed, encapsulated through the network layer.

