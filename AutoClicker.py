from pynput.keyboard import Listener, Key
from pynput.mouse import Button, Controller
from pynput.mouse import Listener as MouseListener
import time
import threading
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import ctypes
import sys
import os
import json

MyAppId = 'IlliaHomon.AutoClickerPython.1.2'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(MyAppId)

if hasattr(sys, '_MEIPASS'):
    icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
else: icon_path = 'icon.ico'

AmountOfClicks = 10
IsClickerActive=False
MouseButtonToClick = Button.left  
StartHotkey="f8"
addTargetHotkey="q"
deleteTargetHotkey="e"
targets = []

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

Banned_Keys = {"control_l", "shift_l", "alt_r", "backspace", "escape", " ", "return", "tab", StartHotkey, addTargetHotkey, deleteTargetHotkey}

root = tk.Tk()
root.title("AutoClicker")
root.geometry("500x425")
root.resizable(width=False, height=False)

selected_option = tk.StringVar()

# -READING FROM JSON-
def load_settings():
    global StartHotkey, AmountOfClicks, MouseButtonToClick,isStayOnTop, selected_option, isMultiTarget
    if os.path.exists("settings.json"):
        try:
            with open("settings.json", "r") as file:
                settings_data = json.load(file)

                StartHotkey=settings_data.get("start_hotkey")
                startKeyBinding_button.config(text=f"{StartHotkey.capitalize()}")

                AmountOfClicks=settings_data.get("amount_of_clicks")

                button_str = settings_data.get("mouse_button_to_click", "Left")
                selected_option.set(button_str)
                MouseButtonToClick=Button_mapping[selected_option.get()]

                hours_InputFrame.delete(0, tk.END)
                hours_InputFrame.insert(0, settings_data.get("hours", 0))
                minutes_InputFrame.delete(0, tk.END)
                minutes_InputFrame.insert(0, settings_data.get("minutes", 0))
                seconds_InputFrame.delete(0, tk.END)
                seconds_InputFrame.insert(0, settings_data.get("seconds", 0))
                miliseconds_InputFrame.delete(0, tk.END)
                miliseconds_InputFrame.insert(0, settings_data.get("miliseconds", 0))

                hoursMultiTarget_InputFrame.delete(0, tk.END)
                hoursMultiTarget_InputFrame.insert(0, settings_data.get("hours_multitarget", 0))
                minutesMultiTarget_InputFrame.delete(0, tk.END)
                minutesMultiTarget_InputFrame.insert(0, settings_data.get("minutes_multitarget", 0))
                secondsMultiTarget_InputFrame.delete(0, tk.END)
                secondsMultiTarget_InputFrame.insert(0, settings_data.get("seconds_multitarget", 0))
                milisecondsMultiTarget_InputFrame.delete(0, tk.END)
                milisecondsMultiTarget_InputFrame.insert(0, settings_data.get("miliseconds_multitarget", 0))

                isStayOnTop.set(settings_data.get("stay_on_top"))
                isMultiTarget.set(settings_data.get("multi_target"))
        except(json.JSONDecodeError, KeyError): 
            print("Settings file corrupted or missing keys. Using default configurations.")

# -WRITING TO JSON-
def save_settings():
    settings_data = {
        "start_hotkey": StartHotkey,
        "amount_of_clicks": AmountOfClicks,
        "mouse_button_to_click": selected_option.get(),
        "hours": int(hours_InputFrame.get() or 0),
        "minutes": int(minutes_InputFrame.get() or 0),
        "seconds": int(seconds_InputFrame.get() or 0),
        "miliseconds": int(miliseconds_InputFrame.get() or 0),
        "stay_on_top": isStayOnTop.get(),
        "multi_target": isMultiTarget.get(),
        "hours_multitarget": int(hoursMultiTarget_InputFrame.get() or 0),
        "minutes_multitarget": int(minutesMultiTarget_InputFrame.get() or 0),
        "seconds_multitarget": int(secondsMultiTarget_InputFrame.get() or 0),
        "miliseconds_multitarget": int(milisecondsMultiTarget_InputFrame.get() or 0)
    }

    with open("settings.json", "w") as file:
        json.dump(settings_data, file, indent=4)

