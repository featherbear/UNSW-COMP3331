---
title: "Lab 07 - NAT, Ethernet and ARP"
date: 2020-04-19T16:13:11+10:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

# Exercise 1: Understanding NAT using Wireshark

File: [NAT_home_side.pcap](./NAT_home_side.pcap)  
File: [NAT_ISP_side.pcap](./NAT_ISP_side.pcap)

## What is the IP address of the client?

`192.168.1.100`

## At time 7.109267 (#56), what are the source and destination IP addresses and TCP source and destination ports on the IP datagram carrying this HTTP GET? 

![](Screenshot from 2020-04-19 16-55-41.png)

Source: `192.168.1.100:4335`  
Destination: `64.233.169.104:80`

## At what time is the corresponding 200 OK HTTP message received from the Google server?  

At `7.158797` seconds (packet #60) is received.  

Source: `64.233.169.104:80`  
Destination: `192.168.1.100:4335`  

The reply to the request is sent back to the client.

## At what time is the client-to-server TCP SYN segment sent that sets up the connection used by the GET sent at time 7.109267? What are the source and destination IP addresses and source and destination ports for the TCP SYN segment? 

At `7.075657` seconds (packet #53), the SYN segment is sent.  

Source: `192.168.1.100:4335`  
Destination: `64.233.169.104:80`

## What are the source and destination IP addresses and source and destination ports of the ACK sent in response to the SYN. At what time is this SYN/ACK received at the client?

The SYN/ACK is received at `7.108986` seconds (packet #54)

Source: `64.233.169.104:80`  
Destination: `192.168.1.100:4335`  

## At what time does the GET request appear in the NAT_ISP_side trace file? 

The GET request appears at `6.069168` seconds (packet #85)

## What are the source and destination IP addresses and TCP source and destination ports on the IP datagram carrying this HTTP GET message (as recorded in the NAT_ISP_side trace file)?

![](Screenshot from 2020-04-19 17-07-54.png)

Source: `71.192.34.104:4335`  
Destination: `64.233.168.104:80`

### Which of these fields are the same, and which are different, than in your answer to Question 2 above? 

The source port, destination IP and destination port have remained the same.  
The source IP, however, has changed from `192.168.1.100` to `71.192.34.104` (WAN address).

### Are any fields in the HTTP GET message changed?

No, the HTTP layer has remained the same

## Which of the following fields in the IP datagram carrying the HTTP GET are changed: Version, Header Length, Flags, Checksum.

> If any of these fields have changed, give a reason (in one sentence) stating why this field needed to change. 

* Version has remained the same (Version 4)
* Header Length has remained the same (20 bytes)
* Flags have remained the same (0x4000)
* Checksum has CHANGED (0xa94a to 0x022f)
  * As the source IP has changed, a new checksum had to be calculated; hence the checksums will differ

## In the NAT_ISP_side trace file, at what time is the first 200 OK HTTP message received from the Google server?

The first 200 OK HTTP message transmitted by the Google server (64.233.169.104) was at `6.117570` seconds (Packet #90).

## What are the source and destination IP addresses and TCP source and destination ports on the IP datagram carrying this HTTP 200 OK message? Which of these fields are the same, and which are different than your answer to Question 3 above? 

Source: `64.233.168.104:80`  
Destination: `71.192.34.104:4335`

The source port, source IP and destination port have remained the same.  
The destination IP, however, has changed from `192.168.1.100` to `71.192.34.104` (WAN address).

## In the NAT_ISP_side trace file, at what time were the client-to-server TCP SYN segment and the server-to-client TCP SYN/ACK segment corresponding to the segments in Question 4 and 5 above captured? 

The SYN segment was captured at `6.035475` seconds (Packet #82).  
The SYN/ACK segment was captured at `6.067775` seconds (Packet #83).

## What are the source and destination IP addresses and source and destination ports for these two segments (TCP SYN and TCP SYN/ACK)? 

> Which of these fields are the same, and which are different than your answer to Question 4 and 5 above? 

### TCP SYN

Source: `71.192.34.104:4335`  
Destination: `64.233.168.104:80`  

Ports are the same, source IP address has changed

### TCP SYN/ACK

Source: `64.233.168.104:80`  
Destination: `71.192.34.104:4335`

Ports are the same, destination IP address has changed

## The discussion on NAT in the Week 7 lecture slide No 80 shows the NAT translation table used by a NAT router. Using your answers to the questions above, fill in the NAT translation table entries for the HTTP connection considered in the questions above. 

From the home side NAT router:

|Local IP|Local Port|WAN IP|WAN Port|
|:------:|:--------:|:----:|:------:|
|192.168.1.100|4335|71.192.34.104|4335|

# Exercise 2: Using Wireshark to understand Ethernet 

File: [ethernet-ethereal-trace-1](./ethernet-ethereal-trace-1)

## What is the 48-bit Ethernet address of the source host of the HTTP GET message packet? 

`00:d0:59:a9:3d:68`

## What is the 48-bit destination address in the Ethernet frame? Is this the Ethernet address of gaia.cs.umass.edu?

> If not, then which device has this address?  
> Note: this is an important question, and one that students sometimes get wrong. You may want to refer back to relevant parts of the text and lecture notes and make sure you understand the answer here.

`00:06:25:da:af:73`

This is **NOT** the Ethernet address of the server that hosts the website gaia.cs.umass.edu.  
Rather, this is the Ethernet MAC address of the Linksys brand router that is serving requests for that host.  

## Give the hexadecimal value for the two-byte Frame type field. 

`0x0800` (IPv4)

## How many bytes from the very start of the Ethernet frame does the ASCII &apos;G&apos; in &apos;GET&apos; appear in the Ethernet frame?  

> Note that when you examine the Data portion of this frame, it actually consists of both the Ethernet frame headers as well as the payload (i.e. bottom window in Wireshark shows the entire 686 byte frame that is captured).  

The ASCII "G" in "GET" is the 55th byte (Byte number 54, starting from 0).  

### Of the bytes preceding the G, the first few bytes are the Ethernet frame header.  

> Does this include the preamble bytes, or are those bytes omitted from the capture?  
Given this, how many bytes of frame header are present? 

The preamble bytes are omitted from the capture.  
Nothing in the "Frame" section is shown in the bottom window.  

### What are the remainder of the bytes before the G?

* Byte 0-13: Ethernet
* Byte 14-33: IP  
* Byte 34-53: TCP

## What is the value of the Ethernet source address in the HTTP response? Is this the address of the host that sent the GET HTTP request, or of gaia.cs.umass.edu? If not then which device has this address?

In packet #16...

The Ethernet source address is `00:06:25:da:af:73`, which is the address of the Linksys router that the gaia server is behind.  

## What is the destination address in the Ethernet frame? Is this the Ethernet address of the source host that sent the earlier GET HTTP request? 

The destination MAC address is `00:d0:59:a9:3d:68`, which is the ethernet address of the source host that send the GET request.

# Exercise 3: Using Wireshark to understand ARP

RFC826: [Link](https://www.rfc-editor.org/rfc/rfc826.txt)  
ARP Protocol Information: [Link](https://erg.abdn.ac.uk/users/gorry/course/inet-pages/arp.html)

## What are the hexadecimal values for the source and destination addresses in the Ethernet frame containing the ARP request message? Is there something special about the destination address?

Source: `00:d0:59:a9:3d:68`  
Destination: `ff:ff:ff:ff:ff:ff` - This is a broadcast address which all devices will receive.  

## Give the hexadecimal value for the two-byte Ethernet Frame type field

`0x0806` (ARP)

## How many bytes from the very beginning of the Ethernet frame does the ARP opcode field begin?  

The 2-byte opcode starts at the 21st byte (bytes 20-21)

## What is the value of the opcode field within the ARP-payload part of the Ethernet frame in which an ARP request is made? 

`ares_op$REQUEST = 1 = 0x0001` 

## Does the ARP request message contain the IP address of the sender?

Yes, the ARP request message contains the sender's MAC address (00:d0:59:a9:3d:68) and IP address (192.168.1.105).

## Where in the ARP request does the &apos;question&apos; (IP address for which the mapping is being requested) appear?  

![](Screenshot from 2020-04-19 17-58-53.png)

The requested IP appears on the last 4 bytes of the ARP request (bytes 38-41 of the frame)

## How many bytes from the very beginning of the Ethernet frame does the ARP reply opcode field begin? 

The 2-byte opcode starts at the 21st byte (bytes 20-21)

## What is the value of the opcode field within the ARP-payload part of the Ethernet frame in which an ARP response is made? 

`ares_op$REPLY = 2 = 0x0002`

## Where in the ARP message does the &apos;answer&apos; to the earlier ARP request appear – the Ethernet address of the machine whose corresponding IP address is being queried?

The answer (Ethernet address 00:06:25:da:af:73) appears in the ARP frame (Bytes 22-27), but also in the Ethernet frame (Bytes 6-11)

## What are the hexadecimal values for the source and destination addresses in the Ethernet frame containing the ARP reply message? 

Source: `00:06:25:da:af:73`  
Destination: `00:d0:59:a9:3d:68`

