#! /usr/bin/python
# Written by Jacken Zimmermann http://www.jackenhack.com
# Big screen character clock code written by Adrian Allan 
# http://allan.me/2015/10/30/a-very-simple-raspberry-pi-clock-using-adafruit-16x2-lcd-pi-plate/

from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import os
from time import *
import time
import subprocess
import logging
import re
from decimal import Decimal, ROUND_DOWN
import logging
import optparse

LOGGING_LEVELS = {'critical': logging.CRITICAL,
                  'error': logging.ERROR,
                  'warning': logging.WARNING,
                  'info': logging.INFO,
                  'debug': logging.DEBUG}


# LED colors
OFF                     = 0x00
RED                     = 0x01
GREEN                   = 0x02
BLUE                    = 0x04
YELLOW                  = RED + GREEN
TEAL                    = GREEN + BLUE
VIOLET                  = RED + BLUE
WHITE                   = RED + GREEN + BLUE
ON                      = RED + GREEN + BLUE

# Define digit pairs from 00 to 61 (yes 61 because of leap seconds)
digits=[\
        [24341,25351],[24120,25120],[24161,25370],[24161,25171],[24301,25141],
        [24360,25171],[24360,25371],[24141,25101],[24361,25371],[24341,25141],
        [ 2241, 2251],[ 2020, 2020],[ 2061, 2270],[ 2061, 2071],[ 2201, 2041],
        [2260, 2071],[ 2260, 2271],[ 2041, 2001],[ 2261, 2271],[ 2241, 2041],
        [ 6341,27251],[ 6120,27020],[ 6161,27270],[ 6161,27071],[ 6301,27041],
        [6360,27071],[ 6360,27271],[ 6141,27001],[ 6361,27271],[ 6341,27041],
        [ 6341, 7351],[ 6120, 7120],[ 6161, 7370],[ 6161, 7171],[ 6301, 7141],
        [6360, 7171],[ 6360, 7371],[ 6141, 7101],[ 6361, 7371],[ 6341, 7141],
        [20341, 4351],[20120, 4120],[20161, 4370],[20161, 4171],[20301, 4141],
        [20360, 4171],[20360, 4371],[20141, 4101],[20361, 4371],[20341, 4141],
        [26241, 7351],[26020, 7120],[26061, 7370],[26061, 7171],[26201, 7141],
        [26260, 7171],[26260, 7371],[26041, 7101],[26261, 7371],[26241, 7141],
        [26241,27351],[26020,27120]]

class lcdScreen(object):
  """Class for handling the Adafruit LCDPlate display"""
  def __init__(self, bgColor, txt):
    self.bgColor = bgColor
    self.lcd = Adafruit_CharLCDPlate()
    self.lcd.clear()
    self.lcd.backlight(bgColor)
    self.lcd.message(txt)

    # Create custom characters for LCD for big clock display
    
    # Create some custom characters
    self.lcd.createChar(0, [0, 0, 0, 0, 0, 0, 0, 0])
    self.lcd.createChar(1, [16, 24, 24, 24, 24, 24, 24, 16])
    self.lcd.createChar(2, [1, 3, 3, 3, 3, 3, 3, 1])
    self.lcd.createChar(3, [17, 27, 27, 27, 27, 27, 27, 17])
    self.lcd.createChar(4, [31, 31, 0, 0, 0, 0, 0, 0])
    self.lcd.createChar(5, [0, 0, 0, 0, 0, 0, 31, 31])
    self.lcd.createChar(6, [31, 31, 0, 0, 0, 0, 0, 31])
    self.lcd.createChar(7, [31, 0, 0, 0, 0, 0, 31, 31])
     


    self.timeSinceAction = 0  # The time since the last keypress. Use timeout to start switching screens