# -KEY BINDING FUNCTIONS-

def start_listening(target):
    startKeyBinding_button.config(state='disabled')
    addTargetKeyBindig_button.config(state='disabled')

    if target == "start":
        startKeyBinding_button.config(text="Press any key...")
    elif target=="add_target":
        addTargetKeyBindig_button.config(text="Press any key...")
    else: deleteTargetKeyBindig_button.config(text="Press any key...")

    root.bind("<Key>", lambda event: capture_key(event, target))

def capture_key(event, target):
    global StartHotkey, addTargetHotkey, deleteTargetHotkey

    key_keysym = event.keysym.lower()

    if target == "start":
        if key_keysym in Banned_Keys:  
            root.unbind("<Key>")    
            startKeyBinding_button.config(text=f"{StartHotkey.capitalize()}", state='normal')
            addTargetKeyBindig_button.config(text=f"{addTargetHotkey.capitalize()}", state='normal')
            deleteTargetKeyBindig_button.config(text=f"{deleteTargetHotkey.capitalize()}", state='normal')
            return

        new_key = event.char if event.char else event.keysym
        new_key=new_key.lower()
        translation = key_translation.get(new_key,new_key)
        if translation: StartHotkey = translation
        root.unbind("<Key>")
        startKeyBinding_button.config(text=f"{StartHotkey.capitalize()}", state='normal')
        addTargetKeyBindig_button.config(text=f"{addTargetHotkey.capitalize()}", state='normal')
        deleteTargetKeyBindig_button.config(text=f"{deleteTargetHotkey.capitalize()}", state='normal')

    elif target == "add_target":
        if key_keysym in Banned_Keys:  
            root.unbind("<Key>")    
            addTargetKeyBindig_button.config(text=f"{addTargetHotkey.capitalize()}", state='normal')
            startKeyBinding_button.config(text=f"{StartHotkey.capitalize()}", state='normal')
            deleteTargetKeyBindig_button.config(text=f"{deleteTargetHotkey.capitalize()}", state='normal')
            return

        new_key = event.char if event.char else event.keysym
        new_key=new_key.lower()
        translation = key_translation.get(new_key,new_key)
        if translation: addTargetHotkey = translation
        root.unbind("<Key>")
        addTargetKeyBindig_button.config(text=f"{addTargetHotkey.capitalize()}", state='normal')
        startKeyBinding_button.config(text=f"{StartHotkey.capitalize()}", state='normal')
        deleteTargetKeyBindig_button.config(text=f"{deleteTargetHotkey.capitalize()}", state='normal')
    
    else:
        if key_keysym in Banned_Keys:  
            root.unbind("<Key>")    
            addTargetKeyBindig_button.config(text=f"{addTargetHotkey.capitalize()}", state='normal')
            startKeyBinding_button.config(text=f"{StartHotkey.capitalize()}", state='normal')
            deleteTargetKeyBindig_button.config(text=f"{deleteTargetHotkey.capitalize()}", state='normal')
            return
        
        new_key = event.char if event.char else event.keysym
        new_key=new_key.lower()
        translation = key_translation.get(new_key,new_key)
        if translation: deleteTargetHotkey = translation
        root.unbind("<Key>")
        addTargetKeyBindig_button.config(text=f"{addTargetHotkey.capitalize()}", state='normal')
        startKeyBinding_button.config(text=f"{StartHotkey.capitalize()}", state='normal')
        deleteTargetKeyBindig_button.config(text=f"{deleteTargetHotkey.capitalize()}", state='normal')

    save_settings()

# -------------------------

# -FUNCTION TO UPDATE WHICH MOUSE BUTTON TO CLICK-
def update_mouse_button(event):
    global MouseButtonToClick
    MouseButtonToClick=Button_mapping[selected_option.get()]
    save_settings()

