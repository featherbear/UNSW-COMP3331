---
title: "Lab 01 - Tools of the Trade"
date: 2020-02-29T16:56:58+11:00

categories: ["Labs"]
hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

# Exercise 1: nslookup

Use the `nslookup` command from the "Tools of the Trade" and answer the following questions:

## Which is the IP address of the website www.koala.com.au? In your opinion, what is the reason of having several IP addresses as an output?

```
$> nslookup www.koala.com.au

Server:		129.94.242.2
Address:	129.94.242.2#53

Non-authoritative answer:
Name:	www.koala.com.au
Address: 104.18.60.21
Name:	www.koala.com.au
Address: 104.18.61.21
```

The `www.koala.com.au` website has several IP addresses: `104.18.60.21`, `104.18.61.21`

One reason that there are multiple address associated to this domain name, so that in the event that the host assigned to one of the addresses goes down, the site is still accessible.

## Find out the name of the IP address 127.0.0.1. What is special about this IP address?

The `127.0.0.1` address is the loopback or localhost address. It is used to address the local computer (itself).

# Exercise 2: Use ping to test host reachability 

Are the following hosts reachable from your machine by using `ping`

`$> ping <host>`

|Host|Status|
|:--|:--:|
|www.unsw.edu.au|Up - 202.58.60.194|
|_www.getfittest.com.au_|No|
|www.mit.edu|Up - 104.116.193.136|
|www.intel.com.au|Up - 184.87.123.186|
|www.tpg.com.au|Up - 203.26.27.38|
|_www.hola.hp_|No|
|www.amazon.com|Up - 13.224.182.228|
|www.tsinghua.edu.cn|Up - 166.111.4.100|
|_www.kremlin.ru_|Down - 95.173.136.70|
|8.8.8.8|Up|

The two sites `www.getfittest.com.au` and `www.hola.hp` do not exist.  

Whilst `www.kremlin.ru` _does_ exist, and is visitable on a web browser, it does not reply to ping requests.
```
$> nslookup www.kremlin.ru
Server:		129.94.242.2
Address:	129.94.242.2#53

Non-authoritative answer:
Name:	www.kremlin.ru
Address: 95.173.136.70
Name:	www.kremlin.ru
Address: 95.173.136.71
Name:	www.kremlin.ru
Address: 95.173.136.72
```

```
$> ping www.kremlin.ru
PING www.kremlin.ru (95.173.136.71) 56(84) bytes of data.
^C
--- www.kremlin.ru ping statistics ---
30 packets transmitted, 0 received, 100% packet loss, time 29680ms
```

# Exercise 3: Use traceroute to understand network topology

Run `traceroute` on your machine `to www.columbia.edu`.

```
$> traceroute www.columbia.edu
traceroute to www.columbia.edu (128.59.105.24), 30 hops max, 60 byte packets
 1  cserouter1-server.cse.unsw.EDU.AU (129.94.242.251)  0.097 ms  0.091 ms  0.115 ms
 2  129.94.39.17 (129.94.39.17)  0.815 ms  0.810 ms  0.837 ms
 3  libudnex1-vl-3154.gw.unsw.edu.au (149.171.253.34)  1.594 ms  2.586 ms  2.587 ms
 4  libcr1-po-6.gw.unsw.edu.au (149.171.255.201)  1.133 ms ombcr1-po-6.gw.unsw.edu.au (149.171.255.169)  1.169 ms ombcr1-po-5.gw.unsw.edu.au (149.171.255.197)  1.091 ms
 5  unswbr1-te-1-9.gw.unsw.edu.au (149.171.255.101)  1.134 ms unswbr1-te-2-13.gw.unsw.edu.au (149.171.255.105)  1.149 ms  1.153 ms
 6  138.44.5.0 (138.44.5.0)  1.247 ms  1.258 ms  1.254 ms
 7  et-1-3-0.pe1.sxt.bkvl.nsw.aarnet.net.au (113.197.15.149)  2.267 ms  2.097 ms  2.123 ms
 8  et-0-0-0.pe1.a.hnl.aarnet.net.au (113.197.15.99)  95.049 ms  95.067 ms  95.063 ms
 9  et-2-1-0.bdr1.a.sea.aarnet.net.au (113.197.15.201)  146.945 ms  146.930 ms  146.936 ms
10  abilene-1-lo-jmb-706.sttlwa.pacificwave.net (207.231.240.8)  146.975 ms  146.905 ms  146.852 ms
11  ae-1.4079.rtsw.minn.net.internet2.edu (162.252.70.173)  179.828 ms  179.937 ms  179.703 ms
12  ae-1.4079.rtsw.eqch.net.internet2.edu (162.252.70.106)  187.821 ms  187.677 ms  187.763 ms
13  ae-0.4079.rtsw3.eqch.net.internet2.edu (162.252.70.163)  187.740 ms  187.664 ms  187.557 ms
14  ae-1.4079.rtsw.clev.net.internet2.edu (162.252.70.130)  196.341 ms  196.578 ms  196.540 ms
15  buf-9208-I2-CLEV.nysernet.net (199.109.11.33)  200.843 ms  200.836 ms  200.835 ms
16  syr-9208-buf-9208.nysernet.net (199.109.7.193)  204.093 ms  203.580 ms  203.613 ms
17  nyc111-9204-syr-9208.nysernet.net (199.109.7.94)  212.870 ms  212.757 ms  212.911 ms
18  nyc-9208-nyc111-9204.nysernet.net (199.109.7.165)  212.979 ms  213.100 ms  214.538 ms
19  columbia.nyc-9208.nysernet.net (199.109.4.14)  212.977 ms  212.970 ms  212.971 ms
20  cc-core-1-x-nyser32-gw-1.net.columbia.edu (128.59.255.5)  213.204 ms  213.098 ms  213.182 ms
21  cc-conc-1-x-cc-core-1.net.columbia.edu (128.59.255.21)  213.351 ms  213.378 ms  213.349 ms
22  exeas.org (128.59.105.24)  213.197 ms  213.157 ms  213.121 ms
```

