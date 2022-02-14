from pynput import keyboard as kb
from pynput import mouse
import pyautogui as pag
import matplotlib.pyplot as plt
import pyperclip
import pytesseract
#from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'/Users/nekodigi/opt/anaconda3/bin/tesseract'



retina = True
lang = 'jpn'#eng jpn



COMBINATION = {kb.Key.alt}#ctrl + c to enable
# The currently active modifiers
current = set()
recording = False
startPos = 0, 0
prtsc = None
mouseX = 0
mouseY = 0

def on_press(key):
    if key == kb.Key.esc:
        kListener.stop()
        mListener.stop()
    c = ''
    try:
        c = key.char
    except:
        pass
    if key in COMBINATION:
        current.add(key)
    if all(k in current for k in COMBINATION):# and c == 'c'
        print('All modifiers active!')
        print(mouseX, mouseY)
        global startPos
        startPos = mouseX, mouseY
        global recording
        recording = True
    #print(key)
    
def on_release(key):
    try:
        current.remove(key)
        if not any(k in current for k in COMBINATION):
            copy()
            recording = False
    except KeyError:
        pass
    
def on_move(x,y):
    global mouseX,mouseY
    mouseX = x
    mouseY = y
    
#def on_click(x, y, button, pressed):
    
    #if recording:
        #if pressed:
            
        #if not pressed:#screenshot mouse position is not same due to retina?
   
def copy():
    global recording,startPos,prtsc
    sx = startPos[0]
    sy = startPos[1]
    bx,by,bw,bh = Pos2Box(sx, sy, mouseX, mouseY)
    print(bx, by, bw, bh)
    if bw > 10 and bh>10:
        if retina:
            prtsc = pag.screenshot(region=(bx*2, by*2, bw*2, bh*2))#require screen record permission
        else:
            prtsc = pag.screenshot(region=(bx, by, bw, bh))#require screen record permission
        div = 1
#         if bh > 100:
#             div = 2
#         if bh > 200:
#             div = 4
#         if bh > 400:
#             div = 8
        print(f"start conv{int(bw/div)},{int(bh/div)}")
        prtsc = prtsc.resize((int(bw/div), int(bh/div)))
        plt.imshow(prtsc)
        text = pytesseract.image_to_string(prtsc, lang=lang)#, 
        print(text)
        pyperclip.copy(text)
    #recording = False


def Pos2Box(x1, y1, x2, y2):#2 position to box(x,y,w,h)
    return min(x1, x2), min(y1, y2), abs(x1-x2), abs(y1-y2)
    
    
kListener = kb.Listener(on_press=on_press,on_release=on_release)
mListener = mouse.Listener(on_move=on_move)#on_click=on_click
kListener.start()#s, on_release=m_on_release
mListener.start()
kListener.join()
mListener.join()