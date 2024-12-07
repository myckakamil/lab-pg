import socket
import struct
import time

MULTICAST_GROUPS = ['224.0.0.1']
PORT = 5007

def multicast_sender():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    
    try:
        while True:
            for group in MULTICAST_GROUPS:
                message = f"Hejka"
                print(f"Sending: {message} to {group}:{PORT}")
                sock.sendto(message.encode('utf-8'), (group, PORT))
                time.sleep(2)
    except KeyboardInterrupt:
        print("Sender terminated.")
    finally:
        sock.close()

if __name__ == "__main__":
    multicast_sender()
