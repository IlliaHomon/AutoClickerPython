from pynput.keyboard import Listener, Key
from pynput.mouse import Button, Controller 
import time
import threading
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import ctypes
import sys
import os

MyAppId = 'IlliaHomon.AutoClickerPython.1.2'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(MyAppId)

if hasattr(sys, '_MEIPASS'):
    icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
else: icon_path = 'icon.ico'

AmountOfClicks = 10
IsClickerActive=False
MouseButtonToClick = Button.left  
Hotkey='f'

Button_mapping={
    "Left": Button.left,
    "Right": Button.right,
    "Middle": Button.middle
}

key_translation={
    "escape": "esc",
    "return": "enter",
    "space": "space",
    "tab": "tab",
    "backspace": "backspace"
}

Banned_Keys = {"control_l", "shift_l", "alt_r", "backspace", "escape", " ", "return", "tab"}

root = tk.Tk()
root.title("AutoClicker")
root.geometry("500x400")
root.resizable(width=False, height=False)

# -KEY BINDING FUNCTIONS-

def start_listening():
    keyBinding_button.config(text="Press any key...", state='disabled')
    root.bind("<Key>", capture_key)

def capture_key(event):
    global Hotkey

    key_keysym = event.keysym.lower()
    if key_keysym in Banned_Keys:  
        root.unbind("<Key>")    
        keyBinding_button.config(text=f"{Hotkey.capitalize()}", state='normal')
        return

    new_key = event.char if event.char else event.keysym
    new_key=new_key.lower()
    translation = key_translation.get(new_key,new_key)
    if translation: Hotkey = translation
    root.unbind("<Key>")
    keyBinding_button.config(text=f"{Hotkey.capitalize()}", state='normal')

# -------------------------

def update_mouse_button(event):
    global MouseButtonToClick

    MouseButtonToClick=Button_mapping[selected_option.get()]

#-------BEGGINING OF GUI SETUP--------

# -INTERVAL-
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

# -MODE SELECTION-
Mode = tk.IntVar()
Mode.set(1)

modeSelection_frame = tk.LabelFrame(root, text="Mode Selection", bd=2)
modeSelection_frame.pack(fill='x', padx=10, pady=10, side='top')

infiniteMode_toggle = tk.Radiobutton(modeSelection_frame, variable=Mode, value=1)
infiniteMode_toggle.grid(row=0, column=0,padx=(10,0))
infiniteMode_label=tk.Label(modeSelection_frame, text="Repeat until stoped")
infiniteMode_label.grid(row=0, column=1)

amountOfClicksMode_toggle = tk.Radiobutton(modeSelection_frame, variable=Mode, value=2)
amountOfClicksMode_toggle.grid(row=0, column=2, padx=(20,0))
amountOfClicksMode_labelPart1=tk.Label(modeSelection_frame, text="Repeat")
amountOfClicksMode_labelPart1.grid(row=0, column=3)
amountOfClicksMode_InputFrame=tk.Entry(modeSelection_frame, width=10)
amountOfClicksMode_InputFrame.insert(0,"10")
amountOfClicksMode_InputFrame.grid(row=0, column=4, padx=5)
amountOfClicksMode_labelPart2=tk.Label(modeSelection_frame, text="times")
amountOfClicksMode_labelPart2.grid(row=0, column=5)

#ROW FOR KEY BINDING AND MOUSE BUTTON SELECTION
Row_frame = tk.Frame(root)
Row_frame.pack(side="top",fill='x')

# -KEY BINDING-
keyBinding_frame = tk.LabelFrame(Row_frame, text="Key Binding", bd=2 )
keyBinding_frame.pack(padx=(10,0), pady=10, side="left", expand=True, fill='x')

keyBinding_label = tk.Label(keyBinding_frame, text="Start/End Hotkey:")
keyBinding_label.grid(row=0, column=0)
keyBinding_button = tk.Button(keyBinding_frame, text="F", command=start_listening,width=10)
keyBinding_button.grid(row=0,column=1,pady=(0,5))

# -MOUSE BUTTON SELECTION-
selected_option=tk.StringVar()
options = ["Left", "Right", "Middle"]

mouseButtonSelection_frame = tk.LabelFrame(Row_frame, text="Mouse button selection", bd=2)
mouseButtonSelection_frame.pack(padx=10, pady=10, side="left", expand=True, fill='x')

mouseButtonSelection_label = tk.Label(mouseButtonSelection_frame, text="Mouse button to click:")
mouseButtonSelection_label.grid(row=0, column=0)
mouseButtonSelection_dropdown = ttk.Combobox(mouseButtonSelection_frame, state="readonly", values=options, textvariable=selected_option, width=10)
mouseButtonSelection_dropdown.current(0)
mouseButtonSelection_dropdown.grid(row=0, column=1, pady=(0,5))
mouseButtonSelection_dropdown.bind("<<ComboboxSelected>>", update_mouse_button)


#------END OF GUI SETUP------

Icon = ImageTk.PhotoImage(Image.open(icon_path))
root.iconphoto(False, Icon)

Mouse = Controller()
        
# -MAIN CLICKER FUNCTION-
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
            
        if Mode.get()==1: 
            Mouse.click(MouseButtonToClick)
            time.sleep(delay)
        else:
            try:
                amountOfClicks = int(amountOfClicksMode_InputFrame.get() or 1)
            except:
                amountOfClicks = 10

            for i in range(amountOfClicks):
                if not IsClickerActive: break
                Mouse.click(MouseButtonToClick)
                time.sleep(delay)
            IsClickerActive=False





#IF THE PRESET BUTTON FOR INFINITE MODE IS PRESSED CHANGE TO CLICKER IS ACTIVE
def on_click(key):
    global IsClickerActive
    if (hasattr(key,'char') and key.char is not None and key.char==Hotkey) or (getattr(key,'name','') and key.name.lower()==Hotkey): IsClickerActive = not IsClickerActive

#REMOVES THE CURSOR FROM ENTRY FIELD IF YOU CLICK SOMEWHERE ELSE
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