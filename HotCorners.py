# Imports
import pyautogui
import threading
from screeninfo import get_monitors
import time
import pystray
from pystray import MenuItem as item
import tkinter as tk
from tkinter import ttk
from PIL import Image
import os
import sys
from Hotkeys import HOTKEYS

# Disable PyAutoGui failsafe
pyautogui.FAILSAFE = False

# Set images path
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Fetch the screen resolution
monitor = get_monitors()[0]
screen_width = monitor.width
screen_height = monitor.height

# Calculate the coordinates of the four corners
top_left = (0, 0)
top_right = (screen_width - 1, 0)
bottom_left = (0, screen_height - 1)
bottom_right = (screen_width - 1, screen_height - 1)

# Trigger delay
delay = float(0.1);

# Function to perform the action based on the triggered corner
def perform_action(corner):
    selected_action = None

    if corner == 'top_left':
        selected_action = top_left_action.get()
    elif corner == 'top_right':
        selected_action = top_right_action.get()
    elif corner == 'bottom_left':
        selected_action = bottom_left_action.get()
    elif corner == 'bottom_right':
        selected_action = bottom_right_action.get()

    if selected_action:
        for name, hotkeys in HOTKEYS:
            if name == selected_action:
                pyautogui.hotkey(*hotkeys)
                break


# Define the function to check if the mouse is in any of the hot corners
def check_hot_corners():
    global is_hot_corner_triggered

    mouse_x, mouse_y = pyautogui.position()

    if (mouse_x, mouse_y) == top_left:
        trigger_hot_corner('top_left')
    elif (mouse_x, mouse_y) == top_right:
        trigger_hot_corner('top_right')
    elif (mouse_x, mouse_y) == bottom_left:
        trigger_hot_corner('bottom_left')
    elif (mouse_x, mouse_y) == bottom_right:
        trigger_hot_corner('bottom_right')
    else:
        is_hot_corner_triggered = False

# Define the function to trigger the hot corner action
def trigger_hot_corner(corner):
    global is_hot_corner_triggered

    if not is_hot_corner_triggered:
        time.sleep(delay)  # Add a delay
        if pyautogui.position() == get_corner_coordinates(corner):  # Re-check the position after the delay
            is_hot_corner_triggered = True
            perform_action(corner)

# Initialize the running state and trigger variable
is_running = True
is_hot_corner_triggered = False

# Get the corner coordinates based on the provided corner name
def get_corner_coordinates(corner):
    if corner == 'top_left':
        return top_left
    elif corner == 'top_right':
        return top_right
    elif corner == 'bottom_left':
        return bottom_left
    elif corner == 'bottom_right':
        return bottom_right








# Create a function to start the hot corners detection
def start_hot_corners():
    global is_running
    is_running = True
    hot_corners_thread = threading.Thread(target=hot_corners_loop)
    hot_corners_thread.start()
    status_text.delete("1.0", tk.END)
    status_text.insert(tk.END, "Hot Corners Running", "running")

# Create a function to stop the hot corners detection
def stop_hot_corners():
    global is_running
    is_running = False
    status_text.delete("1.0", tk.END)
    status_text.insert(tk.END, "Hot Corners Stopped", "stopped")

# Create a function for the hot corners loop
def hot_corners_loop():
    while is_running:
        check_hot_corners()

# Create the main window
root = tk.Tk()
root.title("Hot Corners")

padding = 5

# Create the start button
start_button = ttk.Button(root, text="Start Hot Corners", command=start_hot_corners)
start_button.grid(row=0, column=0, padx=padding, pady=padding)

# Create the stop button
stop_button = ttk.Button(root, text="Stop Hot Corners", command=stop_hot_corners)
stop_button.grid(row=0, column=1, padx=padding, pady=padding)

# Create the status text box
status_text = tk.Text(root, height=1, width=20)
status_text.insert(tk.END, "Not running", "stopped")
status_text.grid(row=0, column=2, columnspan=2, padx=padding, pady=padding)
status_text.tag_configure("running", foreground="green")
status_text.tag_configure("stopped", foreground="red")

# Create variables to store the selected values
top_left_action = tk.StringVar()
top_right_action = tk.StringVar()
bottom_left_action = tk.StringVar()
bottom_right_action = tk.StringVar()

# Create a list of hotkey names
hotkey_names = [name for name, _ in HOTKEYS]

# Create the dropdown lists
top_left_dropdown = ttk.Combobox(root, values=hotkey_names, textvariable=top_left_action, state="readonly")
top_right_dropdown = ttk.Combobox(root, values=hotkey_names, textvariable=top_right_action, state="readonly")
bottom_left_dropdown = ttk.Combobox(root, values=hotkey_names, textvariable=bottom_left_action, state="readonly")
bottom_right_dropdown = ttk.Combobox(root, values=hotkey_names, textvariable=bottom_right_action, state="readonly")

# Create the labels
top_left_label = ttk.Label(root, text="Top Left Action:")
top_right_label = ttk.Label(root, text="Top Right Action:")
bottom_left_label = ttk.Label(root, text="Bottom Left Action:")
bottom_right_label = ttk.Label(root, text="Bottom Right Action:")

# Position the labels
top_left_label.grid(row=1, column=0, columnspan=2, padx=padding, pady=padding)
top_right_label.grid(row=1, column=2, columnspan=2, padx=padding, pady=padding)
bottom_left_label.grid(row=3, column=0, columnspan=2, padx=padding, pady=padding)
bottom_right_label.grid(row=3, column=2, columnspan=2, padx=padding, pady=padding)

# Position the dropdown lists
top_left_dropdown.grid(row=2, column=0, columnspan=2, padx=padding, pady=padding)
top_right_dropdown.grid(row=2, column=2, columnspan=2, padx=padding, pady=padding)
bottom_left_dropdown.grid(row=4, column=0, columnspan=2, padx=padding, pady=padding)
bottom_right_dropdown.grid(row=4, column=2, columnspan=2, padx=padding, pady=padding)

# Define a function for quit the window
def quit_window(icon, item):
    root.quit()
    icon.stop()

# Define a function to show the window again
def show_window(icon, item):
    icon.stop()  # Set focus on the window
    root.after(0, root.deiconify)  # Show the window with a slight delay


# Hide the window and show on the system taskbar
def hide_window():
   # Hide the window
   root.withdraw()

   # Create the context menu
   menu=(item('Quit', quit_window), item('Show', show_window))
   
   # Create the systray icon
   image = Image.open(resource_path("icon.png"))
   icon=pystray.Icon("name", image, "Hot Corners", menu)
   icon.run()
   
# Bind the hide_window function to the "Close" button
root.protocol('WM_DELETE_WINDOW', hide_window)

# Start the main event loop
root.mainloop()