# -FUNCTIONS FOR START AND STOP BUTTONS-
def changeClickerState_toActive():
    global IsClickerActive
    IsClickerActive = not IsClickerActive if IsClickerActive == False else IsClickerActive

def changeClickerState_toUnActive():
    global IsClickerActive
    IsClickerActive = not IsClickerActive if IsClickerActive else IsClickerActive

# -FUNCTIONS FOR STAYING ON TOP-
def stayOnTop():
    if isStayOnTop.get(): root.attributes("-topmost", True)
    else: root.attributes("-topmost", False)
    save_settings()

#-------BEGGINING OF GUI SETUP--------

# -INTERVAL-
timeInput_frame = tk.LabelFrame(root, text="Click Interval",bd=2)
timeInput_frame.pack(fill='x', padx=10, pady=10, side='top')

hours_label = tk.Label(timeInput_frame, text="Hours:", font=("Arial", 9))
hours_label.grid(row=0, column=0, padx=(10,0))
hours_InputFrame = tk.Entry(timeInput_frame, width=8)
hours_InputFrame.insert(0, "0")
hours_InputFrame.grid(pady=5, padx=5, row=0, column=1)
hours_InputFrame.bind("<FocusOut>", lambda event: save_settings())

minutes_label = tk.Label(timeInput_frame, text="Mins:", font=("Arial", 9))
minutes_label.grid(row=0, column=2)
minutes_InputFrame = tk.Entry(timeInput_frame, width=8)
minutes_InputFrame.insert(0, "0")
minutes_InputFrame.grid(pady=5, padx=5, row=0, column=3)
minutes_InputFrame.bind("<FocusOut>", lambda event: save_settings())

seconds_label = tk.Label(timeInput_frame, text="Secs:", font=("Arial", 9))
seconds_label.grid(row=0, column=4)
seconds_InputFrame = tk.Entry(timeInput_frame, width=8)
seconds_InputFrame.insert(0, "0")
seconds_InputFrame.grid(pady=5, padx=5, row=0, column=5)
seconds_InputFrame.bind("<FocusOut>", lambda event: save_settings())

miliseconds_label = tk.Label(timeInput_frame, text="Milisecs:", font=("Arial", 9))
miliseconds_label.grid(row=0, column=6)
miliseconds_InputFrame = tk.Entry(timeInput_frame, width=8)
miliseconds_InputFrame.insert(0, "100")
miliseconds_InputFrame.grid(pady=5, padx=5, row=0, column=7)
miliseconds_InputFrame.bind("<FocusOut>", lambda event: save_settings())

# -INTERVAL INSIDE MULTI TARGET CYCLE-
timeMultiTargetInput_frame = tk.LabelFrame(root, text="Multitarget InCycle Click Interval",bd=2)
timeMultiTargetInput_frame.pack(fill='x', padx=10, pady=(0,10), side='top')

hoursMultiTarget_label = tk.Label(timeMultiTargetInput_frame, text="Hours:", font=("Arial", 9))
hoursMultiTarget_label.grid(row=0, column=0, padx=(10,0))
hoursMultiTarget_InputFrame = tk.Entry(timeMultiTargetInput_frame, width=8)
hoursMultiTarget_InputFrame.insert(0, "0")
hoursMultiTarget_InputFrame.grid(pady=5, padx=5, row=0, column=1)
hoursMultiTarget_InputFrame.bind("<FocusOut>", lambda event: save_settings())

minutesMultiTarget_label = tk.Label(timeMultiTargetInput_frame, text="Mins:", font=("Arial", 9))
minutesMultiTarget_label.grid(row=0, column=2)
minutesMultiTarget_InputFrame = tk.Entry(timeMultiTargetInput_frame, width=8)
minutesMultiTarget_InputFrame.insert(0, "0")
minutesMultiTarget_InputFrame.grid(pady=5, padx=5, row=0, column=3)
minutesMultiTarget_InputFrame.bind("<FocusOut>", lambda event: save_settings())