## How many routers are there between your workstation and `www.columbia.edu`?

There are 21 routers between my workstation (CSE SSH) and `www.columbia.edu`. _(22 if including the final hop)._  

## How many routers along the path are part of the UNSW network?

Of these twenty-one routers, 5 of these routers are part of the UNSW network

## Between which two routers do packets cross the Pacific Ocean?
_Hint: compare the round trip times from your machine to the routers using ping._

```
 7  et-1-3-0.pe1.sxt.bkvl.nsw.aarnet.net.au (113.197.15.149)  2.267 ms  2.097 ms  2.123 ms
 8  et-0-0-0.pe1.a.hnl.aarnet.net.au (113.197.15.99)  95.049 ms  95.067 ms  95.063 ms
 9  et-2-1-0.bdr1.a.sea.aarnet.net.au (113.197.15.201)  146.945 ms  146.930 ms  146.936 ms
```

From the increased RTT time (~2.2ms to 146ms), we can assume that the packets cross between routers 7 and 9.  
The `sea` subdomain seen in hop 7 also suggests that the Pacific Ocean was crossed. 

---

Run traceroute from your machine to the following destinations: (i) `www.ucla.edu` (ii) `www.u-tokyo.ac.jp` and (iii) `www.lancaster.ac.uk`. 


```
$> traceroute www.ucla.edu 
traceroute to www.ucla.edu (164.67.228.152), 30 hops max, 60 byte packets
 1  cserouter1-server.cse.unsw.EDU.AU (129.94.242.251)  0.122 ms  0.121 ms  0.101 ms
 2  129.94.39.17 (129.94.39.17)  0.944 ms  0.941 ms  0.867 ms
 3  ombudnex1-vl-3154.gw.unsw.edu.au (149.171.253.35)  1.717 ms  1.718 ms libudnex1-vl-3154.gw.unsw.edu.au (149.171.253.34)  1.318 ms
 4  libcr1-po-6.gw.unsw.edu.au (149.171.255.201)  1.122 ms libcr1-po-5.gw.unsw.edu.au (149.171.255.165)  1.134 ms ombcr1-po-5.gw.unsw.edu.au (149.171.255.197)  1.104 ms
 5  unswbr1-te-2-13.gw.unsw.edu.au (149.171.255.105)  1.234 ms  1.159 ms unswbr1-te-1-9.gw.unsw.edu.au (149.171.255.101)  1.244 ms
 6  138.44.5.0 (138.44.5.0)  1.342 ms  1.249 ms  1.337 ms
 7  et-1-3-0.pe1.sxt.bkvl.nsw.aarnet.net.au (113.197.15.149)  2.234 ms  2.125 ms  2.072 ms
 8  et-0-0-0.pe1.a.hnl.aarnet.net.au (113.197.15.99)  95.742 ms  95.515 ms  95.512 ms
 9  et-2-1-0.bdr1.a.sea.aarnet.net.au (113.197.15.201)  146.889 ms  146.914 ms  146.907 ms
10  cenichpr-1-is-jmb-778.snvaca.pacificwave.net (207.231.245.129)  164.084 ms  163.521 ms  163.375 ms
11  hpr-lax-hpr3--svl-hpr3-100ge.cenic.net (137.164.25.73)  160.747 ms  160.638 ms  160.014 ms
12  * * *
13  bd11f1.anderson--cr001.anderson.ucla.net (169.232.4.6)  160.372 ms bd11f1.anderson--cr00f2.csb1.ucla.net (169.232.4.4)  160.549 ms bd11f1.anderson--cr001.anderson.ucla.net (169.232.4.6)  161.194 ms
14  cr00f1.anderson--rtr11f4.mathsci.ucla.net (169.232.8.185)  161.200 ms  161.331 ms  160.624 ms
15  * * *
16  * * *
17  * * *
18  * * *
19  * * *
20  * * *
21  * * *
22  * * *
23  * * *
24  * * *
25  * * *
26  * * *
27  * * *
28  * * *
29  * * *
30  * * *
```

