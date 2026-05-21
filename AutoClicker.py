from pynput.keyboard import Listener, Key
from pynput.mouse import Button, Controller 
import time
import threading

delay = 0.5
AmountOfClicks = 10
IsClickerActive=False
IsInfiniteMode = True
MouseButtonToClick = Button.left    

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

thread = threading.Thread(target=Clicker)
thread.start()

with Listener(on_press = on_click) as listener:
    listener.join()   

#time.sleep(delay*AmountOfClicks+1)