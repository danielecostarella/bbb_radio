import Adafruit_BBIO.GPIO as GPIO
import time


# LDC pins
LCD_RS = "P9_12"
LCD_RW = "P9_13"
LCD_E = "P9_14"
LCD_D = ["P8_11", "P8_12", "P8_14", "P8_15", "P8_16", "P8_17", "P8_18", "P8_26"] # [DB7, DB6 ... , DB0]


# Set Pins Directions
def setup():
    GPIO.setup(LCD_RS, GPIO.OUT)
    GPIO.setup(LCD_E, GPIO.OUT)
    GPIO.setup(LCD_RW, GPIO.OUT)

    for i in range(0, 8):
        GPIO.setup(LCD_D[i], GPIO.OUT)

    print "setup done"

# data in bits
# Ex. data = 0010101010
def lcd_w(data):
    
    if data[0] == '0': GPIO.output(LCD_RS, GPIO.LOW)
    else: GPIO.output(LCD_RS, GPIO.HIGH)

    if data[1] == '0': GPIO.output(LCD_RW, GPIO.LOW)
    else: GPIO.output(LCD_RW, GPIO.HIGH)

    for i in range(2,10):
        if data[i] == '0': GPIO.output(LCD_D[i-2], GPIO.LOW)
        else: GPIO.output(LCD_D[i-2], GPIO.HIGH)
    time.sleep(0.01)
    GPIO.output(LCD_E, GPIO.HIGH)
    time.sleep(0.01)
    GPIO.output(LCD_E, GPIO.LOW)

# Send a byte
# mode = data
# mode = cmd
def lcdWriteByte(byte, mode):

    byte = '{:08b}'.format(byte)
    print "Sto scrivendo "+byte+"\n"
    # put data on output port
    for i in range(0, 8):
        if byte[i] == '1': GPIO.output(LCD_D[i], GPIO.HIGH)
        else: GPIO.output(LCD_D[i], GPIO.LOW)

    # set RS mode
    if mode == 'cmd':
        GPIO.output(LCD_RS, GPIO.LOW)
    elif mode == 'data':
        GPIO.output(LCD_RS, GPIO.HIGH)
    else:
        print("[DEBUG] Error in mode selection")

    # RW=0 -> Write
    GPIO.output(LCD_RW, GPIO.LOW) #e braaaaav!

    # E -> 1
    GPIO.output(LCD_E, GPIO.HIGH)
    # wait 1 ms
    time.sleep(0.01)
    # E -> 0
    GPIO.output(LCD_E, GPIO.LOW)


def welcome():
        #lcd_w('0000111000')
        lcdWriteByte(0x38, 'cmd')
        time.sleep(0.01)
        #lcd_w('0000001110')
        lcdWriteByte(0x0C, 'cmd')
        time.sleep(0.01)
        #lcd_w('0000000110')
        lcdWriteByte(0x06, 'cmd')
        time.sleep(0.01)
        #lcd_w('1001010111')
        lcdWriteByte(0x57, 'data')
        time.sleep(0.01)    

def init2():
    GPIO.output(LCD_E, GPIO.LOW)
    time.sleep(1)
    lcd_w('0000110000')
    #print "Sto stampando 0 0 0 0 1 1 0 0 0 0"
    #raw_input()
    time.sleep(0.01)
    lcd_w('0000110000')
    #print "Sto stampando 0 0 0 0 1 1 0 0 0 0"
    #raw_input()
    time.sleep(0.01)
    lcd_w('0000110000')
    #print "Sto stampando 0 0 0 0 1 1 0 0 0 0"
    #raw_input()
    lcd_w('0000111100')
    #print "Sto scrivendo 0 0 0 0 1 1 1 1 0 0"
    #raw_input()
    lcd_w('0000001000')
    #print "Sto scrivendo 0 0 0 0 0 0 1 0 0 0"
    #raw_input()
    lcd_w('0000000001')
    #print "Sto scrivendo 0 0 0 0 0 0 0 0 0 1"
    #raw_input()
    lcd_w('0000000101')
    #print "Sto scrivendo 0 0 0 0 0 0 0 1 0 1"
    #raw_input()
    time.sleep(0.1)
    print "init done"

if __name__ == '__main__':
    print "inizio test"
    setup()
    init2()
    welcome()
    #lcd_w('0000111000')
    while(1): time.sleep(1)
