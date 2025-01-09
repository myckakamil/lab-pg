# -*- coding: utf-8 -*-
import socket
import time

HOST = "::1"  # Adres IPv6 localhost
UDP_PORT = 50001
TCP_PORT = 50002

# Funkcja testująca UDP
def test_udp():
    with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as udp_socket:
        message = "Pytanie przez UDP"
        udp_socket.sendto(message.encode(), (HOST, UDP_PORT))
        response, _ = udp_socket.recvfrom(1024)
        print(f"[UDP] Odpowiedź serwera: {response.decode()}")

# Funkcja testująca TCP
def test_tcp():
    with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as tcp_socket:
        tcp_socket.connect((HOST, TCP_PORT))
        message = "Pytanie przez TCP"
        tcp_socket.sendall(message.encode())
        response = tcp_socket.recv(1024)
        print(f"[TCP] Odpowiedź serwera: {response.decode()}")

if __name__ == "__main__":
    test_udp()
   # test_tcp()
