---
title: "Cyclic Redundancy Checks"
date: 2020-05-06T17:02:21+10:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

A Cyclic Redundancy Check is a powerful error-detection coding.  

A CRC check is performed in the Ethernet and 802.11 WiFi frame.  
For a `CRC-n` check, `n+1` bits are used in the generator bit pattern `G`.

# TLDR

* Append `n` bits to the data `D`
* Divide `D` with `G` (align the first '1', then XOR)
* Continue until the remainder is given

* `R == 0` - successful verification
* `R != 0` - data has been corrupted

---

> http://www.sunshine2k.de/articles/coding/crc/understanding_crc.html

```
Input data is the byte 0xC2 = b11000010.
As generator polynomial (=divisor), let's use b100011101.
The divisor has 9 bits (therefore this is a CRC-8 polynomial), so append 8 zero bits to the input pattern.
Align the leading '1' of the divisor with the first '1' of the dividend and perform a step-by-step school-like division, using XOR operation for each bit:

ABCDEFGHIJKLMNOP
1100001000000000
100011101
---------
010011001
 100011101
 ----------
 000101111
    100011101           (*)
    ---------
    001100101
      100011101
      ---------
      010001001
       100011101
       ---------
       000001111 = 0x0F
ABCDEFGHIJKLMNOP
```

---

* http://www.cs.jhu.edu/~scheideler/courses/600.344_S02/CRC.html  