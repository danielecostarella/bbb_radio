#!/usr/bin/python

#
# HD44780 LCD Driver for BeagleBone and BeagleBone Black
# using Adafruit Python library
#
# Authors:  Daniele Costarella  <daniele.costarella@gmail.com>
#           Mario Pucciarelli   <pucciarelli.mario@gmail.com>
#
# Date:     11/30/2013
#

__author__ = "Daniele Costarella and Mario Pucciarelli"
__credits__ = ["Daniele Costarella", "Mario Pucciarelli"]
__license__ = "GPL"
__version__ = "0.1.0"

import Adafruit_BBIO.GPIO as GPIO
from time import sleep

""" LDC pins """
LCD_RS = "P9_12"  #Control operation type: RS = 1 -> data; RS = 0 -> command
LCD_RW = "P9_13"  #Control operation side: RW = 1 -> read; RW = 0 -> write
LCD_E = "P9_14"   #LCD enable pin, send command to lcd on the falling edge
LCD_D = ["P8_11", "P8_12", "P8_14", "P8_15", "P8_16", "P8_17", "P8_18", "P8_26"]  # LCD_D -> [DB7, DB6 ... , DB0]

class LiquidCrystal_4bits:
    
    def __init__(self):
        self.GPIO = GPIO
        
        """ GPIO pins setup """
        self.GPIO.setup(LCD_RS, GPIO.OUT)
        self.GPIO.setup(LCD_E, GPIO.OUT)
        self.GPIO.setup(LCD_RW, GPIO.OUT)

        for i in range(0, 4):
            GPIO.setup(LCD_D[i], GPIO.OUT)
        
        print "[DEBUG] 4-operation setup: OK"
        
        """ LCD Initialization """
        self.GPIO.output(LCD_E,GPIO.LOW)        # put enable pin low
        sleep(0.01)
        self.writeByte(0x33,'cmd')              # function set
        self.writeByte(0x32,'cmd')              #
        self.writeByte(0x28,'cmd')              # 4 bit operation, 2 lines, 5x8 dots 
        self.writeByte(0x0C,'cmd')              # display on/off control: display on, cursor off 
        self.writeByte(0x06,'cmd')              # entry mode set: increase address by one, no shift
        self.writeByte(0x01,'cmd')
        
    def enablePulse(self):
        """ Put Enable pin to HIGH and then put back to LOW """
        self.GPIO.output(LCD_E, GPIO.HIGH)
        # wait 1 ms
        #time.sleep(0.001)
        self.GPIO.output(LCD_E, GPIO.LOW)
        
    def clear(self):
        self.writeByte(0x01, 'cmd')             # clear display
        self.writeByte(0x02, 'cmd')             # go home
        
    def home(self):
        self.writeByte(0x02, 'cmd')
        
    def goto(self, line, offset):
        """ definition of a dictionary with the inital index of every line on the lcd """
        position = {1:0x00, 2:0x40, 3:0x14, 4:0x54}
        
        """ send the command to the lcd with the desidered position """
        self.writeByte( (0x80 | (position[line] + (offset-1))), 'cmd')
        
    def writeln(self, line, data):
        # check length of the string to be write
        if (len(data) > 20):
            print "[ERROR] Wrong data string length"
        else:
            # fill all the 20 characters of a display line (not used will be fill with space
            data = data.ljust(20)
            #Go to selected line
            self.goto(line,1)
            #Write the string
            for i in range(0,20):    
                self.writeByte(data[i], 'data')
                
    def write(self, text):
        """ Send a string to LCD. Line feed character switch to the next line """
        
        for char in text:
            if char == "\n":
                self.writeByte(0xC0, 'cmd')
            else:
                self.writeByte(ord(char), 'data')
    
    def writeByte(self, byte, mode):
        """ Write most significant nibble first """
        if type(byte)==int:    
            byte = '{:08b}'.format(byte)        # format hex value in binary format
        else:
            byte = '{:08b}'.format(ord(byte))   # byte is a char
            
        self.GPIO.output(LCD_RW, GPIO.LOW)      # RW=0 -> Write

        """ put data on output port """
        for i in range(0, 4):
            if byte[i] == '1': 
                self.GPIO.output(LCD_D[i], GPIO.HIGH)
            else: 
                self.GPIO.output(LCD_D[i], GPIO.LOW)

        """ set RS mode """
        if mode == 'cmd':
            self.GPIO.output(LCD_RS, GPIO.LOW)
        elif mode == 'data':
            self.GPIO.output(LCD_RS, GPIO.HIGH)
        else:
            print "[DEBUG] Error in mode selection"
            
        self.enablePulse()
    
        """ put data on output port """
        for i in range(4, 8):
            if byte[i] == '1': 
                self.GPIO.output(LCD_D[i-4], GPIO.HIGH)
            else: 
                self.GPIO.output(LCD_D[i-4], GPIO.LOW)
    
        """ set RS mode """
        if mode == 'cmd':
            GPIO.output(LCD_RS, GPIO.LOW)
        elif mode == 'data':
            GPIO.output(LCD_RS, GPIO.HIGH)
        else:
            print "[DEBUG] Error in mode selection"

        self.enablePulse()