secondsMultiTarget_label = tk.Label(timeMultiTargetInput_frame, text="Secs:", font=("Arial", 9))
secondsMultiTarget_label.grid(row=0, column=4)
secondsMultiTarget_InputFrame = tk.Entry(timeMultiTargetInput_frame, width=8)
secondsMultiTarget_InputFrame.insert(0, "0")
secondsMultiTarget_InputFrame.grid(pady=5, padx=5, row=0, column=5)
secondsMultiTarget_InputFrame.bind("<FocusOut>", lambda event: save_settings())

milisecondsMultiTarget_label = tk.Label(timeMultiTargetInput_frame, text="Milisecs:", font=("Arial", 9))
milisecondsMultiTarget_label.grid(row=0, column=6)
milisecondsMultiTarget_InputFrame = tk.Entry(timeMultiTargetInput_frame, width=8)
milisecondsMultiTarget_InputFrame.insert(0, "10")
milisecondsMultiTarget_InputFrame.grid(pady=5, padx=5, row=0, column=7)
milisecondsMultiTarget_InputFrame.bind("<FocusOut>", lambda event: save_settings())

# ------SETTINGS-------
settings_frame = tk.LabelFrame(root, text="Settings", bd=2)
settings_frame.pack(fill='x', padx=10, pady=(0,10), side='top')
settings_frame.columnconfigure(0,weight=1)
settings_frame.columnconfigure(1,weight=1)

# -MODE SELECTION-
Mode = tk.IntVar()
Mode.set(1)
selected_option=tk.StringVar()
options = ["Left", "Right", "Middle"]  

modeSelection_frame = tk.LabelFrame(settings_frame, text="Mode Selection", bd=2)
modeSelection_frame.grid(row=0, column=0, sticky='we', padx=10, pady=(0,10))

infiniteMode_toggle = tk.Radiobutton(modeSelection_frame, variable=Mode, value=1)
infiniteMode_toggle.grid(row=0, column=0)
infiniteMode_label=tk.Label(modeSelection_frame, text="Repeat until stoped")
infiniteMode_label.grid(row=0, column=1, columnspan=3, sticky='w')

amountOfClicksMode_toggle = tk.Radiobutton(modeSelection_frame, variable=Mode, value=2)
amountOfClicksMode_toggle.grid(row=1, column=0, pady=5)
amountOfClicksMode_labelPart1=tk.Label(modeSelection_frame, text="Repeat")
amountOfClicksMode_labelPart1.grid(row=1, column=1)
amountOfClicksMode_InputFrame=tk.Entry(modeSelection_frame, width=10)
amountOfClicksMode_InputFrame.insert(0,"10")
amountOfClicksMode_InputFrame.grid(row=1, column=2, padx=5)
amountOfClicksMode_labelPart2=tk.Label(modeSelection_frame, text="times")
amountOfClicksMode_labelPart2.grid(row=1, column=3, sticky='w')

mouseButtonSelection_label = tk.Label(modeSelection_frame, text="Mouse button to click:")
mouseButtonSelection_label.grid(row=3, column=0, columnspan=3)
mouseButtonSelection_dropdown = ttk.Combobox(modeSelection_frame, state="readonly", values=options, textvariable=selected_option, width=10)
if not selected_option.get(): mouseButtonSelection_dropdown.current(0)
mouseButtonSelection_dropdown.grid(row=3, column=3, pady=(0,5))
mouseButtonSelection_dropdown.bind("<<ComboboxSelected>>", update_mouse_button)

# -OTHER SETTINGS-
isStayOnTop = tk.BooleanVar()
isMultiTarget = tk.BooleanVar()

otherSettings_frame = tk.LabelFrame(settings_frame, text="Other Settings", bd=2)
otherSettings_frame.grid(row=0, column=1, sticky='nswe', padx=(0,10), pady=(0,10))

stayOnTop_checkButton = tk.Checkbutton(otherSettings_frame, onvalue=True, offvalue=False, variable=isStayOnTop, command=stayOnTop)
stayOnTop_checkButton.grid(row=0, column=0)
stayOnTop_label = tk.Label(otherSettings_frame, text="Stay on top")
stayOnTop_label.grid(row=0, column=1)

