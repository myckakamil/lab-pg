# -*- coding: utf-8 -*-
import socket
import threading
import datetime

HOST = "::"  # Nasłuch na wszystkich interfejsach IPv6
UDP_PORT = 50001
TCP_PORT = 50002

def handle_udp():
    """Obsługa komunikacji UDP."""
    with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.bind((HOST, UDP_PORT))
        print(f"Serwer UDP nasłuchuje na porcie {UDP_PORT}")
        try:
            while True:
                data, addr = udp_socket.recvfrom(1024)
                timestamp = datetime.datetime.now().isoformat()
                response = f"ECHO: {data.decode()} | Od: {addr} | Czas: {timestamp}"
                print(f"[UDP] Odebrano od {addr}: {data.decode()}")
                udp_socket.sendto(response.encode(), addr)
        except KeyboardInterrupt:
            print("\n[UDP] Zamykam gniazdo UDP...")

def handle_tcp():
    """Obsługa komunikacji TCP."""
    with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as tcp_socket:
        tcp_socket.bind((HOST, TCP_PORT))
        tcp_socket.listen(5)
        print(f"Serwer TCP nasłuchuje na porcie {TCP_PORT}")
        try:
            while True:
                conn, addr = tcp_socket.accept()
                with conn:
                    print(f"[TCP] Połączenie od {addr}")
                    data = conn.recv(1024)
                    if data:
                        timestamp = datetime.datetime.now().isoformat()
                        response = f"ECHO: {data.decode()} | Od: {addr} | Czas: {timestamp}"
                        print(f"[TCP] Odebrano od {addr}: {data.decode()}")
                        conn.sendall(response.encode())
        except KeyboardInterrupt:
            print("\n[TCP] Zamykam gniazdo TCP...")

if __name__ == "__main__":
    try:
        # Tworzymy wątki dla UDP i TCP
        udp_thread = threading.Thread(target=handle_udp, daemon=True)
        tcp_thread = threading.Thread(target=handle_tcp, daemon=True)
        
        udp_thread.start()
        tcp_thread.start()

        print("Serwer działa. Naciśnij Ctrl+C, aby zakończyć.")
        udp_thread.join()
        tcp_thread.join()
    except KeyboardInterrupt:
        print("\nSerwer zakończył działanie.")

