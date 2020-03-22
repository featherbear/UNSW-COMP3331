---
title: "DNS"
date: 2020-03-22T19:23:16+11:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

# Domain Name System

Humans are forgetful, and we can't remember arbitrary numbers easily, let alone IP addresses.

The DNS allows us to type in `facebook.com`, and automagically connect to the servers which are hosting Facebook, without needing to know the IP address!

---

## Distributed Database

There are many name servers in the world, and they work together (as a sort of hierarchy) to resolve hostnames into IP addresses.

In fact your computer has its own "server", a local resolver which your computer first contacts before reaching other DNS servers.

The DNS system is decentralised, as it will not scale well if every single device in the world were to contact the same machine.

## Other Uses

DNS servers are not only used to translate hostnames into IP addresses, they can also be used to point to machines with _dynamic IP addresses_ (ie they keep changing). Furthermore, they can be used as _load balancers_ - to direct users to different redundant servers, or perhaps closer servers.

## The Protocol

DNS is part of the Application Layer protocol, and uses the UDP protocol. (Though there are developments with DoH - DNS over HTTPS)

## Hierarchical Look

![](Screenshot from 2020-03-22 19-31-59.png)
![](Screenshot from 2020-03-22 19-32-29.png)

Root Servers -> TLDs -> Authoritative Servers

### Root Servers

There are 13 root servers throughout the world, that are responsible for pointing to the TLDs 

### Top-Level Domains (TLD)

These servers are responsible for `.com`, `.org`, `.edu`, etc domains, as well as country domains `.au`, `.uk`, etc.

### Authoritative Servers

The rest of the servers fall into this category (ie for companies, schools)

## Iterative vs Recursive Queries

For iterative queries, servers will tell the client the next server to contact to try to resolve the hostname.  

For recursive queries, the servers themselves will try to resolve the hostname to IP addresses (by performing their own queries).  
The client will then only need to contact this one server. A possible drawback, is that the client will not have any feedback from the server until it has replied.

## DNS Caching

To prevent the request for the same host name requiring the DNS server to contact other DNS servers every time; DNS servers cache their results - for a period of time given by a record's TTL (Time To Live) value (in seconds).

If a domain record changes before the TTL expires, your computer/local dns server may not reflect those changes (Without forcing a flush)

## DNS Replies - Authoritative Replies

Sometimes a DNS reply may return DNS records that belong to other DNS servers. When using `dig`, you should have a look to see if the `aa` (authoritative) flag is set.

## Resource Records

DNS records are known as **Resource Records**.

(`name`, `value`, `type`, `ttl`)

### Format

![](Screenshot from 2020-03-22 19-40-48.png)
![](Screenshot from 2020-03-22 19-40-59.png)

* DNS Query and Reply messages share the **same message format**.
* The identification segment is a 16-bit number
  * The reply to a query uses the same number
* Flags are used to mark the type and content of the query/reply

## Reverse DNS

* Maps an IP to a hostname
* Uses `PTR` records

These records are stored to assist troubleshooting tools (traceroute, ping), to validate SMTP servers, load balancing, and for many other purposes.