#    self.switchScreenTime = 8 #Number of seconds between switching screens
    self.lastScreenTime = time.time()    # time since last screen switch
    self.prevStr = ""
    self.screens = ((self.bigTimeView,6),          # Rotating list of views on LCD with how many seconds to display each display. Round robin style.
                    (self.connectedUserView,4),
                    (self.bigTimeView,6),
                    (self.precisionView,4),
                    (self.bigTimeView,6),
                    (self.ntptimeInfo,5),
                    (self.bigTimeView,6),
                    (self.clockperfView,5),
                    ) # list of all views for rotation
                    
    self.nrofscreens = len(self.screens)
    self.currentScreen = 0

  def writeLCD(self, s):
    """Checks the string, if different than last call, update screen."""
    if self.prevStr.decode("ISO-8859-1") != s.decode("ISO-8859-1"):  # Oh what a shitty way around actually learning the ins and outs of encoding chars...
      # Display string has changed, update LCD
      self.lcd.clear()
      self.lcd.message(s)
      self.prevStr = s  # Save so we can test if screen changed between calls, don't update if not needed to reduce LCD flicker

  def bigTimeView(self):
    """Shows custom large local time on LCD"""

    now=time.localtime()
    hrs=int(time.strftime("%H"))
    minutes=int(time.strftime("%M"))
    sec=int(time.strftime("%S"))
    
    # Build string representing top and bottom rows
    L1="0"+str(digits[hrs][0]).zfill(5)+str(digits[minutes][0]).zfill(5)+str(digits[sec][0]).zfill(5)
    L2="0"+str(digits[hrs][1]).zfill(5)+str(digits[minutes][1]).zfill(5)+str(digits[sec][1]).zfill(5)
    
    # Convert strings from digits into pointers to custom character
    i=0
    XL1=""
    XL2=""
    while i < len(L1):
        XL1=XL1+chr(int(L1[i]))
        XL2=XL2+chr(int(L2[i]))
        i += 1
    
    self.writeLCD(XL1+"\n" +XL2)


  def precisionView(self):
    """Calculate and display the NTPD accuracy"""
    try:
      output = subprocess.check_output("ntpq -c rv", shell=True)
      returncode = 0
    except CalledProcessError as e:
        output = e.output
        returncode = e.returncode
        print returncode
        exit(1)
        
    precision = ""
    clkjitter = ""
    clkwander = ""
    search = re.search( r'.*precision=(.*?),.*clk_jitter=(.*),', output, re.M|re.S)
    if search:
      precision = float(search.group(1))
      precision = (1/2.0**abs(precision))*1000000.0
      theStr = "Prec: {:.5f} {}s\n".format(precision,chr(0xE4))
      theStr += "Jitter: {:>5} ms".format(search.group(2))
    self.writeLCD(theStr)

  def ntptimeInfo(self):
    """Statistics from ntptime command"""
    output = subprocess.check_output("ntptime", shell=True)
    precision = re.search( r'precision (.* us).*stability (.* ppm)', output, re.M|re.S)
    theStr = "Precis: {:>8}\n".format(precision.group(1))
    theStr += "Stabi: {:>9}".format(precision.group(2))
    self.writeLCD(theStr)

  def clockperfView(self):
    """Shows jitter etc"""
    output = subprocess.check_output("ntptime", shell=True)
    search = re.search( r'TAI offset.*offset (.*? us).*jitter (.* us)', output, re.M|re.S)
    theStr = "Offset: {:>8}\n".format(search.group(1))
    theStr += "OSjitt: {:>8}".format(search.group(2))
    self.writeLCD(theStr)
    
  def updateLCD(self):
    """Called from main loop to update GPS info on LCD screen"""
    # Check status of GPS unit if it has a lock, otherwise change color of background on LCD to red.
    if time.time() - self.lastScreenTime > self.screens[self.currentScreen][1]: # Time to switch display
      self.currentScreen = self.currentScreen +1
      self.lastScreenTime = time.time()   # reset screen timer
      if self.currentScreen > self.nrofscreens - 1:
        self.currentScreen = 0
    self.screens[self.currentScreen][0]()
      
  def connectedUserView(self):
    """Shows connected clients to ntpd"""
    output = subprocess.check_output("ntpdc -n -c monlist | awk '{if(NR>2)print $1}' | wc -l", shell=True)  # Gets all the connected clients from ntp
    highestCount = subprocess.check_output("ntpdc -n -c monlist | awk '{if(NR>2)print $4}' | sort -nrk1,1 | line", shell=True)  # Gets the highest connections from connected clients
    theStr = "Con users: {:>6}".format(output)
    theStr += "Hi cons: {:>8}".format(highestCount)
    self.writeLCD(theStr)
    

if __name__ == '__main__':
  parser = optparse.OptionParser()
  parser.add_option('-l', '--logging-level', help='Logging level')
  parser.add_option('-f', '--logging-file', help='Logging file name')
  (options, args) = parser.parse_args()
  logging_level = LOGGING_LEVELS.get(options.logging_level, logging.NOTSET)
  logging.basicConfig(level=logging_level, filename=options.logging_file,
                      format='%(asctime)s %(levelname)s: %(message)s',
                      datefmt='%Y-%m-%d %H:%M:%S')

  # Initialize the LCD screen
  mylcd = lcdScreen(WHITE, "Atomic Clock\nNTP/GPS Server")
  sleep(2)
  
  while True:
    mylcd.updateLCD()
    time.sleep(0.20) #set to whatever

