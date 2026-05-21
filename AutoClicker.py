from pynput.keyboard import Listener, Key
from pynput.mouse import Button, Controller 
import time
import threading

delay = 0.5
AmountOfClicks = 10
IsClickerActive=True
IsInfiniteMode = False
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

thread = threading.Thread(target=Clicker)
thread.start()

time.sleep(delay*AmountOfClicks+1)