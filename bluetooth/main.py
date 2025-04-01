from threading import Event
from queue import Queue
import time

from bluetooth_serial import start_bluetooth_writer
from xbox_input import start_xbox_reader
from keyboard_input import start_keyboard_input

if __name__ == "__main__":
    data_queue = Queue()
    stop_event = Event()

    # Set your Bluetooth serial port here
    port_name = "/dev/tty.Suspenders"
    baudrate = 115200

    print("[Main] Starting threads...")

    bt_thread = start_bluetooth_writer(port_name, baudrate, data_queue, stop_event)
    xbox_thread = start_xbox_reader(data_queue, stop_event)
    keyboard_thread = start_keyboard_input(data_queue, stop_event)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[Main] Shutting down...")
        stop_event.set()