```
$> traceroute www.u-tokyo.ac.jp
traceroute to www.u-tokyo.ac.jp (210.152.243.234), 30 hops max, 60 byte packets
 1  cserouter1-server.cse.unsw.EDU.AU (129.94.242.251)  0.110 ms  0.095 ms  0.093 ms
 2  129.94.39.17 (129.94.39.17)  0.844 ms  0.818 ms  0.833 ms
 3  libudnex1-vl-3154.gw.unsw.edu.au (149.171.253.34)  1.541 ms  1.497 ms ombudnex1-vl-3154.gw.unsw.edu.au (149.171.253.35)  1.338 ms
 4  ombcr1-po-5.gw.unsw.edu.au (149.171.255.197)  1.064 ms libcr1-po-6.gw.unsw.edu.au (149.171.255.201)  1.216 ms libcr1-po-5.gw.unsw.edu.au (149.171.255.165)  1.120 ms
 5  unswbr1-te-1-9.gw.unsw.edu.au (149.171.255.101)  1.130 ms  1.203 ms unswbr1-te-2-13.gw.unsw.edu.au (149.171.255.105)  1.117 ms
 6  138.44.5.0 (138.44.5.0)  1.241 ms  1.316 ms  1.271 ms
 7  et-0-3-0.pe1.bkvl.nsw.aarnet.net.au (113.197.15.147)  1.757 ms  1.748 ms  1.836 ms
 8  ge-4_0_0.bb1.a.pao.aarnet.net.au (202.158.194.177)  155.054 ms  155.088 ms  155.031 ms
 9  paloalto0.iij.net (198.32.176.24)  156.388 ms  156.508 ms  156.419 ms
10  osk004bb00.IIJ.Net (58.138.88.185)  287.304 ms osk004bb01.IIJ.Net (58.138.88.189)  269.720 ms  269.713 ms
11  osk004ip57.IIJ.Net (58.138.106.166)  278.306 ms osk004ip57.IIJ.Net (58.138.106.162)  278.142 ms osk004ip57.IIJ.Net (58.138.106.166)  278.137 ms
12  210.130.135.130 (210.130.135.130)  269.402 ms  269.395 ms  278.033 ms
13  124.83.228.58 (124.83.228.58)  269.320 ms  269.293 ms  278.425 ms
14  124.83.252.178 (124.83.252.178)  319.621 ms  317.877 ms  317.739 ms
15  158.205.134.26 (158.205.134.26)  292.991 ms  292.956 ms  292.923 ms
16  * * *
17  * * *
18  * * *
19  * * *
20  * * *
21  * * *
22  * * *
23  * * *
24  * * *
25  * * *
26  * * *
27  * * *
28  * * *
29  * * *
30  * * *
```

```
$> traceroute www.lancaster.ac.uk 
traceroute to www.lancaster.ac.uk (148.88.65.80), 30 hops max, 60 byte packets
 1  cserouter1-server.cse.unsw.EDU.AU (129.94.242.251)  0.127 ms  0.116 ms  0.096 ms
 2  129.94.39.17 (129.94.39.17)  0.927 ms  0.963 ms  0.962 ms
 3  ombudnex1-vl-3154.gw.unsw.edu.au (149.171.253.35)  1.877 ms libudnex1-vl-3154.gw.unsw.edu.au (149.171.253.34)  1.288 ms ombudnex1-vl-3154.gw.unsw.edu.au (149.171.253.35)  1.842 ms
 4  ombcr1-po-6.gw.unsw.edu.au (149.171.255.169)  1.227 ms libcr1-po-6.gw.unsw.edu.au (149.171.255.201)  1.209 ms ombcr1-po-6.gw.unsw.edu.au (149.171.255.169)  1.186 ms
 5  unswbr1-te-2-13.gw.unsw.edu.au (149.171.255.105)  1.279 ms  1.199 ms  1.252 ms
 6  138.44.5.0 (138.44.5.0)  1.664 ms  1.446 ms  1.414 ms
 7  et-2-0-5.bdr1.sing.sin.aarnet.net.au (113.197.15.233)  92.896 ms  92.624 ms  92.542 ms
 8  138.44.226.7 (138.44.226.7)  260.087 ms  260.084 ms  260.058 ms
 9  janet-gw.mx1.lon.uk.geant.net (62.40.124.198)  260.055 ms  260.103 ms  260.076 ms
10  ae29.londpg-sbr2.ja.net (146.97.33.2)  273.026 ms  273.021 ms  272.214 ms
11  ae31.erdiss-sbr2.ja.net (146.97.33.22)  264.492 ms  264.505 ms  264.439 ms
12  ae29.manckh-sbr2.ja.net (146.97.33.42)  266.235 ms  266.295 ms  266.104 ms
13  ae24.lanclu-rbr1.ja.net (146.97.38.58)  268.468 ms  268.538 ms  268.451 ms
14  lancaster-university.ja.net (194.81.46.2)  332.009 ms  331.881 ms  331.875 ms
15  is-border01.bfw01.rtr.lancs.ac.uk (148.88.253.202)  268.899 ms  268.891 ms  268.961 ms
16  bfw01.iss-servers.is-core01.rtr.lancs.ac.uk (148.88.250.98)  272.500 ms  271.125 ms  270.772 ms
17  * * *
18  www.lancs.ac.uk (148.88.65.80)  268.964 ms !X  268.983 ms !X  269.088 ms !X
```

## At which router do the paths from your machine to these three destinations diverge? Find out further details about this router.

_HINT: You can find out more about a router by running the whois command: `whois router-IP-address`_

All three traceroutes follow the same path until they reach hop 6 `138.44.5.0`, where they diverge on hop 7.

This router belongs to AARNET (Australian Academic and Research Network).

