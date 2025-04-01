from threading import Thread

def start_keyboard_input(out_queue, stop_event):
    def run():
        print("[Keyboard] Type commands to send over Bluetooth. Ctrl+C to exit.")

        while not stop_event.is_set():
            try:
                msg = input("> ")
                if msg.strip() != "":
                    out_queue.put((msg.strip() + '\r\n').encode())
            except (EOFError, KeyboardInterrupt):
                print("\n[Keyboard] Input stopped.")
                break

    thread = Thread(target=run, daemon=True)
    thread.start()
    return thread