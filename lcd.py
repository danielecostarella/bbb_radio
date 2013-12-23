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
# 	byte -> byte to send to lcd (hex format). It can be a numeric value or a character	      
# 	mode -> type of the operation (data=send a data to lcd to write a char; cmd=send a command to lcd)
# Output value: none
def lcdWriteByte(byte, mode):
    
    if type(byte)==int:    
        # format hex value in binary format
        byte = '{:08b}'.format(byte)
    else
        byte = '{:08b}'.format(ord(byte))   # byte is a char
    
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
    

# Function lcdWriteLine: Write a line on the lcd 
# 
# Parameters: value=number of line to write [1-4]; string=the string to be written on the selected line
# Output value: none
def lcdWriteLine(value, string):
   #Check if the line number is correct
   if ((value < 0) or (value > 4)):
      print ("[DEBUG] can't write a line out of the range 1 - 4")
   else:
   #Determinate how line must be write
   if (value == 1):
      lcdGoToXY(0,1)
   if (value == 2):
      lcdGoToXY(0,2)
   if (value == 3):
      lcdGoToXY(0,3)
   if (value == 4):
      lcdGoToXY(0,4)
   #Once set the cursor on the right position, write the line on the lcd
      lcdWriteString(string)
 

# Function lcdWriteString: Write a string on the lcd at the current position
# 
# Parameters: string=the string to be written on the selected line
# Output value: none
def lcdWriteString(string):
   #Determination of the string length
   length = len(string)
   for i in range (0, length):
      lcdWriteByte(string[i], 'data')


# Function lcdGoToXY: Send cursor to the desidered position 
# 
# Parameters: Xval=the column to be selected; Yval=the row to be selected
# Output value: none
def lcdGoToXY(Xval, Yval):
   #Select row and column
   switch(Yval):
      case 1:
         pos = 0x00
         break
      case 2:
         pos = 0xC0
      case 3:
         pos = 0x14
      case 4:
         pos = 0xD4
      default:
         print ("[DEBUG] Errore in selecting the line number")
   pos = pos + (XVal - 1)   
   #Set DDRAM to the new position
   value = 0x80 or pos
   lcdWriteByte(value, 'cmd')   

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
    lcdInit()
    #welcome()
    lcdWriteByte('a')
    time.sleep(20)
    lcdWriteString("ciao")
    while(1): time.sleep(1)