```
$> whois 138.44.5.0
whois 138.44.5.0

#
# ARIN WHOIS data and services are subject to the Terms of Use
# available at: https://www.arin.net/resources/registry/whois/tou/
#
# If you see inaccuracies in the results, please report at
# https://www.arin.net/resources/registry/whois/inaccuracy_reporting/
#
# Copyright 1997-2020, American Registry for Internet Numbers, Ltd.
#


NetRange:       138.44.0.0 - 138.44.255.255
CIDR:           138.44.0.0/16
NetName:        APNIC-ERX-138-44-0-0
NetHandle:      NET-138-44-0-0-1
Parent:         NET138 (NET-138-0-0-0-0)
NetType:        Early Registrations, Transferred to APNIC
OriginAS:       
Organization:   Asia Pacific Network Information Centre (APNIC)
RegDate:        2003-12-11
Updated:        2009-10-08
Comment:        This IP address range is not registered in the ARIN database.
Comment:        This range was transferred to the APNIC Whois Database as
Comment:        part of the ERX (Early Registration Transfer) project.
Comment:        For details, refer to the APNIC Whois Database via
Comment:        WHOIS.APNIC.NET or http://wq.apnic.net/apnic-bin/whois.pl
Comment:        
Comment:        ** IMPORTANT NOTE: APNIC is the Regional Internet Registry
Comment:        for the Asia Pacific region.  APNIC does not operate networks
Comment:        using this IP address range and is not able to investigate
Comment:        spam or abuse reports relating to these addresses.  For more
Comment:        help, refer to http://www.apnic.net/apnic-info/whois_search2/abuse-and-spamming
Ref:            https://rdap.arin.net/registry/ip/138.44.0.0

ResourceLink:  http://wq.apnic.net/whois-search/static/search.html
ResourceLink:  whois.apnic.net


OrgName:        Asia Pacific Network Information Centre
OrgId:          APNIC
Address:        PO Box 3646
City:           South Brisbane
StateProv:      QLD
PostalCode:     4101
Country:        AU
RegDate:        
Updated:        2012-01-24
Ref:            https://rdap.arin.net/registry/entity/APNIC

ReferralServer:  whois://whois.apnic.net
ResourceLink:  http://wq.apnic.net/whois-search/static/search.html

OrgTechHandle: AWC12-ARIN
OrgTechName:   APNIC Whois Contact
OrgTechPhone:  +61 7 3858 3188 
OrgTechEmail:  search-apnic-not-arin@apnic.net
OrgTechRef:    https://rdap.arin.net/registry/entity/AWC12-ARIN

OrgAbuseHandle: AWC12-ARIN
OrgAbuseName:   APNIC Whois Contact
OrgAbusePhone:  +61 7 3858 3188 
OrgAbuseEmail:  search-apnic-not-arin@apnic.net
OrgAbuseRef:    https://rdap.arin.net/registry/entity/AWC12-ARIN


#
# ARIN WHOIS data and services are subject to the Terms of Use
# available at: https://www.arin.net/resources/registry/whois/tou/
#
# If you see inaccuracies in the results, please report at
# https://www.arin.net/resources/registry/whois/inaccuracy_reporting/
#
# Copyright 1997-2020, American Registry for Internet Numbers, Ltd.
#



Found a referral to whois.apnic.net.

% [whois.apnic.net]
% Whois data copyright terms    http://www.apnic.net/db/dbcopyright.html

% Information related to '138.44.0.0 - 138.44.255.255'

% Abuse contact for '138.44.0.0 - 138.44.255.255' is 'abuse@aarnet.edu.au'

inetnum:        138.44.0.0 - 138.44.255.255
netname:        AARNET
descr:          Australian Academic and Research Network
descr:          Building 9
descr:          Banks Street
country:        AU
org:            ORG-AAAR1-AP
admin-c:        SM6-AP
tech-c:         ANOC-AP
notify:         irrcontact@aarnet.edu.au
mnt-by:         APNIC-HM
mnt-lower:      MAINT-AARNET-AP
mnt-routes:     MAINT-AARNET-AP
mnt-irt:        IRT-AARNET-AU
status:         ALLOCATED PORTABLE
remarks:        -+-+-+-+-+-+-+-+-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-+-+-+
remarks:        This object can only be updated by APNIC hostmasters.
remarks:        To update this object, please contact APNIC
remarks:        hostmasters and include your organisation's account
remarks:        name in the subject line.
remarks:        -+-+-+-+-+-+-+-+-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-+-+-+
last-modified:  2017-10-09T13:02:43Z
source:         APNIC

irt:            IRT-AARNET-AU
address:        AARNet Pty Ltd
address:        26 Dick Perry Avenue
address:        Kensington, Western Australia
address:        Australia
e-mail:         abuse@aarnet.edu.au
abuse-mailbox:  abuse@aarnet.edu.au
admin-c:        SM6-AP
tech-c:         ANOC-AP
auth:           # Filtered
remarks:        abuse@aarnet.edu.au was validated on 2019-12-03
mnt-by:         MAINT-AARNET-AP
last-modified:  2019-12-03T21:30:31Z
source:         APNIC

organisation:   ORG-AAAR1-AP
org-name:       Australian Academic and Research Network
country:        AU
address:        Building 9
address:        Banks Street
phone:          +61-2-6222-3530
fax-no:         +61-2-6222-3535
e-mail:         irrcontact@aarnet.edu.au
mnt-ref:        APNIC-HM
mnt-by:         APNIC-HM
last-modified:  2017-10-09T12:56:36Z
source:         APNIC

role:           AARNet Network Operations Centre
remarks:
address:        AARNet Pty Ltd
address:        GPO Box 1559
address:        Canberra
address:        ACT  2601
country:        AU
phone:          +61 1300 275 662
phone:          +61 2 6222 3555
remarks:
e-mail:         noc@aarnet.edu.au
remarks:
remarks:        Send abuse reports to abuse@aarnet.edu.au
remarks:        Please include timestamps and offset to UTC in logs
remarks:        Peering requests to peering@aarnet.edu.au
remarks:
admin-c:        SM6-AP
tech-c:         BM-AP
nic-hdl:        ANOC-AP
mnt-by:         MAINT-AARNET-AP
last-modified:  2010-06-30T13:16:48Z
source:         APNIC

person:         Steve Maddocks
remarks:        Director Operations
address:        AARNet Pty Ltd
address:        26 Dick Perry Avenue
address:        Kensington
address:        Perth
address:        WA  6151
country:        AU
phone:          +61-8-9289-2210
fax-no:         +61-2-6222-7509
e-mail:         steve.maddocks@aarnet.edu.au
nic-hdl:        SM6-AP
mnt-by:         MAINT-AARNET-AP
last-modified:  2011-02-01T08:37:06Z
source:         APNIC

% Information related to '138.44.5.0/24AS7575'

route:          138.44.5.0/24
origin:         AS7575
descr:          Australian Academic and Research Network
                Building 9
                Banks Street
mnt-by:         MAINT-AARNET-AP
last-modified:  2019-04-03T03:55:51Z
source:         APNIC

% This query was served by the APNIC Whois Service version 1.88.15-46 (WHOIS-NODE1)
```