class LiquidCrystal_8bits:
    
    def __init__(self):
        self.GPIO = GPIO
        
        """ GPIO pins setup """
        self.GPIO.setup(LCD_RS, GPIO.OUT)
        self.GPIO.setup(LCD_E, GPIO.OUT)
        self.GPIO.setup(LCD_RW, GPIO.OUT)

        for i in range(0, 8):
            GPIO.setup(LCD_D[i], GPIO.OUT)
        
        print "[DEBUG] 8-operation setup: OK"
        
        """ LCD Initialization """
        self.GPIO.output(LCD_E,GPIO.LOW)        # put enable pin low
        sleep(0.01)
        self.writeByte(0x30,'cmd')              # function set
        sleep(0.01)
        self.writeByte(0x30,'cmd')
        sleep(0.01)
        self.writeByte(0x30,'cmd')
        self.writeByte(0x3C,'cmd')              # specify number of lines and character font 
        self.writeByte(0x08,'cmd')              # display off
        self.writeByte(0x01,'cmd')              # display Clear
        self.writeByte(0x05,'cmd')              # entry mode set
        sleep(0.1)
        self.writeByte(0x38, 'cmd')             # 8 bit op, 2 lines, 5x8 dots character font
        sleep(0.01)
        self.writeByte(0x0C, 'cmd')             # display on/off control: display on, cursor off
        sleep(0.01)
        self.writeByte(0x06, 'cmd')             # entry mode set: increase address by one, no shift
        sleep(0.01)
        
        print "[DEBUG] Init done"
        
    def enablePulse(self):
        """ Put Enable pin to HIGH and then put back to LOW """
        self.GPIO.output(LCD_E, GPIO.HIGH)
        # wait 1 ms
        #time.sleep(0.001)
        self.GPIO.output(LCD_E, GPIO.LOW)
        
    def clear(self):
        self.writeByte(0x01, 'cmd')             # clear display
        self.writeByte(0x02, 'cmd')             # go home
        
    def home(self):
        self.writeByte(0x02, 'cmd')
        
    def goto(self, line, offset):
        """ definition of a dictionary with the inital index of every line on the lcd """
        position = {1:0x00, 2:0x40, 3:0x14, 4:0x54}
        
        """ send the command to the lcd with the desidered position """
        self.writeByte( (0x80 | (position[line] + (offset-1))), 'cmd')
        
    def writeln(self, line, data):
        # check length of the string to be write
        if (len(data) > 20):
            print "[ERROR] Wrong data string length"
        else:
            # fill all the 20 characters of a display line (not used will be fill with space
            data = data.ljust(20)
            #Go to selected line
            self.goto(line,1)
            #Write the string
            for i in range(0,20):    
                self.writeByte(data[i], 'data')
                
    def write(self, text):
        """ Send a string to LCD. Line feed character switch to the next line """
        
        for char in text:
            if char == "\n":
                self.writeByte(0xC0, 'cmd')
            else:
                self.writeByte(ord(char), 'data')
    
    def writeByte(self, byte, mode):
        """ Write most significant nibble first """
        if type(byte)==int:    
            byte = '{:08b}'.format(byte)        # format hex value in binary format
        else:
            byte = '{:08b}'.format(ord(byte))   # byte is a char
            
        self.GPIO.output(LCD_RW, GPIO.LOW)      # RW=0 -> Write

        """ put data on output port """
        for i in range(0, 8):
            if byte[i] == '1': 
                self.GPIO.output(LCD_D[i], GPIO.HIGH)
            else: 
                self.GPIO.output(LCD_D[i], GPIO.LOW)

        """ set RS mode """
        if mode == 'cmd':
            self.GPIO.output(LCD_RS, GPIO.LOW)
        elif mode == 'data':
            self.GPIO.output(LCD_RS, GPIO.HIGH)
        else:
            print "[DEBUG] Error in mode selection"
            
        self.enablePulse()
    
 
if __name__ == '__main__':
    lcd = LiquidCrystal_8bits()
    lcd.clear()
    lcd.write("Test1\nTest2")
    lcd.writeln(3, 'Hello!')
    lcd.writeln(4, '01234567890123456789')
        