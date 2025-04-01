def process_axes(lt, rt, lx, ly):
    """
    Map joystick axis values to command strings.
    Returns a list of strings to send.
    """
    cmds = []

    # Example: throttle and steer
    throttle_cmd = f"THROTTLE:{rt:.2f}"
    steer_cmd = f"STEER:{lx:.2f}"

    cmds.append(throttle_cmd)
    cmds.append(steer_cmd)

    return cmds

def process_buttons(buttons):
    """
    Map button states to commands. Only triggers when button goes from 0 -> 1.
    Returns a list of strings to send.
    """
    cmds = []

    for i, pressed in enumerate(buttons):
        if pressed:
            cmds.append(f"BUTTON_{i}\r\n")

    return cmds