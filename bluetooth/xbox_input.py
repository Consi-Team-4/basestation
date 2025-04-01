import pygame
import time
from threading import Thread, Event
from queue import Queue
import os

def start_xbox_reader(out_queue:Queue, stop_event:Event) -> Thread:
    # Setup
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("[Xbox] No controller found.")
        return

    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"[Xbox] Connected: {joystick.get_name()}")
    print(f"[Xbox] Axes: {joystick.get_numaxes()}, Buttons: {joystick.get_numbuttons()}, Hats: {joystick.get_numhats()}")

    def run():
        prev_buttons = [0] * joystick.get_numbuttons()

        while not stop_event.is_set():
            pygame.event.pump()

            buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
            hats = [joystick.get_hat(i) for i in range(joystick.get_numhats())]
            axes = [joystick.get_axis(i) for i in range(joystick.get_numaxes())]

            for i, (prev, curr) in enumerate(zip(prev_buttons, buttons)):
                if curr == 1 and prev == 0:  # button rising edge detected
                    # Handle any rising edges we care about here
                    pass
            
            throttle = -axes[1]
            if throttle > 0:
                throttle *= 1800
            else:
                throttle *= 500

            
            steering = 300 * axes[2]

            out_queue.put(f"MD {round(throttle)}, {round(steering)}\n")
            time.sleep(0.02)

    thread = Thread(target=run)
    thread.start()
    return thread