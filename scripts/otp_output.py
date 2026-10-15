import time
import string
import statistics
import serial 
import random
from operator import itemgetter
import gc
gc.disable()

arduino = serial.Serial(port='/dev/cu.usbserial-110', baudrate=115200, timeout=1)

def main():
    arduino.setDTR(False)
    time.sleep(0.1)
    arduino.setDTR(True)
    time.sleep(2)

    arduino.write(b'alandvaarwovhhjskojrykoqkauwcbwjezprdwycmmdoeqotgfajap cncaadltwnbxiqqgqquqsorptsthnrqtdxwzgukqvyqucmehvgbzk\r\n')
    time.sleep(5)
    
    res = ""
    while "C&C" not in res:
        res = arduino.readline().decode()
        
    time.sleep(2)

    attempt = 0
    guess = "1"

    while True:
        attempt += 1
        arduino.write((guess + "\n").encode())
        time.sleep(0.2)
        line = arduino.readline().decode(errors="replace").strip()
        print(line)
        print(line + "\n")

if __name__ == '__main__':
    main()
