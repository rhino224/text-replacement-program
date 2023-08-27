import time
import os
import keyboard

def replace_text():
    # Load the keys and replacement text from the text file
    with open('replacement.txt', 'r') as file:
        replacements = dict(line.strip().split(':') for line in file)

    key_lengths = {key: len(key) for key in replacements}  # Store the lengths of the keys

    key_sequence = ""  # Initialize the key sequence variable
    key_presses = 0  # Counter for the number of key presses without detection

    def on_press(event):
        nonlocal key_sequence, key_presses  # Use the nonlocal keyword to access the outer variables

        if event.event_type == keyboard.KEY_DOWN:
            key_name = event.name.lower()  # Convert key name to lowercase
            if key_name in ("enter", "shift", "space"):
                return  # Ignore Enter, Shift, and Space keys

            key_sequence += key_name  # Append the pressed key to the sequence
            key_presses += 1  # Increment the counter
            print(f"Key pressed: {key_sequence}")

            # Check if any key from the replacements is present in the text
            for key in replacements:
                if key in key_sequence:
                    remove_original_key_sequence(key_lengths.get(key, 0))
                    replacement = replacements[key]
                    replace_with_text(replacement)
                    print(f"Detected key press: {key_sequence} (Replaced with: {replacement})")
                    key_sequence = ""  # Reset the key sequence
                    key_presses = 0  # Reset the counter
                    return  # Exit the loop to avoid further replacements

        elif event.event_type == keyboard.KEY_UP:
            key_sequence += event.name.lower()  # Append the key name to the sequence

    def replace_with_text(text):
        remove_original_key_sequence(key_lengths.get(key_sequence, 0))
        keyboard.write(text)  # Simulate typing the replacement text

    def remove_original_key_sequence(num_backspaces):
        for _ in range(num_backspaces):
            keyboard.press_and_release("backspace")

    # Start listening for key presses
    keyboard.on_press(on_press)

    # Keep the program running until interrupted
    try:
        while True:
            if key_presses >= 25:
                key_sequence = ""  # Reset the key sequence
                key_presses = 0  # Reset the counter
            time.sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    # Change the working directory to the folder where the script is located
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Run the program
    replace_text()