multiTarget_checkButton = tk.Checkbutton(otherSettings_frame, onvalue=True, offvalue= False, variable=isMultiTarget, command=save_settings)
multiTarget_checkButton.grid(row=1, column=0)
multiTarget_label = tk.Label(otherSettings_frame, text="Multi target")
multiTarget_label.grid(row=1, column=1)

# -----------------------

# -KEY BINDING- 
keyBinding_frame = tk.LabelFrame(root, text="Key Binding", bd=2 )  
keyBinding_frame.pack(padx=10, pady=(0,10), fill='x')

startKeyBinding_label = tk.Label(keyBinding_frame, text="Start/Stop Hotkey:")
startKeyBinding_label.grid(row=0, column=0, padx=(10,0))
startKeyBinding_button = tk.Button(keyBinding_frame, text="F8", command=lambda: start_listening("start"),width=10)
startKeyBinding_button.grid(row=0,column=1,pady=(0,5))

addTargetKeyBindig_label = tk.Label(keyBinding_frame, text="Add target Hotkey:")
addTargetKeyBindig_label.grid(row=1, column=0,pady=(0,10), padx=(10,0))
addTargetKeyBindig_button = tk.Button(keyBinding_frame, text="Q", command=lambda: start_listening("add_target"), width=10)
addTargetKeyBindig_button.grid(row=1, column=1, pady=(0,5))

deleteTargetKeyBindig_label = tk.Label(keyBinding_frame, text="Delete last target Hotkey:")
deleteTargetKeyBindig_label.grid(row=0, column=2,pady=(0,10), padx=(20,0))
deleteTargetKeyBindig_button = tk.Button(keyBinding_frame, text="E", command=lambda: start_listening("delete_target"), width=10)
deleteTargetKeyBindig_button.grid(row=0, column=3, pady=(0,5))

# -START AND STOP BUTTONS-  
StartStop_frame = tk.Frame(root)
StartStop_frame.pack(fill='x')
StartStop_frame.columnconfigure(0, weight=1)
StartStop_frame.columnconfigure(1, weight=1)

startButton = tk.Button(StartStop_frame, text="Start", font=12, command=changeClickerState_toActive, height=2)
startButton.grid(row=0, column=0, padx=(10,0),sticky='we')

stopButton = tk.Button(StartStop_frame, text="Stop", font=12, command=changeClickerState_toUnActive, height=2)
stopButton.grid(row=0, column=1, padx=10, sticky='we')

#------END OF GUI SETUP------

# -OVERLAY WINDOW TO MAKE TARGETS VISIBLE-
overlay = tk.Toplevel(root, bg="gray")
canvas = tk.Canvas(overlay, bg="gray", highlightthickness=0)
canvas.pack(fill="both", expand=True)
root.update_idletasks()
screen_width = root.winfo_screenwidth()    
screen_height = root.winfo_screenheight()
overlay.geometry(f"{screen_width}x{screen_height}+0+0") 
overlay.overrideredirect(True)
overlay.attributes("-topmost", True)
overlay.attributes("-transparentcolor", "gray")
overlay.update() 

# -WIN32 CONSTANTS-
GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020
LWA_COLORKEY = 0x00000001
COLOR_GRAY = 0x808080

hwnd = overlay.winfo_id()

current_style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
new_style = current_style | WS_EX_LAYERED | WS_EX_TRANSPARENT
ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, new_style)

ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, COLOR_GRAY, 0, LWA_COLORKEY)

root.deiconify()

print(f"Overlay Geometry State: {overlay.winfo_geometry()}")
print(f"Overlay Visibility State: {overlay.winfo_viewable()}")

def redraw():
    canvas.delete("all")
    for target in targets:
        canvas.create_oval(target[0]-5, target[1]-5, target[0]+5, target[1]+5, fill="red", outline="white")
    overlay.update_idletasks()



