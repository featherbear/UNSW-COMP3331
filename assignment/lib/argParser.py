import sys

def _(ID_SPACE):  # Argument parser

    """
    Parse arguments for the join commands
    """
    def _JOIN():
        try:
            PEER, KNOWN_PEER, PING_INTERVAL = sys.argv[2:]

            PEER = int(PEER)
            KNOWN_PEER = int(KNOWN_PEER)
            
            if PEER | KNOWN_PEER >= ID_SPACE:
                print(
                    f"Peer IDs must be from 0 to {ID_SPACE-1} (inclusive)")
                return

            PING_INTERVAL = int(PING_INTERVAL)

            return ("join", PEER, KNOWN_PEER, PING_INTERVAL)
        except:
            print(f"Usage: {sys.argv[0]} join <PEER> <KNOWN_PEER> <PING_INTERVAL>")

    """
    Parse arguments for the init command 
    """
    def _INIT():
        try:
            PEER, FIRST_SUCCESSOR, SECOND_SUCCESSOR, PING_INTERVAL = sys.argv[2:]

            PEER = int(PEER)
            FIRST_SUCCESSOR = int(FIRST_SUCCESSOR)
            SECOND_SUCCESSOR = int(SECOND_SUCCESSOR)

            if PEER | FIRST_SUCCESSOR | SECOND_SUCCESSOR >= ID_SPACE:
                print(
                    f"Peer IDs must be from 0 to {ID_SPACE-1} (inclusive)")
                return

            PING_INTERVAL = int(PING_INTERVAL)

            return ("init", PEER, FIRST_SUCCESSOR, SECOND_SUCCESSOR, PING_INTERVAL)

        except Exception as e:
            print(
                f"Usage: {sys.argv[0]} <TYPE> <PEER> <FIRST_SUCCESSOR> <SECOND_SUCCESSOR> <PING_INTERVAL>")

    """
    Check for command type
    """
    TYPE = None
    def _TYPE_CHECK():
        nonlocal TYPE
        try:
            _, TYPE = sys.argv[:2]
            TYPE = TYPE.lower()

            return TYPE in ["init", "join"]
        except:
            pass
    
    #############

    if not _TYPE_CHECK():
        head = f"Usage: {sys.argv[0]} "
        print("\n".join([
            head + "init <PEER> <FIRST_SUCCESSOR> <SECOND_SUCCESSOR> <PING_INTERVAL>",
            " " * len(head) + "join <PEER> <KNOWN_PEER> <PING_INTERVAL>"
        ]))
        return

    if TYPE == "join":
        return _JOIN()
    elif TYPE == "init":
        return _INIT()