import pygame
import time
from threading import Thread, Event
from queue import Queue, Empty
import os
from serial import Serial
from serial.tools.list_ports import comports

serial_port = "COM9"


def controller_thread_func(out_queue:Queue, stop_event:Event):
    # Set up pygame
    #os.environ["SDL_VIDEODRIVER"] = "dummy"
    print("Initializing pygame...")
    pygame.init()
    pygame.joystick.init()
    print("Pygame initialized!")

    print(pygame.joystick.get_count())
    if pygame.joystick.get_count() == 0:
        raise Exception("[Xbox] No controller found.")
        

    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    # print(f"[Xbox] Connected: {joystick.get_name()}")
    # print(f"[Xbox] Axes: {joystick.get_numaxes()}, Buttons: {joystick.get_numbuttons()}, Hats: {joystick.get_numhats()}")
    print("Connected!")

    prev_buttons = [0] * joystick.get_numbuttons()

    while not stop_event.is_set():
        pygame.event.pump()

        buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
        hats = [joystick.get_hat(i) for i in range(joystick.get_numhats())]
        axes = [joystick.get_axis(i) for i in range(joystick.get_numaxes())]

        for i in range(4):
            if abs(axes[i]) < 0.04:
                axes[i] = 0 

        for i, (prev, curr) in enumerate(zip(prev_buttons, buttons)):
            if curr == 1 and prev == 0:  # button rising edge detected
                # Handle any rising edges we care about here
                pass
        
        throttle = -axes[1]
        if throttle > 0:
            throttle *= 1800
            #out_queue.put(f"EF 1\n".encode())
            #out_queue.put(f"ES {round(throttle)}\n".encode())
        else:
            throttle *= 500
            #out_queue.put(f"EP {round(throttle)}\n".encode())

        
        steering = 300 * axes[2]
        #out_queue.put(f"MS {round(steering)}\n".encode())

        out_queue.put(f"MD {round(throttle)} {round(steering)}\n".encode())
        
        time.sleep(0.05)


# Set up serial
print("Connecting to bluetooth serial...")
s = Serial(serial_port)
print("Connected!")

def serial_thread_func(in_queue:Queue, stop_event:Event):
    while not stop_event.is_set():
        try:
            command = in_queue.get(True, 0.01)
            s.write(command)
        except Empty:
            pass


command_queue = Queue()
stop_event = Event()


controller_thread = Thread(target=controller_thread_func, args=[command_queue, stop_event])
controller_thread.start()
serial_thread = Thread(target=serial_thread_func, args=(command_queue, stop_event))
serial_thread.start()

# Accept commands from the console until control C
try:
    while True:
        command = input("> ") + "\n"

        command_queue.put(command.encode())

finally:
    stop_event.set()

     # clear the queue so that it will stop properly?
    try:
        while True:
            command_queue.get(False)
    except Empty:
        pass

    controller_thread.join()
    serial_thread.join()

    s.close()
