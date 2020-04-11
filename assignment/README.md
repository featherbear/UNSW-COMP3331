# UNSW COMP3331 20T1 Assignment - Distributed Hash Table

## Overview

This repository contains Python 3 code towards building a basic Distributed Hash Table network; which implements rudimentary peer management and data transfer services.

* The assignment specifications can be found in [Assignment_3331_9331_20T1_updated_ver.pdf](./Assignment_3331_9331_20T1_updated_ver.pdf)
* The marking rubric can be found in [assignement_marking_rubric_student.pdf](./assignement_marking_rubric_student.pdf)
* The report can be found in [report.pdf](./report.pdf)

## Usage

### P2P Client - `p2p.py`

The `p2p.py` file is the main entry point to the program

#### Initialising nodes of a new network

Usage: `python3 p2p.py join <PEER> <FIRST_SUCCESSOR> <SECOND_SUCCESSOR> <PING_INTERVAL>`

#### Joining an existing network

Usage: `python3 p2p.py join <PEER> <KNOWN_PEER> <PEER_INTERVAL>`

### Network Launcher - `runner.py`

The `runner.py` file initialises a network with 7 nodes, with a default ping interval of 3 seconds.  
_(2, 4, 5, 8, 9, 14 and 19_ as per the assignment outline)_

Usage: `python3 runner.py`

#### Reporter Mode

If launched with the `-r` flag, the reporter mode is entered.  
Each node initialised with the launcher will be inspected for their predecessors and successors.

Usage: `python3 runner.py -r`

