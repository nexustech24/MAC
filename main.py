import threading
import time
from tkinter import *
from tkinter import ttk
from pynput.mouse import Button as MouseButton, Controller
from pynput import keyboard

# Initialize mouse controller
mouse = Controller()

# Global variables
clicking = False
click_interval = 1.0  # Default interval in seconds
click_button = MouseButton.left  # Default button
repeat_count = None  # None means infinite clicking

def auto_clicker():
    global clicking, click_interval, click_button, repeat_count
    click_counter = 0

    while clicking:
        if repeat_count is not None and click_counter >= repeat_count:
            break
        mouse.click(click_button)
        click_counter += 1
        time.sleep(click_interval)

def toggle_clicking():
    global clicking, click_thread
    clicking = not clicking
    if clicking:
        start_button.config(text="Stop Auto Clicking")
        click_thread = threading.Thread(target=auto_clicker, daemon=True)
        click_thread.start()
        status_label.config(text="Status: Running")
        root.iconify()  # Minimize the window
    else:
        start_button.config(text="Start Auto Clicking")
        status_label.config(text="Status: Stopped")
        root.deiconify()  # Restore the window

def set_interval():
    global click_interval
    value = float(interval_entry.get())
    unit = interval_unit.get()
    if unit == "ms":
        click_interval = value / 1000
    elif unit == "s":
        click_interval = value
    elif unit == "m":
        click_interval = value * 60
    elif unit == "h":
        click_interval = value * 3600
    status_label.config(text=f"Interval set to {click_interval} seconds")

def set_button():
    global click_button
    option = button_option.get()
    if option == "Left":
        click_button = MouseButton.left
    elif option == "Right":
        click_button = MouseButton.right
    elif option == "Middle":
        click_button = MouseButton.middle
    status_label.config(text=f"Button set to {option}")

def set_repeat():
    global repeat_count
    count = repeat_entry.get().strip().lower()
    if count == "infinite":
        repeat_count = None
    else:
        try:
            repeat_count = int(count)
            if repeat_count <= 0:
                raise ValueError
        except ValueError:
            repeat_count = None
    status_label.config(text=f"Repeat set to {repeat_count if repeat_count is not None else 'infinite'}")

def start_stop_listener(key):
    if key == keyboard.Key.f6:
        toggle_clicking()

# Create UI
root = Tk()
root.title("Munitonne's Auto Clicker")
root.geometry("400x300")
root.resizable(False, False)  # Disable maximizing or resizing the window

# Interval settings
interval_frame = Frame(root)
interval_frame.pack(pady=10)

Label(interval_frame, text="Click Interval:").grid(row=0, column=0, padx=5)
interval_entry = Entry(interval_frame, width=10)
interval_entry.grid(row=0, column=1)
interval_entry.insert(0, "1.0")

interval_unit = ttk.Combobox(interval_frame, values=["ms", "s", "m", "h"], width=5)
interval_unit.grid(row=0, column=2, padx=5)
interval_unit.current(1)  # Default to seconds

set_interval_button = Button(interval_frame, text="Set Interval", command=set_interval)
set_interval_button.grid(row=0, column=3, padx=5)

# Button option
button_frame = Frame(root)
button_frame.pack(pady=10)

Label(button_frame, text="Click Button:").grid(row=0, column=0, padx=5)
button_option = ttk.Combobox(button_frame, values=["Left", "Right", "Middle"], width=10)
button_option.grid(row=0, column=1, padx=5)
button_option.current(0)  # Default to left button

set_button_button = Button(button_frame, text="Set Button", command=set_button)
set_button_button.grid(row=0, column=2, padx=5)

# Repeat count
repeat_frame = Frame(root)
repeat_frame.pack(pady=10)

Label(repeat_frame, text="Repeat Count:").grid(row=0, column=0, padx=5)
repeat_entry = Entry(repeat_frame, width=10)
repeat_entry.grid(row=0, column=1)
repeat_entry.insert(0, "infinite")

set_repeat_button = Button(repeat_frame, text="Set Repeat", command=set_repeat)
set_repeat_button.grid(row=0, column=2, padx=5)

# Start/Stop Button
start_button = Button(root, text="Start Auto Clicking", command=toggle_clicking)
start_button.pack(pady=20)

# Status label
status_label = Label(root, text="Status: Stopped", fg="blue")
status_label.pack(pady=10)

# Start listening for F6
listener = keyboard.Listener(on_press=start_stop_listener)
listener.start()

root.mainloop()
