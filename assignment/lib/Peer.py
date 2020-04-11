from . import portUtils

import socket
import threading
import time
from select import select
import re
import sys
import os.path

SHOW_PING_REQUEST = True
SHOW_PING_RESPONSE = True
SHOW_CUSTOM_DEBUG = False

"""
DHT P2P Client and Server
"""

class Peer:
    def __init__(self, peer_id: int, ping_interval: int):
        self.__id = peer_id

        self.first_successor = None
        self.second_successor = None
        self.first_predecessor = None
        self.second_predecessor = None

        self.ping_interval = ping_interval

        self.isConnected = False
        self.___readyCallback = None

        self.__lastPing = 0
        self.__pingInfo = {}

        self._connections = []
        self._connectionsMetadata = {}

        if SHOW_CUSTOM_DEBUG: self.__dprint(f"I am Peer #{self.id}")

        # Start TCP Server and UDP Ping Server
        threading.Thread(target=self.__serverFn, daemon=True).start()
        threading.Thread(target=self.__pingServerFn, daemon=True).start()
        
    def __repr__(self):
        return f"<Peer[{self.id}]->{self.first_successor}->{self.second_successor}>"
    
    """
    Send a TCP message in a new connection
    """
    def ___sendTCP(self, peerID: int, data):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(('127.0.0.1', portUtils.calculate_port(peerID)))
        conn.sendall(data)
        conn.close()

    """
    Close a TCP connection
    """
    def ___closeTCP(self, conn: socket.socket) -> bool:
        if conn in self._connections:

            # Remove any associated connection metadata
            metadata = self._connectionsMetadata.get(conn, False)
            if metadata:
                if "fileHandle" in metadata:
                    metadata["fileHandle"].close()
                del self._connectionsMetadata[conn]
            
            self._connections.remove(conn)
            conn.close()
            return True

        return False

    """
    JOIN command entry point
    """
    def join(self, known_peer: int, *, callback = None):
        # Abort if already connected
        if self.isConnected:
            return False
        
        # Set up callback
        if callback is not None:
            self.___readyCallback = callback

        # Send join request to the known peer
        self.___sendTCP(known_peer, f"join|{self.id}".encode())

    """
    INIT command entry point
    """
    def setup(self, first_successor: int, second_successor: int, *, callback = None):
        
        # Set up callback
        if callback is not None:
            self.___readyCallback = callback

        self.first_successor = first_successor
        self.second_successor = second_successor
        self.isConnected = True

    """
    Execute ready events
    * UDP Ping Client
    * (optional) Callback
    """
    def ready(self):
        threading.Thread(target=self.__pingClientFn, daemon=True).start()
        
        # Execute callback
        if self.___readyCallback is not None:
            self.___readyCallback(self)
            self.___readyCallback = None

    """
    TCP Server thread function
    """
    def __serverFn(self):
        self.__serverRunning = True
        LISTEN_PORT = portUtils.calculate_port(self.id)
        
        # Set up socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('', LISTEN_PORT))
        server.listen()
        if SHOW_CUSTOM_DEBUG: self.__dprint(f"Listening for connections on TCP:{LISTEN_PORT}")

        while self.__serverRunning:

            # Check for readable connections
            for readableSock in select([server, *self._connections], [], [], 1)[0]:
                
                # If the connection is a new connection, add it to the queue of future connections
                if readableSock is server:
                    (sock, addr) = server.accept()
                    self._connections.append(sock)
                    # Read from this socket on the next `select`
                    continue
            
                # Read for data
                data = readableSock.recv(1024)

                # Close and remove dead connections                
                if not data:
                    self.___closeTCP(readableSock)
                    continue

                # Check if the socket is for file transfer
                if readableSock in self._connectionsMetadata:
                    metadata = self._connectionsMetadata[readableSock]

                    # Write data into the file handle
                    metadata["bytesLeft"] -= metadata["fileHandle"].write(data)
                    
                    # Check if the transfer is finished
                    if metadata["bytesLeft"] == 0:
                        self.__dprint(f"File {metadata['filename']} received")
                        metadata["fileHandle"].close()
                        del self._connectionsMetadata[readableSock]

                    continue

                ##################################################
                # Now parse commands
                ##################################################

                info = data.split(b"|")
                command = info[0].decode().lower()

                # Handle join requests
                if command == "join":
                    info = [*map(lambda b: b.decode(), info)]
                    newPeerID = int(info[1])

                    # Drop request if new peer claims to be an existing peer
                    if newPeerID in [self.id, self.first_successor, self.second_successor]:
                        if SHOW_CUSTOM_DEBUG: self.__dprint(f"> Peer {newPeerID} trying to join, but peer ID conflicts")
                        self.___closeTCP(readableSock)
                        continue

                    if newPeerID > self.id:
                        # Check if the current node is the appropriate peer to service the join request
                        if newPeerID < self.first_successor or self.first_successor < self.id:
                            self.__dprint(f"> Peer {newPeerID} Join request received")
                            
                            # Send the joining peer an offer
                            self.___sendTCP(newPeerID, f"offer|{self.first_successor}|{self.second_successor}".encode())

                            # Update the second successor of the node's predecessor, to the ID of the new peer
                            if self.first_predecessor is not None:
                                self.___sendTCP(self.first_predecessor, f"secondsuccessor|{newPeerID}".encode())

                            # Update the current node's successors
                            self.second_successor = self.first_successor
                            self.first_successor = newPeerID
                            self.__dprint(f"> My first successor is Peer {self.first_successor}")
                            self.__dprint(f"> My second successor is Peer {self.second_successor}")

                        # Else forward the request
                        else:
                            """ # This block will enable DHT shortcuts, but is disabled as it will violate assignment specifications """
                            # if newPeerID > self.first_successor:
                            #     self.___sendTCP(self.second_successor, data)
                            # else:
                            #    self.___sendTCP(self.first_successor, data)
                            """ # END """

                            self.___sendTCP(self.first_successor, data)
                            self.__dprint(f"> Peer {newPeerID} Join request forwarded to my successor")
                
                # Handle network join offers
                elif command == "offer":
                    # Ignore offer if already connected
                    if self.isConnected:
                        continue

                    info = [*map(lambda b: b.decode(), info)]

                    # Initialise the peer
                    self.setup(*map(int, info[1:]))

                    self.__dprint("> Join request has been accepted")
                    self.__dprint(f"> My first successor is Peer {self.first_successor}")
                    self.__dprint(f"> My second successor is Peer {self.second_successor}")

                    self.isConnected = True
                    self.ready()

                # Force-update the second successor
                elif command == "secondsuccessor":
                    info = [*map(lambda b: b.decode(), info)]
                    
                    self.second_successor = int(info[1])

                    self.__dprint(f"> Successor Change request received")
                    self.__dprint(f"> My new first successor is Peer {self.first_successor}")
                    self.__dprint(f"> My new second successor is Peer {self.second_successor}")
                
                # Handle store command
                elif command == "store":
                    info = [*map(lambda b: b.decode(), info)]
                    if len(info) == 3:
                        self.store(info[1], info[2])

                # Handle request command
                elif command == "request":
                    info = [*map(lambda b: b.decode(), info)]
                    if len(info) == 3:
                        self.request(info[1], info[2])

                # Handle incoming file reception
                elif command == "file":
                    _, peer, filename, dataLength, data = data.split(b"|", 4)
                    
                    peer = peer.decode()
                    filename = filename.decode()
                    dataLength = int(dataLength.decode())
                    
                    self.__dprint(f"> Peer {peer} had File {filename}")
                    self.__dprint(f"> Receiving File {filename} from Peer {peer}")
                    
                    f = open(f"received_{filename}.pdf", "wb")

                    # Create metadata structure
                    metadata = dict(
                        filename = filename,
                        fileHandle = f,
                        bytesLeft = dataLength,
                    )

                    metadata["bytesLeft"] -= f.write(data)
                    self._connectionsMetadata[readableSock] = metadata

                # Handle disconnect messages
                elif command == "quit":
                    info = [*map(lambda b: b.decode(), info)]
                    peer, first_successor, second_successor = map(int,info[1:4])

                    self.__dprint(f"> Peer {peer} will depart from the network")

                    # Reassign successors
                    if peer == self.first_successor:
                        self.first_successor = first_successor
                        self.second_successor = second_successor
                    elif peer == self.second_successor:
                        self.second_successor = first_successor
                    
                    # Ping first successor for any updates
                    self.__sendPing(peerID = self.first_successor)

                    self.__dprint(f"> My new first successor is Peer {self.first_successor}")
                    self.__dprint(f"> My new second successor is Peer {self.second_successor}")
                    
        server.close()

    """
    UDP Ping Server thread function
    """
    def __pingServerFn(self):
        self.__pingServerRunning = True
        LISTEN_PORT = portUtils.calculate_port(self.id)
        
        # Set up the server
        self.___pingServer = server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('', LISTEN_PORT))
        if SHOW_CUSTOM_DEBUG: self.__dprint(f"Listening for ping requests on UDP:{LISTEN_PORT}")

        while self.__pingServerRunning:
            # Wait for new messages
            if select([server], [], [], 1)[0]:
                (data, addr) = server.recvfrom(1024)
                info = data.decode().split("|")

                SHOW_PING_REQUEST and self.__dprint(f"> Ping request message received from Peer {info[0]}")

                # Check for the first predecessor
                if len(info) > 1 and int(info[1]) == self.id:
                    if self.first_predecessor is None:
                        if SHOW_CUSTOM_DEBUG: self.__dprint("> Circular DHT established")
                    self.first_predecessor = int(info[0])
                
                # Check for the second predecessor
                if len(info) > 2 and int(info[2]) == self.id:
                    if self.second_predecessor is None:
                        if SHOW_CUSTOM_DEBUG: self.__dprint("> Second predecessor determined")
                    self.second_predecessor = int(info[0])
                
                # Craft the response message
                string = f"{self.id}"
                if self.first_successor: string += f"|{self.first_successor}"
                if self.second_successor: string += f"|{self.second_successor}"
                
                server.sendto(string.encode(), addr)
        
        server.close()

    """
    Function stub to send ping messages
    Gets overridden when __pingClientFn spawns
    """
    def __sendPing(self, *, peerID=None, ctime=None):
        raise NotImplementedError("STUB")

    """
    UDP Ping Client thread function
    """
    def __pingClientFn(self):
        # Set up the UDP socket
        c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Create sendPing function bounded to the created UDP socket
        def sendPing(*, peerID=None, ctime=None):
            if ctime is None:
                ctime = time.time()
            if peerID is None:
                self.__lastPing = ctime
            for peerID in [peerID] if peerID else [self.first_successor, self.second_successor]:
                if peerID is not None:
                    string = f"{self.id}"
                    if self.first_successor: string += f"|{self.first_successor}"
                    if self.second_successor: string += f"|{self.second_successor}"
                    c.sendto(string.encode(), ('localhost', portUtils.calculate_port(peerID)))

        # Assign function to the class scope
        self.__sendPing = sendPing

        while True:

            # Check if a new periodic ping is needed
            ctime = time.time()
            if ctime - self.__lastPing > self.ping_interval:
                sendPing(ctime=ctime)

                # Format print message
                if SHOW_PING_REQUEST:
                    pingList = [s for s in [self.first_successor, self.second_successor] if s is not None]
                    if len(pingList) > 0:
                        self.__dprint(f"> Ping requests sent to Peer{'s' if len(pingList) == 2 else ''} {' and '.join(map(str, pingList))}")

            # Check for replies
            while select([c], [], [], 10)[0]:
                (data, addr) = c.recvfrom(1024)
                info = data.decode().split("|")
                info = [*map(int, info)]

                try:
                    self.__pingInfo[info[0]] = time.time()
                    SHOW_PING_RESPONSE and self.__dprint(f"> Ping response received from Peer {info[0]}")

                    # Update second successor if currently unset / cleared
                    if info[0] == self.first_successor and self.second_successor is None:
                        self.second_successor = info[1]
                        
                # Ignore errors
                except:
                    pass

            # Check if last response was a while ago
            ctime = time.time()
            for peerID in [self.first_successor, self.second_successor]:
                if peerID is None:
                    continue
                if peerID not in self.__pingInfo: 
                    self.__pingInfo[peerID] = ctime
                    continue
                if ctime - self.__pingInfo[peerID] < min(max(20, self.ping_interval * 4), 60):
                    # Allow at least 20 seconds, at most 60 seconds
                    continue

                self.__dprint(f"> Peer {peerID} is no longer alive")

                # NOTE: DO NOT REFACTOR - It is clearer to leave like this
                if peerID == self.first_successor:
                    self.first_successor = self.second_successor
                    self.second_successor = None
                    self.__sendPing(peerID = self.first_successor)
                else: # peerID == self.second_successor
                    self.second_successor = None
                    self.__sendPing(peerID = self.first_successor)

    """
    Handle storing
    """
    def store(self, filename, requestor=None):
        requestor = requestor or self.id

        # Validate filename
        # FIXME: Possibly ^\d{4}$
        if not re.match("^\d{1,4}$", filename):
            if SHOW_CUSTOM_DEBUG: self.__dprint("> Invalid filename '{filename}'")
            return False
  
        _filename = int(filename)
        _hash = _filename % 256

        # Check if the current node is the appropriate handler
        if any([
            _hash == self.id,
            self.first_predecessor and self.id < self.first_predecessor and (_hash > self.first_predecessor or _hash < self.id),
            self.first_predecessor and _hash > self.first_predecessor and _hash < self.id
        ]):
            self.__dprint(f"> Store {_filename} request accepted")
            open(f"{_filename}.pdf", "w").close()
        
        # Forward the request
        else:
            self.__dprint(f"> Store {_filename} request forwarded to my successor")

            """ # This block will enable DHT shortcuts, but is disabled as it will violate assignment specifications """
            # if hash > self.first_successor:
            #     self.___sendTCP(self.second_successor, f"store|{_filename}|{requestor}".encode())
            # else:
            #     self.___sendTCP(self.first_successor, f"store|{_filename}|{requestor}".encode())
            """ # END """
            self.___sendTCP(self.first_successor, f"store|{_filename}|{requestor}".encode())

    def request(self, filename, requestor=None):
        requestor = requestor or self.id

        # Validate filename
        # FIXME: Possibly ^\d{4}$
        if not re.match("^\d{1,4}$", filename):
            if SHOW_CUSTOM_DEBUG: self.__dprint("> Invalid filename '{filename}'")
            return False
  
        _filename = int(filename)
        _hash = _filename % 256

        _requestor = int(requestor)

        # Check if the current node is the appropriate handler
        if any([
            _hash == self.id,
            self.first_predecessor and self.id < self.first_predecessor and (_hash > self.first_predecessor or _hash < self.id),
            self.first_predecessor and _hash > self.first_predecessor and _hash < self.id
        ]):

            self.__dprint(f"> File {filename} is stored here")

            if self.id == _requestor:
                return

            self.__dprint(f"> Sending file {filename} to Peer {_requestor}")
            self.sendFile(_requestor, filename.zfill(4))
        
        # Forward the request
        else:
            if self.id == requestor:
                self.__dprint(f"> File request for {filename} has been sent to my successor")
            else:
                self.__dprint(f"> Request for File {filename} has been received, but the file is not stored here")

            """ # This block will enable DHT shortcuts, but is disabled as it will violate assignment specifications """
            # if hash > self.first_successor:
            #     self.___sendTCP(self.second_successor, f"request|{filename}|{requestor}".encode())
            # else:
            #     self.___sendTCP(self.first_successor, f"request|{filename}|{requestor}".encode())
            """ # END """
            self.___sendTCP(self.first_successor, f"request|{filename}|{requestor}".encode())

    """
    Send [filename].pdf to peerID

    [filename].pdf MUST exist
    """
    def sendFile(self, peerID: int, filename: str):
        path = filename + ".pdf"
        
        # Abort if the file does not exist
        if not os.path.exists(path) or not os.path.isfile(path):
            self.__dprint(f"> The physical file at {path} was requested, but does not exist or is an invalid file!")
            return

        # Read and send the file
        with open(path, "rb") as f:
            data = f.read()
            dataLength = len(data) # struct pack me?

            self.___sendTCP(peerID, f"file|{self.id}|{filename}|{dataLength}|".encode() + data)
            
        self.__dprint("> The file has been sent")

    """
    Exit the network
    """
    def quit(self):
        payload = f"quit|{self.id}|{self.first_successor}|{self.second_successor}".encode()

        # Notify predecessors
        if self.first_predecessor is not None: self.___sendTCP(self.first_predecessor, payload)
        if self.second_predecessor is not None: self.___sendTCP(self.second_predecessor, payload)
        
        self.__serverRunning = False
        self.__pingServerRunning = False

    @property
    def id(self):
        return self.__id

    # Override me!
    def __dprint(self, *args, **kwargs):
        print(*args, **kwargs)
