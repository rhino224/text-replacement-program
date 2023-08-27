import time
import os
import sys
import importlib
import keyboard
import subprocess
import json

restart_program_flag = False
key_sequence = ""
key_presses = 0  # Counter for the number of key presses without detection

def replace_text():
    global restart_program_flag, key_sequence, key_presses


    with open('replacement.txt', 'r') as file:
        replacements = dict(line.strip().split(':') for line in file)

    key_lengths = {key: len(key) for key in replacements}

    def on_press(event):
        global restart_program_flag, key_sequence, key_presses

        if event.name == "r" and keyboard.is_pressed("ctrl"):  # Check for Ctrl + R
            restart_program_flag = True
            return

        if event.event_type == keyboard.KEY_DOWN:
            key_name = event.name.lower()

            if key_name in ("enter", "shift", "space", "backspace", "alt", "caps"):
                return

            key_sequence += key_name
            key_presses += 1  # Increment the counter
            print(f"Key pressed: {key_sequence}")

            for key in replacements:
                if key in key_sequence:
                    remove_original_key_sequence(key_lengths.get(key, 0))
                    replacement = replacements[key]
                    replace_with_text(replacement)
                    print(f"Detected key press: {key_sequence} (Replaced with: {replacement})")
                    key_sequence = ""  # Reset the key sequence
                    key_presses = 0  # Reset the counter
                    return

    def replace_with_text(text):
        remove_original_key_sequence(key_lengths.get(key_sequence, 0))
        keyboard.write(text)

    def remove_original_key_sequence(num_backspaces):
        for _ in range(num_backspaces):
            keyboard.press_and_release("backspace")

    def restart_program():
        python = sys.executable
        os.startfile(__file__)
        time.sleep(0.4)
        sys.exit()

    keyboard.on_press(on_press)

    try:
        while True:
            if key_presses >= 25:
                print("Woah, We have more than 25 Key Presses!")
                key_sequence = ""  # Reset the key sequence
                key_presses = 0  # Reset the counter
            if restart_program_flag == True:
                print("Program is Restarting...")
                keyboard.unhook_all()
                restart_program()
                restart_program_flag = False  # Reset the restart flag
            time.sleep(1)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    replace_text()
