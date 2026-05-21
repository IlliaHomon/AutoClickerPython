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
    icon_path = os.path.join(sys._MEIPASS, 'icon.png')
else: icon_path = 'icon.png'

delay = 0.5
AmountOfClicks = 10
IsClickerActive=False
IsInfiniteMode = True
MouseButtonToClick = Button.left  

root = tk.Tk()
root.title("AutoClicker")

Icon = ImageTk.PhotoImage(Image.open(icon_path))
root.iconphoto(False, Icon)
Mouse = Controller()
        
def Clicker():
    global IsClickerActive
    
    while True:
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

thread = threading.Thread(target=Clicker, daemon=True)
thread.start()

KeyboardListener = Listener(on_press=on_click)
KeyboardListener.daemon=True
KeyboardListener.start()   

root.mainloop()

#time.sleep(delay*AmountOfClicks+1)