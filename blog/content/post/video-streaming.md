---
title: "Video Streaming"
date: 2020-03-22T20:16:06+11:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

Videos use **a lot** of space, and bandwidth.  
With so many users each day, even at the same time; lots of money and thought has been put into video hosting and streaming services.

Hetereogeneity - End-systems also have different capabilities - ie some devices have lots of bandwidth, some have none. It is a challenge to cater for all the different requirements.

## Reducing Sizes

* Coding - use redundancy within and between images to decrease the number of bits used to encode an image
  * Spatial - within an image - ie `blue for this whole row`
  * Temporal - between images - ie `this row is still blue`

## Bit Rates

CBR - Constant Bit Rate - Encoding rate is fixed

VBR - Variable Bit Rate - Encoding rate changes depending on the amount of spatial and temporal coding

## DASH

**Dynamic, Adaptive Streaming over HTTP**.

Videos are divided into multiple chunks, and each chunk is encoded at different bit rates. A manifest file provides the URLs for the different chunks and their different bit rates.

The client periodically measures the server-to-client bandwidth, and requests the next chunk at the best bitrate.