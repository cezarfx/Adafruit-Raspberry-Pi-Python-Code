#!/usr/bin/python

#
# Code by Cezar Andrei 3/25/2016
#

from Adafruit_PWM_Servo_Driver import PWM
import time
import termios, fcntl, sys, os


# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
pwm = PWM(0x40)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)

freq = 100       # Initial freq in Hz
ch =     0       # Servo channel
min =  210       # min pulse threshhold, modify this with value before servo is not responding
max = 1100       # max pulse threshhold, modify this with value before servo is not responding
servoMin = 290   # initial Min pulse length out of 4096
servoMax = 300   # initial Max pulse length out of 4096

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= freq                     # ex 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)




fd = sys.stdin.fileno()

oldterm = termios.tcgetattr(fd)
newattr = termios.tcgetattr(fd)
newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
termios.tcsetattr(fd, termios.TCSANOW, newattr)

oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

print ' '
print 'Use keys to find out the frequency, min, max and middle values of your servo'
print '  5 : ch += 1'
print '  6 : ch -= 1'
print '  o : freq += 10'
print '  l : freq -= 10'
print '  a : servoMin += 10'
print '  z : servoMin -= 10'
print '  d : servoMax += 10'
print '  c : servoMax -= 10'
print '  m : go to middle of servoMin and servoMax'
print '  r : read from i2c, always returns 0'
print '  q : quit'
print ' '


pwm.setPWMFreq(freq)                        # Set frequency to 60 Hz

try:
  while 1:
    try:
      c = sys.stdin.read(1)
      # print "Got character", repr(c)
      if c == 'z':
        servoMin -= 10
		    if servoMin < min:
          servoMin = min
        print "Min-: " + str(servoMin)
        pwm.setPWM(ch, 0, servoMin)
      if c == 'a':
        servoMin += 10
        if servoMin > max:
          servoMin = max
        print "Min+: " + str(servoMin)
        pwm.setPWM(ch, 0, servoMin)                
      if c == 'd':
        servoMax += 10
		    if servoMax > max:
          servoMax = max
        print "Max+: " + str(servoMax)
        pwm.setPWM(ch, 0, servoMax)
      if c == 'c':
        servoMax -= 10
		    if servoMax < min:
          servoMax = min
        print "Max-: " + str(servoMax)
        pwm.setPWM(ch, 0, servoMax)
      if c == 'l':
        freq -= 10
        print "Freq-: " + str(freq)
        pwm.setPWMFreq(freq)                        # Set frequency
      if c == 'o':
        freq += 10
        print "Freq+: " + str(freq)
        pwm.setPWMFreq(freq)                        # Set frequency
      if c == 'm':
        print 'Middle ' + str( (servoMin + servoMax) / 2 )
        pwm.setPWM(ch, 0, (servoMin + servoMax) / 2 )
      if c == 'r':
        print 'Reading from servo: '
        val = pwm.i2c.readU16(ch)
        print '  val = ' + str(val)
      if c == '5':
        ch -= 1
        if ch < 0:
          ch = 0
        print 'Channel-: ' + str(ch)
      if c == '6':
        ch += 1
        if ch > 15:
          ch = 15
        print 'Channel+: ' + str(ch)
      if c == 'q':
        break
                
    except IOError: pass
finally:
  termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
  fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
