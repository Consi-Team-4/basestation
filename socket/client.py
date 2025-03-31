import pygame
import socket
import time

# Initialize pygame
pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()

# Initialize client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('rcpi', 9999))

prev_fb_en = 1
prev_throttle_pos = 0

while True:
    # process events
    pygame.event.pump()
    
    buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
    hats = [joystick.get_hat(i) for i in range(joystick.get_numhats())]
    axes = [joystick.get_axis(i) for i in range(joystick.get_numaxes())]

    for i in range(len(axes)):
        if abs(axes[i]) < 0.04:
            axes[i] = 0   

    # A is buttons[0]
    # B is buttons[1]
    fb_en = prev_fb_en
    if buttons[1]:
        fb_en = 0
    elif  buttons[0]:
        fb_en = 1
    
    # Update suspension feedback enable
    if fb_en != prev_fb_en:
        prev_fb_en = fb_en
        client_socket.send(f"SF {fb_en}\n".encode())
    

    throttle = -axes[1] # Left stick Y

    # Update throttle feedback enable (want on for forwards, not for backwards)
    throttle_pos = int(throttle > 0)
    if throttle_pos != prev_throttle_pos:
        prev_throttle_pos = throttle_pos
        client_socket.send(f"EF {throttle_pos}\n".encode())
    
    # Write setpoint if positive, write power level if negative
    if throttle_pos:
        client_socket.send(f"ES {round(1800*throttle)}\n".encode())
    else:
        client_socket.send(f"EP {round(500*throttle)}\n".encode())
    
    steering = axes[2] # Right stick X
    client_socket.send(f"MS {round(300*steering)}\n".encode())

    time.sleep(0.05)