## Is the number of hops on each path proportional the physical distance?  

_HINT: You can find out the geographical location of a server using the following tool - http://www.yougetsignal.com/tools/network-location/_

Geographically, Japan is the closest to Australia, followed by USA then UK.  
If the number of hops were to be proportional to the physical distance, we would expect there to be more hops to the UK than to Japan,

|Host|RTT (ms)|Hops|
|:--|:--:|:--:|
|www.ucla.edu|160|14|
|www.u-tokyo.ac.jp|300|15|
|www.lancaster.ac.uk|170|18|

Whilst we do notice that there are more hops to the UK site than to the Japanese site (18 hops > 15 hops), there are more hops to the Japanese site than to the US site (15 hops > 14 hops) despite Japan being geographically closer.  
There is also a much higher ping time to the geographically closest site (Japan).

Therefore we cannot confirm that the number of hops on each path is proportional to the physical distance.

---

Several servers distributed around the world provide a web interface from which you can perform a traceroute to any other host in the Internet.
Here are two examples: (i) http://www.speedtest.com.sg/tr.php and (ii) https://www.telstra.net/cgi-bin/trace. 

Run traceroute from both these servers towards your machine and in the reverse direction (i.e. From your machine to these servers).

_You may also try other traceroute servers from the list at www.traceroute.org._

### http://www.speedtest.com.sg/tr.php

Local To Remote

```
 1  cserouter1-server.cse.unsw.EDU.AU (129.94.242.251)  0.128 ms  0.133 ms  0.110 ms
 2  129.94.39.17 (129.94.39.17)  0.866 ms  0.859 ms  0.880 ms
 3  libudnex1-vl-3154.gw.unsw.edu.au (149.171.253.34)  1.925 ms  1.928 ms  1.921 ms
 4  libcr1-po-6.gw.unsw.edu.au (149.171.255.201)  1.169 ms ombcr1-po-6.gw.unsw.edu.au (149.171.255.169)  1.153 ms ombcr1-po-5.gw.unsw.edu.au (149.171.255.197)  1.143 ms
 5  unswbr1-te-1-9.gw.unsw.edu.au (149.171.255.101)  1.164 ms unswbr1-te-2-13.gw.unsw.edu.au (149.171.255.105)  1.169 ms unswbr1-te-1-9.gw.unsw.edu.au (149.171.255.101)  1.193 ms
 6  138.44.5.0 (138.44.5.0)  1.311 ms  1.296 ms  1.290 ms
 7  et-0-3-0.pe1.alxd.nsw.aarnet.net.au (113.197.15.153)  1.714 ms  1.740 ms  1.741 ms
 8  xe-0-2-7.bdr1.a.lax.aarnet.net.au (202.158.194.173)  147.603 ms  147.651 ms  147.606 ms
 9  singtel.as7473.any2ix.coresite.com (206.72.210.63)  147.788 ms  147.642 ms  147.685 ms
10  203.208.171.117 (203.208.171.117)  148.602 ms  148.049 ms  148.039 ms
11  203.208.172.145 (203.208.172.145)  242.553 ms 203.208.171.85 (203.208.171.85)  239.710 ms 203.208.172.145 (203.208.172.145)  242.827 ms
12  203.208.158.17 (203.208.158.17)  335.722 ms  329.498 ms *
13  * * *
14  * * 203.208.177.110 (203.208.177.110)  329.402 ms
15  * * *
16  * * *
17  * * *
18  * * *
19  * * *
20  * * *
21  * * *
22  * * *
23  * * *
24  * * *
25  * * *
26  * * *
27  * * *
28  * * *
29  * * *
30  * * *
```

Remote to Local

```
 1  ge2-8.r01.sin01.ne.com.sg (202.150.221.169)  0.168 ms  0.198 ms  0.220 ms
 2  10.15.62.210 (10.15.62.210)  0.229 ms  0.336 ms  0.369 ms
 3  aarnet.sgix.sg (103.16.102.67)  209.173 ms  209.189 ms  209.203 ms
 4  et-7-3-0.pe1.nsw.brwy.aarnet.net.au (113.197.15.232)  208.167 ms  208.216 ms  208.235 ms
 5  138.44.5.1 (138.44.5.1)  209.222 ms  209.292 ms  209.313 ms
 6  ombcr1-te-1-5.gw.unsw.edu.au (149.171.255.106)  211.587 ms  211.556 ms  211.537 ms
 7  libudnex1-po-2.gw.unsw.edu.au (149.171.255.198)  208.901 ms  208.649 ms  208.748 ms
 8  ufw1-ae-1-3154.gw.unsw.edu.au (149.171.253.36)  212.338 ms  212.181 ms  212.196 ms
 9  129.94.39.23 (129.94.39.23)  210.050 ms  210.064 ms  210.165 ms
```

### https://www.telstra.net/cgi-bin/trace

Local To Remote

