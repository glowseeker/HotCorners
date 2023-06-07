# Imports
import pyautogui
import threading
from screeninfo import get_monitors
import time
import pystray
from pystray import MenuItem as item
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

# Disable PyAutoGui failsafe
pyautogui.FAILSAFE = False

# Set icon path
script_directory = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_directory, "icon.png")

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

# Define the action to perform when the hot corner is triggered
def perform_action(corner):
    print(f"Hot corner triggered: {corner}")
    # Add your desired action or function here
    if corner == 'top_left':
        pyautogui.hotkey('alt', 'tab')

    if corner == 'top_right':
        pyautogui.hotkey('alt', 'tab')

    if corner == 'bottom_left':
        pyautogui.hotkey('win', 'd')

    if corner == 'bottom_right':
        pyautogui.hotkey('win', 'd')

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

# Create a frame to hold the widgets
frame = ttk.Frame(root, padding="20")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create the start button
start_button = ttk.Button(frame, text="Start Hot Corners", command=start_hot_corners)
start_button.grid(row=0, column=0, padx=(0, 10), pady=(0, 10), sticky=tk.W)

# Create the stop button
stop_button = ttk.Button(frame, text="Stop Hot Corners", command=stop_hot_corners)
stop_button.grid(row=0, column=1, padx=(10, 0), pady=(0, 10), sticky=tk.W)

# Create the status text box
status_text = tk.Text(frame, height=1, width=25)
status_text.grid(row=1, column=0, columnspan=2)
status_text.tag_configure("running", foreground="green")
status_text.tag_configure("stopped", foreground="red")

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
   image = Image.open(image_path)
   icon=pystray.Icon("name", image, "Hot Corners", menu)
   icon.run()
   
# Bind the hide_window function to the "Close" button
root.protocol('WM_DELETE_WINDOW', hide_window)

# Start the main event loop
root.mainloop()