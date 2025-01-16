# Kamil Myćka 184652
# Aleksandra Rykowska 184616

import socket
import threading
import time

def send_messages(sock, multicast_group, port, can_send_event):
    while True:
        try:
            # Oczekiwanie na pozwolenie wysłania wiadomości
            can_send_event.wait()
            message = input("Wpisz wiadomość do wysłania: ")
            sock.sendto(message.encode('utf-8'), (multicast_group, port))
            can_send_event.clear()  # Zablokuj możliwość wysyłania kolejnej wiadomości
        except KeyboardInterrupt:
            print("\nKończenie wątku wysyłania.")
            break

def receive_messages(sock, own_address, can_send_event):
    while True:
        try:
            response, addr = sock.recvfrom(1024)
            if addr[0] != own_address:  # Ignoruj odpowiedzi od samego siebie
                print(f"Odpowiedź od {addr[0]}: {response.decode('utf-8')}")
                time.sleep(1)  # Odczekaj 1 sekundę
                can_send_event.set()  # Zezwól na wysłanie kolejnej wiadomości
        except KeyboardInterrupt:
            print("\nKończenie wątku odbierania.")
            break

def multicast_client(multicast_group, port):
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, 1)  # TTL = 1
    sock.bind(("::", 0))  # Bindowanie do nasłuchiwania

    # Pobranie adresu własnego
    own_address = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET6)[0][4][0]

    # Dołączenie do grupy multicastowej
    group_bin = socket.inet_pton(socket.AF_INET6, multicast_group)
    mreq = group_bin + b'\x00' * 12  # Interfejs = 0 (domyślny)
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

    # Mechanizm synchronizacji wątków
    can_send_event = threading.Event()
    can_send_event.set()  # Na początku pozwalamy wysyłać wiadomości

    print(f"Klient działa. Wysyła na {multicast_group}:{port}")
    try:
        # Uruchomienie dwóch wątków
        sender_thread = threading.Thread(target=send_messages, args=(sock, multicast_group, port, can_send_event), daemon=True)
        receiver_thread = threading.Thread(target=receive_messages, args=(sock, own_address, can_send_event), daemon=True)

        sender_thread.start()
        receiver_thread.start()

        # Poczekaj na zakończenie obu wątków
        sender_thread.join()
        receiver_thread.join()
    except KeyboardInterrupt:
        print("\nKlient zakończył pracę.")
    finally:
        # Opuszczenie grupy multicastowej
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_LEAVE_GROUP, mreq)
        sock.close()
        print("Opuszczono grupę multicastową i zamknięto gniazdo.")

if __name__ == "__main__":
    multicast_group = "ff22::1"
    port = 12345
    multicast_client(multicast_group, port)

