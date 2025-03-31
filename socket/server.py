import socket
from threading import Thread, Event
from queue import Queue, Empty
import json



def socket_to_queue(out_queue: Queue, stop_event: Event):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 9999))
    server_socket.listen()
    server_socket.settimeout(0.01)

    while not stop_event.is_set():
        try:
            connection, address = server_socket.accept()
        except socket.timeout:
            continue

        while not stop_event.is_set():
            try:
                #server_socket.setblocking(False)
                buf = connection.recv(2000)
                if len(buf) == 0:
                    break
                else:
                    data = buf.decode()
                    out_queue.put(data)

            except socket.timeout:
                continue

data_queue = Queue()
stop_event = Event()

socket_thread = Thread(target=socket_to_queue, args=(data_queue, stop_event))
socket_thread.start()

prev_fb_en = 1
prev_esc_sign = 0

try:

    while True:
        try:
            data = data_queue.get(block=True, timeout=0.01)
            print(data)
            
        except Empty:
            pass
        

finally:
    stop_event.set()