```
 1  cserouter1-server.cse.unsw.EDU.AU (129.94.242.251)  0.126 ms  0.101 ms  0.103 ms
 2  129.94.39.17 (129.94.39.17)  0.822 ms  0.782 ms  0.874 ms
 3  libudnex1-vl-3154.gw.unsw.edu.au (149.171.253.34)  1.950 ms ombudnex1-vl-3154.gw.unsw.edu.au (149.171.253.35)  5.662 ms libudnex1-vl-3154.gw.unsw.edu.au (149.171.253.34)  1.978 ms
 4  ombcr1-po-5.gw.unsw.edu.au (149.171.255.197)  1.063 ms libcr1-po-6.gw.unsw.edu.au (149.171.255.201)  1.110 ms  1.128 ms
 5  unswbr1-te-2-13.gw.unsw.edu.au (149.171.255.105)  1.102 ms  1.110 ms  1.135 ms
 6  138.44.5.0 (138.44.5.0)  1.274 ms  1.282 ms  1.288 ms
 7  xe-0-0-0.bdr1.rsby.nsw.aarnet.net.au (113.197.15.33)  1.441 ms  1.396 ms  1.399 ms
 8  gigabitethernet3-11.ken37.sydney.telstra.net (139.130.0.77)  2.147 ms  2.260 ms  3.811 ms
 9  bundle-ether13.ken-core10.sydney.telstra.net (203.50.11.94)  3.275 ms  3.699 ms  3.717 ms
10  bundle-ether10.win-core10.melbourne.telstra.net (203.50.11.123)  14.763 ms  14.667 ms  14.132 ms
11  tengigabitethernet8-1.exi2.melbourne.telstra.net (203.50.80.154)  12.792 ms * *
```

Remote To Local

```
 1  gigabitethernet3-3.exi2.melbourne.telstra.net (203.50.77.53)  0.339 ms  0.204 ms  0.240 ms
 2  bundle-ether3-100.win-core10.melbourne.telstra.net (203.50.80.129)  1.491 ms  1.603 ms  2.118 ms
 3  bundle-ether12.ken-core10.sydney.telstra.net (203.50.11.122)  13.860 ms  12.597 ms  12.985 ms
 4  bundle-ether1.ken-edge901.sydney.telstra.net (203.50.11.95)  12.109 ms  12.094 ms  12.860 ms
 5  aarnet6.lnk.telstra.net (139.130.0.78)  11.983 ms  11.725 ms  11.735 ms
 6  xe-5-2-2.pe1.brwy.nsw.aarnet.net.au (113.197.15.32)  11.985 ms  11.848 ms  11.863 ms
 7  138.44.5.1 (138.44.5.1)  12.108 ms  12.102 ms  12.109 ms
 8  libcr1-te-1-5.gw.unsw.edu.au (149.171.255.102)  12.107 ms  12.097 ms  12.111 ms
 9  libudnex1-po-1.gw.unsw.edu.au (149.171.255.166)  12.858 ms
10  ufw1-ae-1-3154.gw.unsw.edu.au (149.171.253.36)  12.857 ms  12.851 ms  12.732 ms
11  129.94.39.23 (129.94.39.23)  12.860 ms  12.975 ms  12.859 ms
```

## What are the IP addresses of the two servers that you have chosen.

* CSE Machine: `129.94.242.19`
* `ge2-8.r01.sin01.ne.com.sg` - `202.150.221.169`
* `gigabitethernet3-3.exi2.melbourne.telstra.net` - `203.50.77.53`

## Does the reverse path go through the same routers as the forward path?

The reverse path does not go through the exact same routers, however they do pass very similar ones.  

## If you observe common routers between the forward and the reverse path, do you also observe the same IP addresses? Why or why not? 

-

# Exercise 4: Use ping to gain insights into network performance 

Use [this script](./runping.sh) for the following destinations:  
(i) www.uq.edu.au (ii) www.dlsu.edu.ph and (iii) www.tu-berlin.de 

Then plot them with [this script](./plot.sh)

