from pynput.keyboard import Listener, Key
from pynput.mouse import Button, Controller 
import time
import threading
import tkinter as tk
from PIL import Image, ImageTk
import ctypes
import sys
import os

MyAppId = 'IlliaHomon.AutoClickerPython.1.2'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(MyAppId)

if hasattr(sys, '_MEIPASS'):
    icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
else: icon_path = 'icon.png'

AmountOfClicks = 10
IsClickerActive=False
IsInfiniteMode = True
MouseButtonToClick = Button.left  

root = tk.Tk()
root.title("AutoClicker")
root.geometry("500x400")

timeInput_frame = tk.LabelFrame(root, text="Click Interval",bd=2)
timeInput_frame.pack(fill='x', padx=10, pady=10, side='top')

hours_label = tk.Label(timeInput_frame, text="Hours:", font=("Arial", 9))
hours_label.grid(row=0, column=0, padx=(10,0))
hours_InputFrame = tk.Entry(timeInput_frame, width=8)
hours_InputFrame.insert(0, "0")
hours_InputFrame.grid(pady=5, padx=5, row=0, column=1)

minutes_label = tk.Label(timeInput_frame, text="Mins:", font=("Arial", 9))
minutes_label.grid(row=0, column=2)
minutes_InputFrame = tk.Entry(timeInput_frame, width=8)
minutes_InputFrame.insert(0, "0")
minutes_InputFrame.grid(pady=5, padx=5, row=0, column=3)

seconds_label = tk.Label(timeInput_frame, text="Secs:", font=("Arial", 9))
seconds_label.grid(row=0, column=4)
seconds_InputFrame = tk.Entry(timeInput_frame, width=8)
seconds_InputFrame.insert(0, "0")
seconds_InputFrame.grid(pady=5, padx=5, row=0, column=5)

miliseconds_label = tk.Label(timeInput_frame, text="Milisecs:", font=("Arial", 9))
miliseconds_label.grid(row=0, column=6)
miliseconds_InputFrame = tk.Entry(timeInput_frame, width=8)
miliseconds_InputFrame.insert(0, "100")
miliseconds_InputFrame.grid(pady=5, padx=5, row=0, column=7)

Icon = ImageTk.PhotoImage(Image.open(icon_path))
root.iconphoto(False, Icon)
Mouse = Controller()
        
def Clicker():
    global IsClickerActive
    
    while True:

        try:
            h = float(hours_InputFrame.get() or 0)
            m = float(minutes_InputFrame.get() or 0)
            s = float(seconds_InputFrame.get() or 0)
            ms = float(miliseconds_InputFrame.get() or 0)
            
            delay = (h * 3600) + (m * 60) + s + (ms / 1000)
            
            if delay <= 0: 
                delay = 0.1
        except ValueError:
            delay = 0.5 

        if not IsClickerActive:
            time.sleep(0.1)
            continue    
            
        if IsInfiniteMode: 
            Mouse.click(MouseButtonToClick)
            time.sleep(delay)
        else:
            for i in range(AmountOfClicks):
                Mouse.click(MouseButtonToClick)
                time.sleep(delay)
            IsClickerActive=False

def on_click(key):
    global IsClickerActive
    if hasattr(key,'char') and key.char == 'f': IsClickerActive = not IsClickerActive

def remove_focus(event):
    if event.widget.winfo_class() == "Entry": return
    root.focus_set()



thread = threading.Thread(target=Clicker, daemon=True)
thread.start()

KeyboardListener = Listener(on_press=on_click)
KeyboardListener.daemon=True
KeyboardListener.start()   

root.bind("<Button-1>", remove_focus)

root.mainloop()

#time.sleep(delay*AmountOfClicks+1)