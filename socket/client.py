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
client_socket.connect(('localhost', 9999))

prev_fb_en = 1
prev_throttle_sign = 0

while True:
    # process events
    pygame.event.pump()
    
    buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
    hats = [joystick.get_hat(i) for i in range(joystick.get_numhats())]
    axes = [joystick.get_axis(i) for i in range(joystick.get_numaxes())]

    # A is buttons[0]
    # B is buttons[1]

    throttle = -axes[1] # Left stick Y
    steering = axes[2] # Right stick X

    fb_en = prev_fb_en
    if buttons[1]:
        fb_en = 0
    elif  buttons[0]:
        fb_en = 1
    
    if fb_en != prev_fb_en:
        client_socket.send(f"SF {fb_en}\n".encode())


    # throttle is LY, 1 is forwards
    # steering is RX, 1 is right

    data = {"throttle":  "steering": axes[2], "fb_en": fb_en}

    print(data)
    client_socket.send(json.dumps(data).encode())

    time.sleep(0.01)