```
$> ./runping.sh www.uq.edu.au
ping -s 22 -c 50 -i 1 www.uq.edu.au > www.uq.edu.au-p50
ping -s 222 -c 50 -i 1 www.uq.edu.au > www.uq.edu.au-p250
ping -s 472 -c 50 -i 1 www.uq.edu.au > www.uq.edu.au-p500
ping -s 722 -c 50 -i 1 www.uq.edu.au > www.uq.edu.au-p750
ping -s 972 -c 50 -i 1 www.uq.edu.au > www.uq.edu.au-p1000
ping -s 1222 -c 50 -i 1 www.uq.edu.au > www.uq.edu.au-p1250
ping -s 1472 -c 50 -i 1 www.uq.edu.au > www.uq.edu.au-p1500


$> ./plot www.uq.edu.au-p*
www.uq.edu.au
processing www.uq.edu.au-p1000
1000 17.180 16.888
processing www.uq.edu.au-p1250
1250 17.299 16.966
processing www.uq.edu.au-p1500
1500 17.454 17.145
processing www.uq.edu.au-p250
250 17.042 16.642
processing www.uq.edu.au-p50
50 16.948 16.458
processing www.uq.edu.au-p500
500 17.010 16.691
processing www.uq.edu.au-p750
750 17.162 16.786
ps2pdf www.uq.edu.au_delay.ps
ps2pdf www.uq.edu.au_scatter.ps

# $> ./runping.sh www.dlsu.edu.ph
# Took too long so decided to use another destination

$> ./runping upd.edu.ph
ping -s 22 -c 50 -i 1 upd.edu.ph > upd.edu.ph-p50
ping -s 222 -c 50 -i 1 upd.edu.ph > upd.edu.ph-p250
ping -s 472 -c 50 -i 1 upd.edu.ph > upd.edu.ph-p500
ping -s 722 -c 50 -i 1 upd.edu.ph > upd.edu.ph-p750
ping -s 972 -c 50 -i 1 upd.edu.ph > upd.edu.ph-p1000
ping -s 1222 -c 50 -i 1 upd.edu.ph > upd.edu.ph-p1250
ping -s 1472 -c 50 -i 1 upd.edu.ph > upd.edu.ph-p1500

$> ./plot upd.edu.ph-p*
upd.edu.ph
processing upd.edu.ph-p1000
1000 354.618 354.378
processing upd.edu.ph-p1250
1250 354.856 354.532
processing upd.edu.ph-p1500
1500 355.189 354.743
processing upd.edu.ph-p250
250 353.939 353.613
processing upd.edu.ph-p50
50 353.622 353.146
processing upd.edu.ph-p500
500 354.128 353.847
processing upd.edu.ph-p750
750 355.285 354.207
ps2pdf upd.edu.ph_delay.ps
ps2pdf upd.edu.ph_scatter.ps

$> ./runping.sh www.tu-berlin.de
ping -s 22 -c 50 -i 1 www.tu-berlin.de > www.tu-berlin.de-p50
ping -s 222 -c 50 -i 1 www.tu-berlin.de > www.tu-berlin.de-p250
ping -s 472 -c 50 -i 1 www.tu-berlin.de > www.tu-berlin.de-p500
ping -s 722 -c 50 -i 1 www.tu-berlin.de > www.tu-berlin.de-p750
ping -s 972 -c 50 -i 1 www.tu-berlin.de > www.tu-berlin.de-p1000
ping -s 1222 -c 50 -i 1 www.tu-berlin.de > www.tu-berlin.de-p1250
ping -s 1472 -c 50 -i 1 www.tu-berlin.de > www.tu-berlin.de-p1500

$> ./plot www.tu-berlin.de-p*
www.tu-berlin.de
processing www.tu-berlin.de-p1000
1000 288.093 287.903
processing www.tu-berlin.de-p1250
1250 288.088 287.972
processing www.tu-berlin.de-p1500
1500 288.181 288.027
processing www.tu-berlin.de-p250
250 287.751 287.598
processing www.tu-berlin.de-p50
50 287.596 287.496
processing www.tu-berlin.de-p500
500 287.819 287.724
processing www.tu-berlin.de-p750
750 287.941 287.812
ps2pdf www.tu-berlin.de_delay.ps
ps2pdf www.tu-berlin.de_scatter.ps
```

## Files

**Ping Results**

|www.uq.edu.au|upd.edu.ph|www.tu-berlin.de|
|:--|:--|:--|
|[www.uq.edu.au-p50](./www.uq.edu.au-p50)|[upd.edu.ph-p50](./upd.edu.ph-p50)|[www.tu-berlin.de-p50](./www.tu-berlin.de-p50)|
|[www.uq.edu.au-p250](./www.uq.edu.au-p250)|[upd.edu.ph-p250](./upd.edu.ph-p250)|[www.tu-berlin.de-p250](./www.tu-berlin.de-p250)|
|[www.uq.edu.au-p500](./www.uq.edu.au-p500)|[upd.edu.ph-p500](./upd.edu.ph-p500)|[www.tu-berlin.de-p500](./www.tu-berlin.de-p500)|
|[www.uq.edu.au-p750](./www.uq.edu.au-p750)|[upd.edu.ph-p750](./upd.edu.ph-p750)|[www.tu-berlin.de-p750](./www.tu-berlin.de-p750)|
|[www.uq.edu.au-p1000](./www.uq.edu.au-p1000)|[upd.edu.ph-p1000](./upd.edu.ph-p1000)|[www.tu-berlin.de-p1000](./www.tu-berlin.de-p1000)|
|[www.uq.edu.au-p1250](./www.uq.edu.au-p1250)|[upd.edu.ph-p1250](./upd.edu.ph-p1250)|[www.tu-berlin.de-p1250](./www.tu-berlin.de-p1250)|
|[www.uq.edu.au-p1500](./www.uq.edu.au-p1500)|[upd.edu.ph-p1500](./upd.edu.ph-p1500)|[www.tu-berlin.de-p1500](./www.tu-berlin.de-p1500)|

**Averages**

|Packet Size|www.uq.edu.au|upd.edu.ph|www.tu-berlin.de|
|:--:|:--:|:--:|:--:|
|-FILES-|[www.uq.edu.au_avg.txt](./www.uq.edu.au_avg.txt)|[upd.edu.ph_avg.txt](./upd.edu.ph_avg.txt)|[www.tu-berlin.de_avg.txt](./www.tu-berlin.de_avg.txt)|
|50|16.948|353.622|287.596|
|250|17.042|353.939|287.751|
|500|17.010|354.128|287.819|
|750|17.162|355.285|287.941|
|1000|17.180|354.618|288.093|
|1250|17.299|354.856|288.088|
|1500|17.454|355.189|288.181|

**Minimums**

|Packet Size|www.uq.edu.au|upd.edu.ph|www.tu-berlin.de|
|:--:|:--:|:--:|:--:|
|-FILES-|[www.uq.edu.au_avg.txt](./www.uq.edu.au_avg.txt)|[upd.edu.ph_avg.txt](./upd.edu.ph_avg.txt)|[www.tu-berlin.de_avg.txt](./www.tu-berlin.de_avg.txt)|
|50|16.458|353.146|287.496|
|250|16.642|353.613|287.598|
|500|16.691|353.847|287.724|
|750|16.786|354.207|287.812|
|1000|16.888|354.378|287.903|
|1250|16.966|354.532|287.972|
|1500|17.145|354.743|288.027|

