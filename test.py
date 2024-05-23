import keyboard

# Define a callback function to print a message when the trigger is detected
def on_trigger_detected():
    print("Trigger detected!")

# Add a word listener for a specific secret + trigger combination
keyboard.add_word_listener("test!", on_trigger_detected, triggers=['!'])

# Keep the script running to listen for the trigger
keyboard.wait('esc')  # Press 'esc' to stop the script
