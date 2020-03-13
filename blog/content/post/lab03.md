---
title: "Lab 03 - DNS & Socket Programming"
date: 2020-03-13T11:02:27+11:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---


# Explore DNS records

> DNS servers use different record types for different purposes. For each type of DNS record, there is an associated type of DNS query. Check the following page ( https://en.wikipedia.org/wiki/List_of_DNS_record_types ) and find out what the following resource record types are used for:  
* A  
* CNAME  
* MX  
* NS  
* PTR  
* SOA  

* `A` record - Domain -> IPv4 Address
* `CNAME` - Canonical Name - Alias to another name  
* `MX` - Mail Exchange - Map domain names to MTAs
* `NS` - Name Server - For subdomain DNS resolving
* `PTR` - Pointer - Like the alias, but doesn't keep trying to resolve -> Used for Reverse DNS
* `SOA` - Start Of Authority - Authoritative information.

---

|TYPE|EXAMPLE|
|:--|:--|
|A|example.com A 1400 IN 192.168.1.1|
|CNAME|ftp.example CNAME 1400 IN example.com|


# Tracing DNS with Wireshark

![](Screenshot from 2020-03-13 11-13-06.png)

File: [dns-ethereal-trace-2](./dns-ethereal-trace-2)

## What transport layer protocol is being used by the DNS messages?

UDP (User Datagram Protocol)

**Why?**  
Don't need reliability, and also need performance

## What is the source and destination port for the DNS query message and the corresponding response? 

Query: Source `3742` | Dest `53`  
Response: Source `53` | Dest `3742`

## To what IP address is the DNS query message sent? Is this the same as the default local DNS server?

`128.238.29.22`

Yes, it is the same IP.

## How many &apos;questions&apos; are contained in the DNS query message? What &apos;Type&apos; of DNS queries are they? Does the query message also contain any &apos;answers&apos;? 

One. `www.mit.edu: type A, class IN`.  
No answers in the query.

# Examine the DNS response message. Provide details of the contents of the &apos;Answers&apos;, &apos;Authority&apos; and &apos;Additional Information&apos; fields. What can you infer from these? 

Answer: `www.mit.edu: type A, class IN, addr 18.7.22.83`

Authoritive Nameservers  

* `mit.edu: type NS, class IN, ns BITSY.mit.edu`
* `mit.edu: type NS, class IN, ns STRAWB.mit.edu`
* `mit.edu: type NS, class IN, ns W20NS.mit.edu`

Additional Records

* `BITSY.mit.edu: type A, class IN, addr 18.72.0.3`
* `STRAWB.mit.edu: type A, class IN, addr 18.71.0.151`
* `W20NS.mit.edu: type A, class IN, addr 18.70.0.160`

`www.mit.edu` points to the address `18.7.22.83`.  
There are three nameservers which handle the (sub)domain names for `mit.edu` - `BITSY` (`18.72.0.3`), `STRAWB` (`18.71.0.151`) nd `W20NS` (`18.70.0.160`).

# Digging into DNS

## What is the IP address of www.cecs.anu.edu.au? What type of DNS query is sent to get this answer?

```
$> dig www.cecs.anu.edu.au

; <<>> DiG 9.9.5-9+deb8u18-Debian <<>> www.cecs.anu.edu.au
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 42848
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 4, ADDITIONAL: 9

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;www.cecs.anu.edu.au.           IN      A

;; ANSWER SECTION:
www.cecs.anu.edu.au.    1518    IN      CNAME   rproxy.cecs.anu.edu.au.
rproxy.cecs.anu.edu.au. 1518    IN      A       150.203.161.98

;; AUTHORITY SECTION:
edu.au.                 238     IN      NS      q.au.
edu.au.                 238     IN      NS      t.au.
edu.au.                 238     IN      NS      s.au.
edu.au.                 238     IN      NS      r.au.

;; ADDITIONAL SECTION:
q.au.                   21726   IN      A       65.22.196.1
q.au.                   11497   IN      AAAA    2a01:8840:be::1
r.au.                   27461   IN      A       65.22.197.1
r.au.                   126705  IN      AAAA    2a01:8840:bf::1
s.au.                   37577   IN      A       65.22.198.1
s.au.                   20725   IN      AAAA    2a01:8840:c0::1
t.au.                   12598   IN      A       65.22.199.1
t.au.                   7678    IN      AAAA    2a01:8840:c1::1

;; Query time: 0 msec
;; SERVER: 129.94.242.2#53(129.94.242.2)
;; WHEN: Fri Mar 13 11:53:49 AEDT 2020
;; MSG SIZE  rcvd: 325
```

`www.cecs.anu.edu.au` points to `150.203.161.98`. An `A` record DNS query is sent to get this answer.

We can confirm thi result with a `ping`, as seen below

```
$> ping www.cecs.anu.edu.au -c 1
PING rproxy.cecs.anu.edu.au (150.203.161.98) 56(84) bytes of data.
64 bytes from rproxy.cecs.anu.edu.au (150.203.161.98): icmp_seq=1 ttl=52 time=6.40 ms

--- rproxy.cecs.anu.edu.au ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 6.408/6.408/6.408/0.000 ms
```

## What is the canonical name for the CECS ANU web server? Suggest a reason for having an alias for this server. 

```
$> dig www.cecs.anu.edu.au CNAME

; <<>> DiG 9.9.5-9+deb8u18-Debian <<>> www.cecs.anu.edu.au CNAME
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 64945
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 3, ADDITIONAL: 4

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;www.cecs.anu.edu.au.           IN      CNAME

;; ANSWER SECTION:
www.cecs.anu.edu.au.    1359    IN      CNAME   rproxy.cecs.anu.edu.au.

;; AUTHORITY SECTION:
anu.edu.au.             53      IN      NS      ns.adelaide.edu.au.
anu.edu.au.             53      IN      NS      una.anu.edu.au.
anu.edu.au.             53      IN      NS      ns1.anu.edu.au.

;; ADDITIONAL SECTION:
ns.adelaide.edu.au.     2480    IN      A       129.127.40.3
ns1.anu.edu.au.         778     IN      A       150.203.1.10
una.anu.edu.au.         53      IN      A       150.203.22.28

;; Query time: 0 msec
;; SERVER: 129.94.242.2#53(129.94.242.2)
;; WHEN: Fri Mar 13 11:56:28 AEDT 2020
;; MSG SIZE  rcvd: 179
```

`www.cecs.anu.edu.au` is a `CNAME` to `rproxy.cecs.anu.edu.au`.

Canonical names and aliases are useful for maintainability, as only `rproxy.cecs.anu.edu.au` will need to have an `A` record assigned.  
Therefore if the IP address of the server machine changes, only one record will need to be updated.

## What can you make of the rest of the response (i.e. the details available in the Authority and Additional sections)? 


```
edu.au.                 238     IN      NS      q.au.
edu.au.                 238     IN      NS      t.au.
edu.au.                 238     IN      NS      s.au.
edu.au.                 238     IN      NS      r.au.
```

The Authority section notes that the name servers at `q.au`, `t.au`, `s.au` and `r.au` are responsible for DNS queries of the subdomains of `edu.au`

---

```
anu.edu.au.             53      IN      NS      ns.adelaide.edu.au.
anu.edu.au.             53      IN      NS      una.anu.edu.au.
anu.edu.au.             53      IN      NS      ns1.anu.edu.au.
```

Subdomain records for ANU are managed by `ns.adelaide.edu.au`, `una.anu.edu.au` and `ns1.anu.edu.au`.

Their IPv4 and IPv6 addresses are shown in the previous dig command output.

## What is the IP address of the local nameserver for your machine? 

`129.94.242.2`

## What are the DNS nameservers for the &apos;cecs.anu.edu.au&apos; domain (note: the domain name is cecs.anu.edu.au and not www.cecs.anu.edu.au )? Find out their IP addresses? What type of DNS query is sent to obtain this information? 

```
$> dig cecs.anu.edu.au NS

; <<>> DiG 9.9.5-9+deb8u18-Debian <<>> cecs.anu.edu.au NS
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 37725
;; flags: qr rd ra; QUERY: 1, ANSWER: 3, AUTHORITY: 0, ADDITIONAL: 7

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;cecs.anu.edu.au.               IN      NS

;; ANSWER SECTION:
cecs.anu.edu.au.        299     IN      NS      ns4.cecs.anu.edu.au.
cecs.anu.edu.au.        299     IN      NS      ns3.cecs.anu.edu.au.
cecs.anu.edu.au.        299     IN      NS      ns2.cecs.anu.edu.au.

;; ADDITIONAL SECTION:
ns2.cecs.anu.edu.au.    299     IN      A       150.203.161.36
ns2.cecs.anu.edu.au.    500     IN      AAAA    2001:388:1034:2905::24
ns3.cecs.anu.edu.au.    299     IN      A       150.203.161.50
ns3.cecs.anu.edu.au.    500     IN      AAAA    2001:388:1034:2905::32
ns4.cecs.anu.edu.au.    299     IN      A       150.203.161.38
ns4.cecs.anu.edu.au.    500     IN      AAAA    2001:388:1034:2905::26

;; Query time: 0 msec
;; SERVER: 129.94.242.2#53(129.94.242.2)
;; WHEN: Fri Mar 13 12:02:58 AEDT 2020
;; MSG SIZE  rcvd: 230
```

_Ignoring IPv6 / AAAA records..._  
The nameservers for `cecs.anu.edu.au` are `ns2.cecs.anu.edu.au` (`150.203.161.36`), `ns3.cecs.anu.edu.au` (`150.203.161.50`) and `ns3.cecs.anu.edu.au` (`150.203.161.38`).

An `NS` query was sent to obtain this information

## What is the DNS name associated with the IP address 111.68.101.54? What type of DNS query is sent to obtain this information? 

```
$> dig -x 111.68.101.54

; <<>> DiG 9.9.5-9+deb8u18-Debian <<>> -x 111.68.101.54
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 58962
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 2, ADDITIONAL: 3

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;54.101.68.111.in-addr.arpa.    IN      PTR

;; ANSWER SECTION:
54.101.68.111.in-addr.arpa. 1213 IN     PTR     webserver.seecs.nust.edu.pk.

;; AUTHORITY SECTION:
101.68.111.in-addr.arpa. 22072  IN      NS      ns2.hec.gov.pk.
101.68.111.in-addr.arpa. 22072  IN      NS      ns1.hec.gov.pk.

;; ADDITIONAL SECTION:
ns1.hec.gov.pk.         1212    IN      A       103.4.93.5
ns2.hec.gov.pk.         1212    IN      A       103.4.93.6

;; Query time: 0 msec
;; SERVER: 129.94.242.2#53(129.94.242.2)
;; WHEN: Fri Mar 13 12:05:18 AEDT 2020
;; MSG SIZE  rcvd: 172
```

`111.68.101.54` points to `webserver.seecs.nust.edu.pk`.

A `PTR` query (Reverse DNS lookup) was sent to obtain this information.

## Run dig and query the CSE nameserver (129.94.242.33) for the mail servers for Yahoo! Mail (again the domain name is yahoo.com, not www.yahoo.com ). Did you get an authoritative answer? Why?  

_HINT: Just because a response contains information in the authoritative part of the DNS response message does not mean it came from an authoritative name server. You should examine the flags in the response to determine the answer_

```
$> dig @129.94.242.33 yahoo.com MX

; <<>> DiG 9.9.5-9+deb8u18-Debian <<>> @129.94.242.33 yahoo.com MX
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 38935
;; flags: qr rd ra; QUERY: 1, ANSWER: 3, AUTHORITY: 5, ADDITIONAL: 10

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;yahoo.com.                     IN      MX

;; ANSWER SECTION:
yahoo.com.              1122    IN      MX      1 mta6.am0.yahoodns.net.
yahoo.com.              1122    IN      MX      1 mta7.am0.yahoodns.net.
yahoo.com.              1122    IN      MX      1 mta5.am0.yahoodns.net.

;; AUTHORITY SECTION:
yahoo.com.              8763    IN      NS      ns3.yahoo.com.
yahoo.com.              8763    IN      NS      ns5.yahoo.com.
yahoo.com.              8763    IN      NS      ns2.yahoo.com.
yahoo.com.              8763    IN      NS      ns4.yahoo.com.
yahoo.com.              8763    IN      NS      ns1.yahoo.com.

;; ADDITIONAL SECTION:
ns1.yahoo.com.          428328  IN      A       68.180.131.16
ns1.yahoo.com.          27501   IN      AAAA    2001:4998:130::1001
ns2.yahoo.com.          384130  IN      A       68.142.255.16
ns2.yahoo.com.          62254   IN      AAAA    2001:4998:140::1002
ns3.yahoo.com.          311     IN      A       27.123.42.42
ns3.yahoo.com.          186     IN      AAAA    2406:8600:f03f:1f8::1003
ns4.yahoo.com.          529675  IN      A       98.138.11.157
ns5.yahoo.com.          9135    IN      A       202.165.97.53
ns5.yahoo.com.          62254   IN      AAAA    2406:2000:ff60::53

;; Query time: 0 msec
;; SERVER: 129.94.242.33#53(129.94.242.33)
;; WHEN: Fri Mar 13 12:07:10 AEDT 2020
;; MSG SIZE  rcvd: 399
```

An authoritive answer would have the `aa` flag in the dig answer flags.  
We do not have this flag, and therefore we do not have an authoritve answer.

## Repeat the above but use one of the nameservers obtained. What is the result? 

_Using `ns3.yahoo.com`_

```
$> dig @ns3.yahoo.com yahoo.com MX

; <<>> DiG 9.9.5-9+deb8u18-Debian <<>> @ns3.yahoo.com yahoo.com MX
; (2 servers found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 5815
;; flags: qr aa rd; QUERY: 1, ANSWER: 3, AUTHORITY: 5, ADDITIONAL: 10
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1272
;; QUESTION SECTION:
;yahoo.com.                     IN      MX

;; ANSWER SECTION:
yahoo.com.              1800    IN      MX      1 mta5.am0.yahoodns.net.
yahoo.com.              1800    IN      MX      1 mta7.am0.yahoodns.net.
yahoo.com.              1800    IN      MX      1 mta6.am0.yahoodns.net.

;; AUTHORITY SECTION:
yahoo.com.              172800  IN      NS      ns2.yahoo.com.
yahoo.com.              172800  IN      NS      ns4.yahoo.com.
yahoo.com.              172800  IN      NS      ns5.yahoo.com.
yahoo.com.              172800  IN      NS      ns1.yahoo.com.
yahoo.com.              172800  IN      NS      ns3.yahoo.com.

;; ADDITIONAL SECTION:
ns1.yahoo.com.          86400   IN      AAAA    2001:4998:130::1001
ns2.yahoo.com.          86400   IN      AAAA    2001:4998:140::1002
ns3.yahoo.com.          1800    IN      AAAA    2406:8600:f03f:1f8::1003
ns5.yahoo.com.          86400   IN      AAAA    2406:2000:ff60::53
ns1.yahoo.com.          1209600 IN      A       68.180.131.16
ns2.yahoo.com.          1209600 IN      A       68.142.255.16
ns3.yahoo.com.          1800    IN      A       27.123.42.42
ns4.yahoo.com.          1209600 IN      A       98.138.11.157
ns5.yahoo.com.          86400   IN      A       202.165.97.53

;; Query time: 262 msec
;; SERVER: 2406:8600:f03f:1f8::1003#53(2406:8600:f03f:1f8::1003)
;; WHEN: Fri Mar 13 12:08:58 AEDT 2020
;; MSG SIZE  rcvd: 399
```

We now have the `aa` flag in the answer, meaning that this was an authoritive answer.

## Obtain the authoritative answer for the mail servers for Yahoo! mail. What type of DNS query is sent to obtain this information? 

From the above, the mail servers (MX records) are `mta5.am0.yahoodns.net`, `mta7.am0.yahoodns.net`, `mta6.am0.yahoodns.net`.  
A `MX` query was sent to obtain this information

## Simulate an Iterative DNS Query

> In this exercise you simulate the iterative DNS query process to find the IP address of your machine (e.g. lyre00.cse.unsw.edu.au). First, find the name server (query type NS) of the &apos;.&apos; domain (root domain). Query this nameserver to find the authoritative name server for the &apos;au.&apos; domain. Query this second server to find the authoritative nameserver for the &apos;edu.au.&apos; domain. Now query this nameserver to find the authoritative nameserver for &apos;unsw.edu.au&apos;. Next query the nameserver of unsw.edu.au to find the authoritative name server of cse.unsw.edu.au. Now query the nameserver of cse.unsw.edu.au to find the IP address of your host. How many DNS servers do you have to query to get the authoritative answer?

Using the `wagner.orchestra.cse.unsw.edu.au` machine...

|Command|Result|
|:------|:-----|
|`dig . NS`|`.                       195026  IN      NS      a.root-servers.net.`|
|`dig @a.root-servers.net au. NS`|`au.                     172800  IN      NS      a.au.`|
|`dig @a.au edu.au. NS`|`edu.au.                 86400   IN      NS      r.au.`|
|`dig @r.au unsw.edu.au NS`|`unsw.edu.au.            900     IN      NS      ns1.unsw.edu.au.`|
|`dig @ns1.unsw.edu.au cse.unsw.edu.au NS`|`cse.unsw.edu.au.        10800   IN      NS      beethoven.orchestra.cse.unsw.edu.au.`|
|`dig @beethoven.orchestra.cse.unsw.edu.au orchestra.cse.unsw.edu.au NS`|`orchestra.cse.unsw.edu.au. 3600 IN      NS      beethoven.orchestra.cse.unsw.edu.au.`|
|`dig @beethoven.orchestra.cse.unsw.edu.au wagner.orchestra.cse.unsw.edu.au`|`wagner.orchestra.cse.unsw.edu.au. 3600 IN A     129.94.242.19`|

`wagner.orchestra.cse.unsw.edu.au` points to `129.94.242.19`.  
We performed 7 queries on 6 different DNS servers to get this answer.

**Trace**

```
$> dig . NS

; <<>> DiG 9.9.5-9+deb8u18-Debian <<>> . NS
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 29980
;; flags: qr rd ra; QUERY: 1, ANSWER: 13, AUTHORITY: 0, ADDITIONAL: 27

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;.                              IN      NS

;; ANSWER SECTION:
.                       194644  IN      NS      i.root-servers.net.
.                       194644  IN      NS      b.root-servers.net.
.                       194644  IN      NS      l.root-servers.net.
.                       194644  IN      NS      j.root-servers.net.
.                       194644  IN      NS      d.root-servers.net.
.                       194644  IN      NS      g.root-servers.net.
.                       194644  IN      NS      k.root-servers.net.
.                       194644  IN      NS      h.root-servers.net.
.                       194644  IN      NS      m.root-servers.net.
.                       194644  IN      NS      a.root-servers.net.
.                       194644  IN      NS      f.root-servers.net.
.                       194644  IN      NS      c.root-servers.net.
.                       194644  IN      NS      e.root-servers.net.

;; ADDITIONAL SECTION:
a.root-servers.net.     285193  IN      A       198.41.0.4
a.root-servers.net.     316986  IN      AAAA    2001:503:ba3e::2:30
b.root-servers.net.     353811  IN      A       199.9.14.201
b.root-servers.net.     528193  IN      AAAA    2001:500:200::b
c.root-servers.net.     2136    IN      A       192.33.4.12
c.root-servers.net.     32208   IN      AAAA    2001:500:2::c
d.root-servers.net.     426837  IN      A       199.7.91.13
d.root-servers.net.     32208   IN      AAAA    2001:500:2d::d
e.root-servers.net.     178461  IN      A       192.203.230.10
e.root-servers.net.     186900  IN      AAAA    2001:500:a8::e
f.root-servers.net.     428837  IN      A       192.5.5.241
f.root-servers.net.     32208   IN      AAAA    2001:500:2f::f
g.root-servers.net.     347706  IN      A       192.112.36.4
g.root-servers.net.     327320  IN      AAAA    2001:500:12::d0d
h.root-servers.net.     286693  IN      A       198.97.190.53
h.root-servers.net.     32208   IN      AAAA    2001:500:1::53
i.root-servers.net.     15231   IN      A       192.36.148.17
i.root-servers.net.     32208   IN      AAAA    2001:7fe::53
j.root-servers.net.     35923   IN      A       192.58.128.30
j.root-servers.net.     180794  IN      AAAA    2001:503:c27::2:30
k.root-servers.net.     199829  IN      A       193.0.14.129
k.root-servers.net.     185662  IN      AAAA    2001:7fd::1
l.root-servers.net.     286910  IN      A       199.7.83.42
l.root-servers.net.     32208   IN      AAAA    2001:500:9f::42
m.root-servers.net.     173007  IN      A       202.12.27.33
m.root-servers.net.     32208   IN      AAAA    2001:dc3::35

;; Query time: 0 msec
;; SERVER: 129.94.242.2#53(129.94.242.2)
;; WHEN: Fri Mar 13 12:22:06 AEDT 2020
;; MSG SIZE  rcvd: 811

$> dig @a.root-servers.net au. NS

; <<>> DiG 9.9.5-9+deb8u18-Debian <<>> @a.root-servers.net au. NS
; (2 servers found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 43112
;; flags: qr rd; QUERY: 1, ANSWER: 0, AUTHORITY: 9, ADDITIONAL: 19
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;au.                            IN      NS

;; AUTHORITY SECTION:
au.                     172800  IN      NS      m.au.
au.                     172800  IN      NS      d.au.
au.                     172800  IN      NS      q.au.
au.                     172800  IN      NS      t.au.
au.                     172800  IN      NS      s.au.
au.                     172800  IN      NS      r.au.
au.                     172800  IN      NS      n.au.
au.                     172800  IN      NS      a.au.
au.                     172800  IN      NS      c.au.

;; ADDITIONAL SECTION:
m.au.                   172800  IN      A       156.154.100.24
m.au.                   172800  IN      AAAA    2001:502:2eda::24
d.au.                   172800  IN      A       162.159.25.38
d.au.                   172800  IN      AAAA    2400:cb00:2049:1::a29f:1926
q.au.                   172800  IN      A       65.22.196.1
q.au.                   172800  IN      AAAA    2a01:8840:be::1
t.au.                   172800  IN      A       65.22.199.1
t.au.                   172800  IN      AAAA    2a01:8840:c1::1
s.au.                   172800  IN      A       65.22.198.1
s.au.                   172800  IN      AAAA    2a01:8840:c0::1
r.au.                   172800  IN      A       65.22.197.1
r.au.                   172800  IN      AAAA    2a01:8840:bf::1
n.au.                   172800  IN      A       156.154.101.24
n.au.                   172800  IN      AAAA    2001:502:ad09::24
a.au.                   172800  IN      A       58.65.254.73
a.au.                   172800  IN      AAAA    2407:6e00:254:306::73
c.au.                   172800  IN      A       162.159.24.179
c.au.                   172800  IN      AAAA    2400:cb00:2049:1::a29f:18b3

;; Query time: 116 msec
;; SERVER: 2001:503:ba3e::2:30#53(2001:503:ba3e::2:30)
;; WHEN: Fri Mar 13 12:22:20 AEDT 2020
;; MSG SIZE  rcvd: 571

$> dig @a.au edu.au. NS

; <<>> DiG 9.9.5-9+deb8u18-Debian <<>> @a.au edu.au. NS
; (2 servers found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 60489
;; flags: qr rd; QUERY: 1, ANSWER: 0, AUTHORITY: 4, ADDITIONAL: 9
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;edu.au.                                IN      NS

;; AUTHORITY SECTION:
edu.au.                 86400   IN      NS      q.au.
edu.au.                 86400   IN      NS      t.au.
edu.au.                 86400   IN      NS      r.au.
edu.au.                 86400   IN      NS      s.au.

;; ADDITIONAL SECTION:
q.au.                   86400   IN      A       65.22.196.1
r.au.                   86400   IN      A       65.22.197.1
s.au.                   86400   IN      A       65.22.198.1
t.au.                   86400   IN      A       65.22.199.1
q.au.                   86400   IN      AAAA    2a01:8840:be::1
r.au.                   86400   IN      AAAA    2a01:8840:bf::1
s.au.                   86400   IN      AAAA    2a01:8840:c0::1
t.au.                   86400   IN      AAAA    2a01:8840:c1::1

;; Query time: 161 msec
;; SERVER: 2407:6e00:254:306::73#53(2407:6e00:254:306::73)
;; WHEN: Fri Mar 13 12:22:30 AEDT 2020
;; MSG SIZE  rcvd: 275

$> dig @r.au unsw.edu.au NS

; <<>> DiG 9.9.5-9+deb8u18-Debian <<>> @r.au unsw.edu.au NS
; (2 servers found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 15654
;; flags: qr rd; QUERY: 1, ANSWER: 0, AUTHORITY: 3, ADDITIONAL: 6
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;unsw.edu.au.                   IN      NS

;; AUTHORITY SECTION:
unsw.edu.au.            900     IN      NS      ns2.unsw.edu.au.
unsw.edu.au.            900     IN      NS      ns1.unsw.edu.au.
unsw.edu.au.            900     IN      NS      ns3.unsw.edu.au.

;; ADDITIONAL SECTION:
ns1.unsw.edu.au.        900     IN      AAAA    2001:388:c:35::1
ns2.unsw.edu.au.        900     IN      AAAA    2001:388:c:35::2
ns1.unsw.edu.au.        900     IN      A       129.94.0.192
ns2.unsw.edu.au.        900     IN      A       129.94.0.193
ns3.unsw.edu.au.        900     IN      A       192.155.82.178

;; Query time: 20 msec
;; SERVER: 2a01:8840:bf::1#53(2a01:8840:bf::1)
;; WHEN: Fri Mar 13 12:22:39 AEDT 2020
;; MSG SIZE  rcvd: 198

$> dig @ns1.unsw.edu.au cse.unsw.edu.au NS

; <<>> DiG 9.9.5-9+deb8u18-Debian <<>> @ns1.unsw.edu.au cse.unsw.edu.au NS
; (2 servers found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 44014
;; flags: qr rd; QUERY: 1, ANSWER: 0, AUTHORITY: 2, ADDITIONAL: 5
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;cse.unsw.edu.au.               IN      NS

;; AUTHORITY SECTION:
cse.unsw.edu.au.        10800   IN      NS      maestro.orchestra.cse.unsw.edu.au.
cse.unsw.edu.au.        10800   IN      NS      beethoven.orchestra.cse.unsw.edu.au.

;; ADDITIONAL SECTION:
beethoven.orchestra.cse.unsw.edu.au. 10800 IN A 129.94.172.11
beethoven.orchestra.cse.unsw.edu.au. 10800 IN A 129.94.208.3
beethoven.orchestra.cse.unsw.edu.au. 10800 IN A 129.94.242.2
maestro.orchestra.cse.unsw.edu.au. 10800 IN A   129.94.242.33

;; Query time: 4 msec
;; SERVER: 2001:388:c:35::1#53(2001:388:c:35::1)
;; WHEN: Fri Mar 13 12:22:48 AEDT 2020
;; MSG SIZE  rcvd: 164

$> dig @beethoven.orchestra.cse.unsw.edu.au orchestra.cse.unsw.edu.au NS

; <<>> DiG 9.9.5-9+deb8u18-Debian <<>> @beethoven.orchestra.cse.unsw.edu.au orchestra.cse.unsw.edu.au NS
; (3 servers found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 57788
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 3

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;orchestra.cse.unsw.edu.au.     IN      NS

;; ANSWER SECTION:
orchestra.cse.unsw.edu.au. 3600 IN      NS      beethoven.orchestra.cse.unsw.edu.au.
orchestra.cse.unsw.edu.au. 3600 IN      NS      maestro.orchestra.cse.unsw.edu.au.

;; ADDITIONAL SECTION:
maestro.orchestra.cse.unsw.edu.au. 3600 IN A    129.94.242.33
beethoven.orchestra.cse.unsw.edu.au. 3600 IN A  129.94.242.2

;; Query time: 0 msec
;; SERVER: 129.94.242.2#53(129.94.242.2)
;; WHEN: Fri Mar 13 12:23:02 AEDT 2020
;; MSG SIZE  rcvd: 132

$> dig @beethoven.orchestra.cse.unsw.edu.au wagner.orchestra.cse.unsw.edu.au 

; <<>> DiG 9.9.5-9+deb8u18-Debian <<>> @beethoven.orchestra.cse.unsw.edu.au wagner.orchestra.cse.unsw.edu.au
; (3 servers found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 43276
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 2, ADDITIONAL: 3

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;wagner.orchestra.cse.unsw.edu.au. IN   A

;; ANSWER SECTION:
wagner.orchestra.cse.unsw.edu.au. 3600 IN A     129.94.242.19

;; AUTHORITY SECTION:
orchestra.cse.unsw.edu.au. 3600 IN      NS      beethoven.orchestra.cse.unsw.edu.au.
orchestra.cse.unsw.edu.au. 3600 IN      NS      maestro.orchestra.cse.unsw.edu.au.

;; ADDITIONAL SECTION:
maestro.orchestra.cse.unsw.edu.au. 3600 IN A    129.94.242.33
beethoven.orchestra.cse.unsw.edu.au. 3600 IN A  129.94.242.2

;; Query time: 1 msec
;; SERVER: 129.94.242.2#53(129.94.242.2)
;; WHEN: Fri Mar 13 12:23:18 AEDT 2020
;; MSG SIZE  rcvd: 155
```

## Can one physical machine have several names and/or IP addresses associated with it? 

Yes, a machine can have several hostnames / DNS names associated with it.  
Additionally, a machine can have several IP addresses (i.e. several network cards on the same machine).


# A Simple Web Server

