import Adafruit_BBIO.GPIO as GPIO
import time


# LDC pins
LCD_RS = "P9_12"  #Control operation type: RS = 1 -> data; RS = 0 -> command
LCD_RW = "P9_13"  #Control operation side: RW = 1 -> read; RW = 0 -> write
LCD_E = "P9_14"   #LCD enable pin, send command to lcd on the falling edge
LCD_D = ["P8_11", "P8_12", "P8_14", "P8_15", "P8_16", "P8_17", "P8_18", "P8_26"] # [DB7, DB6 ... , DB0]


# Function setup: Configure the pins of the BBB for properly operation
# 
# Parameters: none
# Output value: none
def setup():
    GPIO.setup(LCD_RS, GPIO.OUT)
    GPIO.setup(LCD_E, GPIO.OUT)
    GPIO.setup(LCD_RW, GPIO.OUT)

    for i in range(0, 8):
        GPIO.setup(LCD_D[i], GPIO.OUT)

    print "setup done"



# Function lcdWriteByte: Send a byte to lcd
# 
# Parameters: 
# 	byte -> byte to send to lcd (hex format)	      
# 	mode -> type of the operation (data=send a data to lcd to write a char; cmd=send a command to lcd)
# Output value: none
def lcdWriteByte(byte, mode):
    
    # format hex value in binary format
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
    GPIO.output(LCD_RW, GPIO.LOW) 

    # E -> 1
    GPIO.output(LCD_E, GPIO.HIGH)
    # wait 1 ms
    time.sleep(0.01)
    # E -> 0
    GPIO.output(LCD_E, GPIO.LOW)


# Function lcdInit: initialize lcd 
# 
# Parameters: none
# Output value: none
def lcdInit():
    #Put enable pin low
    GPIO.output(LCD_E,GPIO.LOW)   
    time.sleep(0.01)
    #Function set
    lcdWriteByte(0x30,'cmd')   
    time.sleep(0.01)
    lcdWriteByte(0x30,'cmd')
    time.sleep(0.01)
    lcdWriteByte(0x30,'cmd')
    #Specify number of lines and character font
    lcdWriteByte(0x3C,'cmd') 
    #Display Off
    lcdWriteByte(0x08,'cmd')
    #Display Clear 
    lcdWriteByte(0x01,'cmd') 
    #Entry mode set
    lcdWriteByte(0x05,'cmd') 
    time.sleep(0.1)
    print "init done"
    

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


if __name__ == '__main__':
    print "inizio test"
    setup()
    init()
    welcome()
    while(1): time.sleep(1)
