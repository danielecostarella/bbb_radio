import os
import subprocess
import time
import sys
import re
import lcd
import threading

stations={'JAZZ': 'http://www.radioswissjazz.ch/live/aacp.m3u', 'Virgin Radio': 'http://shoutcast.unitedradio.it:1301','Deejay': 'http://mp3.kataweb.it:8000/RadioDeejay','105Hits': 'http://shoutcast.unitedradio.it:1109/listen.pls'}
volume = 25 	#default volume value for mplayer 
streamTitle=""
pause = 0
lines = [1, 2, 3, 4]

#p = subprocess.Popen(["mplayer","-ao","alsa:device=hw=1.0", "-quiet", "-slave", "http://shoutcast.unitedradio.it:1301"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#p = subprocess.Popen(["mplayer","-ao","alsa:device=hw=1.0", "-slave", "-playlist", "http://www.radioswissjazz.ch/live/aacp.m3u"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
#p = subprocess.Popen(["mplayer","-ao","alsa:device=hw=1.0", "-slave", "-mixer-channel", "-playlist", stations['JAZZ']], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
p = subprocess.Popen(["mplayer","-ao","alsa:device=hw=1.0", "-slave", "-playlist", stations['JAZZ']], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

# set the lcd up
lcd.setup()
lcd.init()
# to be called as a new thread
#def waitCmd():

# to be called as a new thread
def streamAnalysis():
    global streamTitle
    print "[DEBUG] Thread analysis"
    for line in p.stdout:
        if line.startswith("ICY Info"):
            info = line.split(':', 1)[1].strip()
            attr = dict(re.findall("(\w+)='([^']*)'", info))
            print '[DEBUG] Stream title: '+ attr.get('StreamTitle', '(none)')
            #streamTitle = '[DEBUG] Stream title: '+ attr.get('StreamTitle', '(none)')
            streamTitle = attr.get('StreamTitle', '(none)')
            print streamTitle


lcd.writeln(1, "Welcome!")
print "Welcome!"

t = threading.Thread(target=streamAnalysis)
t.start()


"""
for line in p.stdout:
    if line.startswith("ICY Info"):
        info = line.split(':', 1)[1].strip()
        attr = dict(re.findall("(\w+)='([^']*)'", info))
        print '[DEBUG] Stream title: '+ attr.get('StreamTitle', '(none)')
"""
#out, err = p.communicate()
#------Mario 08/02/2014 tolta la pausa di 5 secondi per fare prove su controllo volume
#time.sleep(5)
#p.stdin.write('pause\n') #funziona
#subprocess.Popen(["echo","'pause\n'"], shell=True, stdin=subprocess.PIPE).stdin
#sys.stdin = sys.stdout
#print "prima pausa"
#sys.stdout.write("pause\n")
#time.sleep(5)
#p.stdin.write('pause\n') #funziona play di nuovo
#print "play di nuovo"
#sys.stdout.write("pause\n")
sys.stdin = sys.__stdin__ #restore original stdin 
#print "[INFO] Versione DEMO: solo 15 secondi di radio..."
#time.sleep(15)
#p.kill()

def function1():
    print "Run function 1"
    global volume
    volume = volume + 5
    string = "set_property volume %d\n"  %(volume)
    print "Setting volume: %d\n" %(volume) 
    #p.stdin.write('set_property volume 10\n')
    p.stdin.write(string)

def function2():
    print "Run function 2"
    global volume
    volume = volume - 5
    print "Setting volume: %d\n" %(volume)
    string = 'set_property volume %d\n' %(volume)
    p.stdin.write(string)
    #p.stdin.write('set_property volume 40\n')

def function3():
    global pause
    print "Run function 3"
    if pause==False: 
        p.stdin.write('pause\n')
        lcd.writeln(4, "**PAUSE**")
        pause = True
    else:
        p.stdin.write('pause\n')
        lcd.writeln(4, "") # clear line 4
        pause = False	

def function4():
    global streamTitle
    print "Run function 4"
    print streamTitle
    lcd.writeln(2, streamTitle[0:20])

def updateLCD():
    global lines 
    global streamTitle
    while(1):
        lines[1] = streamTitle
        lcd.writeln(2, lines[1][0:20])
        #lcd.writeln(2, streamTitle[0:20])
        time.sleep(1)

t2 = threading.Thread(target=updateLCD)
t2.start()


# read event streaming
evt_file = open("/dev/input/event1", "rb")
while(1):
    #lcd.writeln(2, streamTitle[0:20])
    evt = evt_file.read(16) # Read the event
    evt_file.read(16)       # Discard the debounce event 
    code = ord(evt[10])
    #print "Button "+str(code)+" pressed with direction "+str(ord(evt[12]))
    if str(code)=='1' and str(ord(evt[12]))=='1': function1()
    elif str(code)=='2' and str(ord(evt[12]))=='1': function2()
    elif str(code)=='3' and str(ord(evt[12]))=='1': function3()
    elif str(code)=='4' and str(ord(evt[12]))=='1': function4()
