---
title: "Wireless Links and Networks"
date: 2020-04-28T21:59:16+10:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

# Wireless Communication

* Hosts - Devices that utilise wireless links
  * i.e. Phones and Laptops
* Base Stations - Devices that relay packets between wired and wireless hosts
  * i.e. Cell towers and Access Points

* Different protocols, use different frequencies, and strengths.
* They vary in range and data bandwidth

## Issues with Wireless Communication

* Signal strength - Signal attenuation as it passes through matter
* Multipath propagation - Radio signals bounce off objects and arrive at the destination at different times
* Interference - Electromagnetic interference from ... everything

* Free Space Path Lost = (4 * pi * distance / wavelength)^2 = (4 * pi * distance * frequency / speed of light)^2
* Signal to Noise Ratio (SNR) - Measure of how easy it is to extract a signal from noise
  * Larger SNR the better
  * Often improved with higher antennae power

## The failure of CSMA/CD

If two devices are separated by a far distance, with another device in the middle - the two original devices may not be aware of each other, and only of the common middle device.  
They will be unaware of if the other device is transmitting to the middle device, and are hence unaware of possible interference of transmission.

## WiFi (IEEE 802.11)

* BSS - Basic Service Set - Cell - Access Points
  * APs regularly transmit beacon frames containing their SSID and MAC address

* 2.4 GHz spectrum - divided into 11 channels (frequency ranges)
  * Try to be on different channels than nearby networks for better performance
* Hosts associate with a given access point

### CSMA/CA in WiFi

> Rather than trying to detect for possible collisions, just try to avoid it.  

* There is no global collision - Each sender and receiver will be experiencing different signals at any given moment.  
* Only reception of the signal by the receiver is kept in mind - Sender will transmit even if it detect other transmissions

1) If sense channel idle for Distributed Coordination Function Inter Frame Space (DIFS) - then transmit  
2) If sense channel busy, then backoff for a random amount of time

The receiver will broadcast an ACK after the Short Inter Frame Space (SIFS) time so that other devices know that it is ready to receive.

![](Screenshot from 2020-04-28 22-22-40.png)

### RTS and CTS

A transmitting device will send a Request To Send (RTS) packet.  
Only when (and if) the receiving device replies with a Clear To Send (CTS) packet, will the transmission begin.  
Otherwise transmission will be defered until later.  

The Clear To Send packet is broadcasted to all nearby hosts, so they know not to transmit if they are not the recipient in the broadcast

Flow: RTS -> CTS -> DATA -> ACK
