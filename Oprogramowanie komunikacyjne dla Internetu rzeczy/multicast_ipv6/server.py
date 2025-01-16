# Kamil Myćka 184652
# Aleksandra Rykowska 184616

import socket
import struct

def join_multicast_group(sock, multicast_group):
    group_bin = socket.inet_pton(socket.AF_INET6, multicast_group)
    # Dołączamy do grupy multicastowej (idx = 0 dla interfejsu domyślnego)
    mreq = group_bin + struct.pack('@I', 0)
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)
    return mreq  # Zwracamy mreq do późniejszego opuszczenia grupy

def multicast_server(multicast_group, port):
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bindowanie do adresu "::" i portu
    sock.bind(("::", port))

    # Dołącz do grupy multicastowej
    mreq = join_multicast_group(sock, multicast_group)

    print(f"Serwer działa. Nasłuchuje na {multicast_group}:{port}")
    try:
        while True:
            data, addr = sock.recvfrom(1024)
            message = data.decode('utf-8')
            print(f"Odebrano wiadomość od {addr[0]}: {message}")

            # Wysyłanie potwierdzenia do nadawcy
            response = f"Serwer odebrał: {message}"
            sock.sendto(response.encode('utf-8'), addr)
    except KeyboardInterrupt:
        print("\nSerwer zakończył pracę.")
    finally:
        # Opuszczenie grupy multicastowej
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_LEAVE_GROUP, mreq)
        sock.close()
        print("Opuszczono grupę multicastową i zamknięto gniazdo.")

if __name__ == "__main__":
    multicast_group = "ff22::1"
    port = 12345
    multicast_server(multicast_group, port)

