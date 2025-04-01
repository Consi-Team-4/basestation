import serial
import time
from threading import Thread

def start_bluetooth_writer(port_name, baudrate, data_queue, stop_event):
    def run():
        ser = None

        while not stop_event.is_set():
            if ser is None or not ser.is_open:
                try:
                    ser = serial.Serial(port_name, baudrate, timeout=1)
                    print(f"[BT] Connected to {port_name}")
                except serial.SerialException:
                    print("[BT] Bluetooth device not available, retrying...")
                    time.sleep(1)
                    continue

            try:
                data = data_queue.get(timeout=0.1)
                ser.write(data)
            except serial.SerialException:
                print("[BT] Serial write failed, resetting...")
                ser.close()
                ser = None
                time.sleep(1)
            except Exception:
                pass

    thread = Thread(target=run, daemon=True)
    thread.start()
    return thread