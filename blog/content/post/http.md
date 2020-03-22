---
title: "Http"
date: 2020-03-10T20:46:55+11:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

# History of HTTP

HTTP 0 - 1990  
HTTP/0.9 - 1991  
HTTP/1.0 - 1992 - simple caching  
HTTP/1.1 - 1996  
HTTP/2.0 - 2015

---

# HTTP Overview

* **H**yper**T**ext **T**ransfer **P**rotocol
* [Client-Server Model](../application-communication#client-server-architecture)
* Generally operates on port 80 and 443 (SSL)
* Uses TCP as the underlying transport layer
* Stateless
  * Server maintains no information about past requests from a given client
* General flow
  * TCP connection opened
  * Server accepts conncetion
  * HTTP messages exchanged
  * TCP connection closed
* Entirely text-based
* Not very efficient though
  * the string "12345678" -> 8 bytes
  * the integer 12345678 -> 4 bytes
  * headers do not have any guaranteeed order
  * requires strings to be parsed

## HTTP Requests

```
GET /index.html HTTP/1.1\r\n
Host: www-net.cs.umass.edu\r\n
User-Agent: Firefox/3.6.10\r\n
Accept: text/html,application/xhtml+xml\r\n
Accept-Language: en-us,en;q=0.5\r\n
Accept-Encoding: gzip,deflate\r\n
Accept-Charset: ISO-8859-1,utf-8;q=0.7\r\n
Keep-Alive: 115\r\n
Connection: keep-alive\r\n
\r\n
```

* All lines in the request are followed by a `\r\n`
* First line has the request
  * GET / POST / HEAD / etc...
  * Path
  * Protocol version
* `Header`: `Value`
* The request is terminated with another `\r\n`

## HTTP Response

```
HTTP/1.1 200 OK\r\n
Date: Sun, 26 Sep 2010 20:09:20 GMT\r\n
Server: Apache/2.0.52 (CentOS)\r\n
Last-Modified: Tue, 30 Oct 2007 17:00:02 GMT\r\n
ETag: "17dc6-a5c-bf716880"\r\n
Accept-Ranges: bytes\r\n
Content-Length: 2652\r\n
Keep-Alive: timeout=10, max=100\r\n
Connection: Keep-Alive\r\n
Content-Type: text/html; charset=ISO-8859-1\r\n
\r\n
data data data data data ...
```

* HTTP header sent with optional response
  * Header ends with a `\r\n` before the data is sent

## Cookies

Cookies are pieces of text stored on the client's browser. These cookies are sent to the server whenever a request is made, and helps to track and identify who the client is (Remember, HTTP is stateless!)

They are stored on the client as `Set-Cookie` headers in [HTTP Responses](#http-response)

## Measuring HTTP Performance

The **Page Load Time** (PLT) is the timing metric, from when the user clicks on a link, to when the client sees the page.

It depends on factors such as the page's content/structure; the protocols involved; and the network environment (bandwidth and RTT)

### Improving PLT

* Reduce transfer sizes
  * Smaller images
  * Compression
    * Compression of text, images (ie lossy vs lossless)
* Change how HTTP works
  * Persistent Connections
    * Instead of a new TCP connection being created for each resource; reuse the same connection
    * Reduces RTT from TCP connection setup
    * Allows TCP to learn more accurate RTT estimates
    * Allows TCP congestion window to increase
    * Leverage previously discovered bandwidth
  * Pipelining (HTTP/1.1)
    * Request for multiple resources within the same request
    * Reduces the number of RTT
* Change where the response come from
  * Caches and Web Proxies 
    * Store copies of the server response
    * Has file-newness implications
    * `ETag` header - identifier of version of a resource
      * Can use the Conditional GET header `If-Modified-Since: <ETag>`
  * CDNs
    * Move the content closer to the user
    * Pull - Local CDN pulls the resource when requested
    * Push - CDNs distribute resources, expecting it to be accessed

## HTTPS

HTTP over Transport Layer Security (TLS)

## HTTP/2.0

Googly SPDY (pronounced Speedy) - RFC7540

* Better structure of contents
* Servers can push new content out
* Multiplexed requets and responses 
* Overcomes head-of-line blocking seen in HTTP/1.1
* Resource request prioritisation
* Compression of HTTP headers
