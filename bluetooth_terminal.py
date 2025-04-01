import serial
import threading

def read_from_port(ser):
    while True:
        if ser.in_waiting:
            print(ser.readline().decode().strip())

ser = serial.Serial('/dev/tty.Suspenders', 115200, timeout=1)
thread = threading.Thread(target=read_from_port, args=(ser,))
thread.daemon = True
thread.start()

print("Type something to send. Press Ctrl+C to exit.")

try:
    while True:
        msg = input("> ")
        ser.write((msg + '\r\n').encode())
except KeyboardInterrupt:
    print("Exiting...")
    ser.close()