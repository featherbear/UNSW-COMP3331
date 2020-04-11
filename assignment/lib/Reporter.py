from .Peer import Peer
import time
import sys
import os
import threading


"""
Reporter class to provide an overview report of the predecessors and successors of monitored peers.
"""
class Reporter:
    def __init__(self, refreshInterval, suppressOutput = True):

        self.peers = []
        self.refreshInterval = refreshInterval
        self.__maxLength = 2 # Start with 2-width characters
        self.suppressOutput = suppressOutput

    def run(self):
        thread = threading.Thread(target=self.___run).start()

    """
    Thread function
    """
    def ___run(self):
        if self.suppressOutput: sys.stdout = open(os.devnull, 'w')

        # Pad text to be nicely formatted
        def __prettyConvert(truthyValue): return str(truthyValue).rjust(self.__maxLength) if truthyValue else "?"*self.__maxLength

        while True:
            builder = []
            builder.append("==================================")

            unmonitoredPeers = []
            successors = []
            
            for peer in self.peers:
                # Get IDs and format as prettified text

                _id = __prettyConvert(self._id_passthrough(peer.id))

                __first_predecessor = __prettyConvert(self._id_passthrough(peer.first_predecessor))
                __second_predecessor = __prettyConvert(self._id_passthrough(peer.second_predecessor))
                
                __first_successor = self._id_passthrough(peer.first_successor)
                successors.append(__first_successor)
                _first_successor = __prettyConvert(__first_successor)

                __second_successor = self._id_passthrough(peer.second_successor)
                successors.append(__second_successor)
                _second_successor = __prettyConvert(__second_successor)

                builder.append(f"Peer {_id} - {__second_predecessor} > {__first_predecessor} > [{_id}] > {_first_successor} > {_second_successor}")
            
            # Check for peers that are not monitored, but were referenced by other peers
            peer_ids = [peer.id for peer in self.peers]
            for key in list(dict.fromkeys(successors)):
                if key is None: continue
                if key not in peer_ids:
                    unmonitoredPeers.append(key)

            if len(unmonitoredPeers) > 0:
                builder.append(f"\nUnmonitored Peers ({len(unmonitoredPeers)}): {', '.join(map(str,sorted(unmonitoredPeers)))}")

            builder.append("==================================")
            if self.suppressOutput: os.system("clear")
            print("\n".join(builder), file=sys.__stdout__)

            time.sleep(self.refreshInterval)

    """ 
    Helper function to the ID prettifier
    """
    def _id_passthrough(self, value: int):
        if type(value) not in [int, str]:
            return value

        checkLen = len(str(value))
        if checkLen > self.__maxLength:
            self.__maxLength = checkLen
        return value

    """
    Register a peer to be monitored
    """    
    def register(self, peer: Peer):
        if peer not in self.peers:
            self.peers.append(peer)
