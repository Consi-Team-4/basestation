from serial import Serial
from serial.tools.list_ports import comports
import datetime

port = None

for p in comports():
    if p.description.startswith("USB Serial Device"):
        port = p.name

print(port)

with Serial(port) as s:
    with open("logs/" + datetime.datetime.now().isoformat().replace(":", "-").replace(".", "-") + ".csv", "xb") as log:
        while True:
            buf = s.read(s.in_waiting)
            print(buf.decode(), end="")
            log.write(buf)
