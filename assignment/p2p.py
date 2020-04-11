#!/usr/bin/python3.7

from lib.Peer import Peer
from lib.argParser import _
import sys
import time

import threading

ID_SPACE = 256

if __name__ == "__main__":

    # Validate and parse
    args = _(ID_SPACE) or sys.exit(1)

    # Ready flag to signify acceptance of user input
    ready = False
    def callback(*_, **__):
        global ready
        ready = True

    # Start a peer in JOIN mode
    if args[0] == "join":
        PEER, KNOWN_PEER, PING_INTERVAL = args[1:]
        p = Peer(PEER, PING_INTERVAL)
        p.join(KNOWN_PEER, callback=callback)
        
    # Start a peer in INIT mode
    elif args[0] == "init":
        PEER, FIRST_SUCCESSOR, SECOND_SUCCESSOR, PING_INTERVAL = args[1:]
        p = Peer(PEER, PING_INTERVAL)
        p.setup(FIRST_SUCCESSOR, SECOND_SUCCESSOR, callback=callback)
        p.ready()
        
    print("Launched peer:", p)
    
    # Wait until peer is ready
    while not ready:
        time.sleep(0.5)

    line = None
    def getLine(prompt: str) -> str:
        global line
        line = input(prompt)
        return line or " "
    
    # Parse commands
    while getLine("> "):
        tokens = line.split(" ")
        command = tokens[0].lower()
        if command == "store":
            # Pre command validation
            if len(tokens) != 2:
                print("Usage: Store <4-digit filename>")
                continue

            p.store(tokens[1])
            continue

        if command == "request":
            # Pre command validation
            if len(tokens) != 2:
                print("Usage: Request <4-digit filename>")
                continue

            p.request(tokens[1])
            continue

        if command == "quit":
            # If the predecessors have never pinged this node, then the node will not be able to send a disconnect message to them
            # Signify the user (or the marker) that they may need to wait a bit longer before quitting, for the graceful leave to work.
            if p.first_predecessor is None or p.second_predecessor:
                print("Circular DHT was not fully established. Perhaps the predecessors haven't pinged you yet?")
                print("Disconnect message NOT sent")

            p.quit()
            sys.exit()
