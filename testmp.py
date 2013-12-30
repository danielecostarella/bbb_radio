import os
import subprocess
import time
import sys
import re
import lcd

#p = subprocess.Popen(["mplayer","-ao","alsa:device=hw=1.0", "-quiet", "-slave", "http://shoutcast.unitedradio.it:1301"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p = subprocess.Popen(["mplayer","-ao","alsa:device=hw=1.0", "-slave", "-playlist", "http://www.radioswissjazz.ch/live/aacp.m3u"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

# set the lcd up
lcd.setup()
lcd.init()

lcd.writeln(3, "Welcome!")
print "Welcome!"
for line in p.stdout:
    if line.startswith("ICY Info"):
        info = line.split(':', 1)[1].strip()
        attr = dict(re.findall("(\w+)='([^']*)'", info))
        print 'Stream title: '+ attr.get('StreamTitle', '(none)')
#out, err = p.communicate()
time.sleep(5)
#p.stdin.write('pause\n')
#subprocess.Popen(["echo","'pause\n'"], shell=True, stdin=subprocess.PIPE).stdin
#sys.stdin = sys.stdout
#sys.stdout.write("pause\n")
sys.stdin = sys.__stdin__ #restore original stdin
#time.sleep(5)
#sys.stdout.write("pause")
#subprocess.call(["echo", "pause"]) 
print "Versione DEMO: solo 15 secondi di radio..."
time.sleep(15)
p.kill()
#print("fatto")
