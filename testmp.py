import os
import subprocess
import time
import sys

p = subprocess.Popen(["mplayer","-ao","alsa:device=hw=1.0", "-quiet", "-slave", "http://shoutcast.unitedradio.it:1301"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
