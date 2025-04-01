import pygame
import time
from threading import Thread
import os
from command_mapper import process_axes, process_buttons

def start_xbox_reader(out_queue, stop_event):
    def run():
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

        prev_buttons = [0] * joystick.get_numbuttons()

        while not stop_event.is_set():
            pygame.event.pump()

            lt = joystick.get_axis(2)
            rt = joystick.get_axis(5)
            lx = joystick.get_axis(0)
            ly = joystick.get_axis(1)

            buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
              
            #print(f"Axes -> LT:{lt:.2f} RT:{rt:.2f} LX:{lx:.2f} LY:{ly:.2f}, Buttons -> {buttons}")
            msg = f"LT:{lt:.2f} RT:{rt:.2f} LX:{lx:.2f} LY:{ly:.2f}\n".encode()
            out_queue.put(msg)

            axis_cmds = process_axes(lt, rt, lx, ly)
            button_cmds = []

            for i, (prev, curr) in enumerate(zip(prev_buttons, buttons)):
                if curr == 1 and prev == 0:  # button press detected
                    button_cmds.extend(process_buttons([i]))

            prev_buttons = buttons

            for cmd in axis_cmds + button_cmds:
                out_queue.put((cmd + '\r\n').encode())
                
                


            time.sleep(0.05)

        pygame.quit()

    thread = Thread(target=run, daemon=True)
    thread.start()
    return thread