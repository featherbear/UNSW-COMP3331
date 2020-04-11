#!/usr/bin/python3

PING_INTERVAL = 3
REPORTER_INTERVAL = 1

"""
Set the nodes to launch here

Format: (id, first_successor, second_successor)
The ping interval is set by the PING_INTERVAL global
"""
nodes = [
    # ID 1st 2nd
    ( 2,  4,  5),
    ( 4,  5,  8),
    ( 5,  8,  9),
    ( 8,  9, 14),
    ( 9, 14, 19),
    (14, 19,  2),
    (19,  2,  4)
]

#######################################

import sys; REPORTER = "-r" in sys.argv
from lib.Peer import Peer

# Set up the reporter if enabled with the `-r` flag
if REPORTER:
    from lib.Reporter import Reporter
    reporter = Reporter(REPORTER_INTERVAL)

"""
Peer init function
"""
def _setup(PEER: int, FIRST_SUCCESSOR: int, SECOND_SUCCESSOR: int, PING_INTERVAL: int):
    peer = Peer(PEER, PING_INTERVAL)
    peer.setup(FIRST_SUCCESSOR, SECOND_SUCCESSOR)
    if REPORTER: reporter.register(peer)

    # Override <Peer>.__dprint function to insert the peer's ID for output clarity
    peer._Peer__dprint = lambda *args, **kwargs: print(f"[{peer.id}]", *args, **kwargs)

    return peer

# Initialise the peers
nodes = [*map(lambda nodeInfo: _setup(*nodeInfo, PING_INTERVAL), nodes)]

print("Launching nodes:", "".join([f"\n■ {n}" for n in nodes]), "\n")

# Start the peers
for node in nodes: node.ready()

# Start the reporter if enabled
if REPORTER: reporter.run()

import time
while True:
    time.sleep(0.1)