**Scatter Diagrams**

|www.uq.edu.au|upd.edu.ph|www.tu-berlin.de|
|:--:|:--:|:--:|
|![](www.uq.edu.au_scatter.png)|![](upd.edu.ph_scatter.png)|![](www.tu-berlin.de_scatter.png)|
|[www.uq.edu.au_scatter.pdf](./www.uq.edu.au_scatter.pdf)|[upd.edu.ph_scatter.pdf](./upd.edu.ph_scatter.pdf)|[www.tu-berlin.de_scatter.pdf](./www.tu-berlin.de_scatter.pdf)|
|[www.uq.edu.au_scatter.ps](./www.uq.edu.au_scatter.ps)|[upd.edu.ph_scatter.ps](./upd.edu.ph_scatter.ps)|[www.tu-berlin.de_scatter.ps](./www.tu-berlin.de_scatter.ps)|

**Delay Diagrams**

|www.uq.edu.au|upd.edu.ph|www.tu-berlin.de|
|:--:|:--:|:--:|
|![](www.uq.edu.au_delay.png)|![](upd.edu.ph_delay.png)|![](www.tu-berlin.de_delay.png)|
|[www.uq.edu.au_delay.pdf](./www.uq.edu.au_delay.pdf)|[upd.edu.ph_delay.pdf](./upd.edu.ph_delay.pdf)|[www.tu-berlin.de_delay.pdf](./www.tu-berlin.de_delay.pdf)|
|[www.uq.edu.au_delay.ps](./www.uq.edu.au_delay.ps)|[upd.edu.ph_delay.ps](./upd.edu.ph_delay.ps)|[www.tu-berlin.de_delay.ps](./www.tu-berlin.de_delay.ps)|

## For each of these locations compute the shortest possible time T for a packet to reach that location from UNSW.

_HINT: Find the (approximate) physical distance from UNSW using Google Maps_  
_You should assume that the packet moves (i.e. propagates) at the speed of light, 3 x 10^8 m/s._  
_Note that the shortest possible time will simply be the distance divided by the propagation speed._  

|Destination|Distance (km)|Time Taken (ms)|
|:--|--:|--:|
|University of Queensland|730|2|
|University of the Philippines Diliman|6300|21|
|Berlin Institute of Technology|16,100|53|

## Plot a graph of the distance to each city against the RTT / theoretical time ratio

Where the x-axis represents the distance to each city (i.e. Brisbane, <s>Manila</s> Diliman and Berlin)  
and the y-axis represents the ratio between the minimum delay (i.e. RTT) as measured by the ping program (select the values for 50 byte packets) and the shortest possible time T to reach that city from UNSW.

![](distance-to-ratio-graph.png)


## Can you think of at least two reasons why the y-axis values that you plot are greater than 2? 

> Note that the y-values are no smaller than 2 since it takes at least 2*T time for any packet to reach the destination from UNSW and get back.  

* The time it takes to get to a destination and back will take at least twice as long, since the packet needs to travel the same distance to and fro.

* Delays (queueing, transmission, processing, propagation) will make the packet take a longer time to arrive.

## Is the delay to the destinations constant or does it vary over time? Explain why. 

The delays will vary over time for a number of reasons.  
Depending on the network load by other devices, congestion may affect the bandwidth and the rate at which the packets can be transmitted.  
Environmental factors can also affect the transmission of packets, as understood via wireless technologies (Radio interference, humidity, etc).

The delays related to the UNSW network would be rather constant for the investigations performed in this lab exercise, as all commands were executed at roughly the same time.

## Explore where the website for www.epfl.ch is hosted. Is it in Switzerland? 

**nslookup**
```
nslookup www.epfl.ch
Server:		129.94.242.45
Address:	129.94.242.45#53

Non-authoritative answer:
www.epfl.ch	canonical name = www.epfl.ch.cdn.cloudflare.net.
Name:	www.epfl.ch.cdn.cloudflare.net
Address: 104.20.228.42
Name:	www.epfl.ch.cdn.cloudflare.net
Address: 104.20.229.42
```

**ping**
```
$> ping www.epfl.ch -c 1
PING www.epfl.ch.cdn.cloudflare.net (104.20.229.42) 56(84) bytes of data.
64 bytes from 104.20.229.42: icmp_req=1 ttl=56 time=1.47 ms

--- www.epfl.ch.cdn.cloudflare.net ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 1.478/1.478/1.478/0.000 ms
```

**Whois Query**

```
Domain name: epfl.ch

Holder: Ecole Polytechnique Federale de Lausanne
        Repond Nicolas
        Station 8
        EPFL SI
        CH-1015 Lausanne
Registrar: Swizzonic AG

DNSSEC: no

Name servers:
  stisun1.epfl.ch   128.178.15.8
  stisun1.epfl.ch   2001:620:618:10f:1:80b2:f08:1
  stisun2.epfl.ch   128.178.15.7
  stisun2.epfl.ch   2001:620:618:10f:1:80b2:f07:1

First registration date: before 01 January 1996
```

From the above, the `www.epfl.ch` domain appears to be hosted on CloudFlare servers (in the US) outside of Switzerland.

## Which delay type depends on the packet size and which do not? 

_The measured delay (i.e., the delay you can see in the graphs) is composed of propagation delay, transmission delay, processing delay and queuing delay._

Packet size affects the processing and transmission delay, whilst propagation and queueing delay are unaffected by the packet size.