Icon = ImageTk.PhotoImage(Image.open(icon_path))
root.iconphoto(False, Icon)

Mouse = Controller()
        
# -MAIN CLICKER FUNCTION-
def Clicker():
    global IsClickerActive
    
    while True:

        try:
            hours = float(hours_InputFrame.get() or 0)
            minutes = float(minutes_InputFrame.get() or 0)
            seconds = float(seconds_InputFrame.get() or 0)
            miliseconds = float(miliseconds_InputFrame.get() or 0)
            
            delay = (hours * 3600) + (minutes * 60) + seconds + (miliseconds / 1000)
            
            if delay <= 0: 
                delay = 0.1
        except ValueError:
            delay = 0.5 

        if not IsClickerActive:
            time.sleep(0.1)
            continue    

        if isMultiTarget.get() and targets:   
            try:
                hoursMultiTarget = float(hoursMultiTarget_InputFrame.get() or 0)
                minutesMultiTarget = float(minutesMultiTarget_InputFrame.get() or 0)
                secondsMultiTarget = float(secondsMultiTarget_InputFrame.get() or 0)
                milisecondsMultiTarget = float(milisecondsMultiTarget_InputFrame.get() or 0)
                
                delayMultiTarget = (hoursMultiTarget * 3600) + (minutesMultiTarget * 60) + secondsMultiTarget + (milisecondsMultiTarget / 1000)
                
                if delayMultiTarget <= 0: 
                    delayMultiTarget = 0.01
            except ValueError:
                delayMultiTarget = 0.01


            if Mode.get()==1: 
                for target in targets:
                    if not IsClickerActive: break
                    Mouse.position = (target[0],target[1])
                    time.sleep(delayMultiTarget)
                    Mouse.click(MouseButtonToClick)
                time.sleep(delay)
            else:
                try:
                    amountOfClicks = int(amountOfClicksMode_InputFrame.get() or 1)
                except:
                    amountOfClicks = 10

                for i in range(amountOfClicks):
                    for target in targets:
                        if not IsClickerActive: break
                        Mouse.position = (target[0],target[1])
                        time.sleep(delayMultiTarget)
                        Mouse.click(MouseButtonToClick)
                    time.sleep(delay)
                IsClickerActive=False
        else:
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

#IF THE START/STOP HOTKEY IS PRESSED CHANGE TO CLICKER IS ACTIVE
def on_click(key):
    global IsClickerActive
    if (hasattr(key,'char') and key.char is not None and key.char==StartHotkey) or (getattr(key,'name','') and key.name.lower()==StartHotkey): IsClickerActive = not IsClickerActive

# -EVERYTHING FOR CATCHING PRESS OF ADD TARGET HOTKEY
def on_addTarget_click(key):
    if (
        ((hasattr(key,'char') and key.char is not None and key.char==addTargetHotkey) or 
        (getattr(key,'name','') and key.name.lower()==addTargetHotkey)) and 
        isMultiTarget.get()
        ): 
            time.sleep(0.1)
            mouseListener = MouseListener(on_click=add_target)
            mouseListener.start()

def add_target(x, y, button, pressed):
    global targets
    if button == Button.left and pressed: 
        targets.append([x,y])
        redraw()
        return False #This line is to destroy listener

def delete_target(key):
    if (
        ((hasattr(key,'char') and key.char is not None and key.char==deleteTargetHotkey) or 
        (getattr(key,'name','') and key.name.lower()==deleteTargetHotkey)) and 
        isMultiTarget.get() and targets
        ):
            del targets[-1]
            redraw()
    
KeyboardAddTargetListener = Listener(on_press = on_addTarget_click)
KeyboardAddTargetListener.daemon=True
KeyboardAddTargetListener.start()

KeyboardDeleteTargetListener = Listener(on_press=delete_target)
KeyboardDeleteTargetListener.daemon=True
KeyboardDeleteTargetListener.start()

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

load_settings()
root.mainloop()

#time.sleep(delay*AmountOfClicks+1)