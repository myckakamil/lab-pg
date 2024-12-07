import socket
import struct

# Multicast address and port
MULTICAST_GROUP = '224.0.0.1'
PORT = 5007

def multicast_receiver():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    
    sock.bind(('', PORT))

    group = socket.inet_aton(MULTICAST_GROUP)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    try:
        while True:
            print("Waiting for message...")
            data, address = sock.recvfrom(1024)
            print(f"Received {data.decode('utf-8')} from {address}")
    except KeyboardInterrupt:
        print("Receiver terminated.")
    finally:
        sock.close()

if __name__ == "__main__":
    multicast_receiver()
