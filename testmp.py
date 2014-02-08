import os
import subprocess
import time
import sys
import re
import lcd
import threading

stations={'JAZZ': 'http://www.radioswissjazz.ch/live/aacp.m3u', 'Virgin Radio': 'http://shoutcast.unitedradio.it:1301'}

#p = subprocess.Popen(["mplayer","-ao","alsa:device=hw=1.0", "-quiet", "-slave", "http://shoutcast.unitedradio.it:1301"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#p = subprocess.Popen(["mplayer","-ao","alsa:device=hw=1.0", "-slave", "-playlist", "http://www.radioswissjazz.ch/live/aacp.m3u"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
p = subprocess.Popen(["mplayer","-ao","alsa:device=hw=1.0", "-slave", "-playlist", stations['JAZZ']], stdin=subprocess.PIPE, stdout=subprocess.PIPE)


# set the lcd up
lcd.setup()
lcd.init()

# to be called as a new thread
#def waitCmd():

# to be called as a new thread
def streamAnalysis():
    print "[DEBUG] Thread analysis"
    for line in p.stdout:
        if line.startswith("ICY Info"):
            info = line.split(':', 1)[1].strip()
            attr = dict(re.findall("(\w+)='([^']*)'", info))
            print '[DEBUG] Stream title: '+ attr.get('StreamTitle', '(none)')

lcd.writeln(3, "Welcome!")
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
time.sleep(5)
p.stdin.write('pause\n') #funziona
#subprocess.Popen(["echo","'pause\n'"], shell=True, stdin=subprocess.PIPE).stdin
#sys.stdin = sys.stdout
#print "prima pausa"
#sys.stdout.write("pause\n")
time.sleep(5)
p.stdin.write('pause\n') #funziona play di nuovo
#print "play di nuovo"
#sys.stdout.write("pause\n")
sys.stdin = sys.__stdin__ #restore original stdin 
print "[INFO] Versione DEMO: solo 15 secondi di radio..."
#time.sleep(15)
#p.kill()
while(1):
    time.sleep(1)
