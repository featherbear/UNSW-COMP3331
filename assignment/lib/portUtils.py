BASE_PORT = 12000

"""
Calculate the port

By assignment definition, it is the base port + the peer ID
"""
def calculate_port(offset: int) -> int:
    return BASE_PORT + offset

