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
    else:
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


# Function init: initialize lcd 
# 
# Parameters: none
# Output value: none
def init():
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
    #lcd_w('0000111000')
    lcdWriteByte(0x38, 'cmd')   # function set: 8 bit operation, 2 lines, 5x8 dots character font
    time.sleep(0.01)
    #lcd_w('0000001110')
    lcdWriteByte(0x0C, 'cmd')   # display on/off control: display on, cursor off
    time.sleep(0.01)
    #lcd_w('0000000110')
    lcdWriteByte(0x06, 'cmd')   # entry mode set: increase address by one, no shift
    time.sleep(0.01)
    #lcd_w('1001010111')

# Function writeln: Write a line on the lcd 
# 
# Parameters: line=number of lcd line on wich write string; data=the string to be written
# Output value: none
def writeln(line, data):
    #Check length of the string to be write
    if (len(data) > 20):
        print "ERROR: wrong string length"
    else:
    #Fill all the 20 characters of a display line (not used will be fill with space
        data = data.ljust(20)
        #Go to selected line
        goto(line,1)
        #Write the string
        for i in range(0,19):    
            lcdWriteByte(data[i], 'data')


# Function writestr: Write a string on the lcd at the current position
# 
# Parameters: string=the string to be written on the selected line
# Output value: none
def writestr(data):
   #Determination of the string length
   length = len(data)
   #Write the string
   for i in range (0, length):
      lcdWriteByte(data[i], 'data')


# Function goto: Send the cursor to the desidered position on lcd 
# 
# Parameters: line=the line to go to [1-4]; offset=the character index on the line previously indicated
# Output value: none
def goto(line, offset):
    #Define a dictionary with the inital index of every line on the lcd
    position = {1:0x00, 2:0x40, 3:0x14, 4:0x54}
    #Send the command to the lcd with the desidered position
    lcdWriteByte( (0x80 | (position[line] + (offset-1))), 'cmd')    
        


# Function clear: clear the whole display
# 
# Parameters: none
# Output value: none
def clear():
    lcdWriteByte(0x01, 'cmd')   # clear display
    lcdWriteByte(0x02, 'cmd')   # go home

def welcome():
    lcdWriteByte(0x57, 'data')  # write 'W' char
    time.sleep(0.01)    


if __name__ == '__main__':
    print "inizio test"
    setup()
    lcdInit()
    #welcome()
    print "Scrivo 'a'"
    lcdWriteByte('a', 'data')
    time.sleep(5)
    print "Scrivo 'ciao'"
    lcdWriteString("ciao")
    time.sleep(2)
    goto(2,4)
    lcdWriteString("Vittoria!")
    writeln(3,'01234567890123456789')
    while(1): time.sleep(1)
