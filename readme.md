# Raspberry Pi NTP Server Clock and Statistics LCD Display
This is a simple Python program for displaying time and statistics on an [Adafruit CharPlate LCD for Raspberry Pi](https://www.adafruit.com/products/1110) on a Raspberry Pi NTP Server.

A lot o people (aka. Time-nuts) are using Raspberry Pi's for setting up an very accurate NTP server. You can use the Raspberry Pi GPIO pins and feed it a [PPS time pulse](https://en.wikipedia.org/wiki/Pulse-per-second_signal) and optimise the kernel so both the kernel and the NTP server uses the PPS signal to discipline it to an accurate (depending on the PPS source) NTP server. Sources for the signals are usually a GPSDO[^gpsdo] (or any GPS that outputs a PPS signal) or a Rubidium clock.

I wanted to have a display to see the accuracy, how many connected users and naturally the time, so this is the result. Future plans include changing the background color if something is out of spec. 
## Views

#### Big Clock
![Big Clock LCD Display](https://github.com/jacken/Raspberry-Pi-ntp-server-LCD-display/blob/master/images/big-clock.jpg)
First and formost, if you have a server that is synced to atomic clocks, you want to see the time. The "Big Clock" code was written by [Adrian Allan](http://allan.me/2015/10/30/a-very-simple-raspberry-pi-clock-using-adafruit-16x2-lcd-pi-plate/)

[^gpsdo]: GPS disciplined oscillator, usually a controlled oven heated crystal or a Rubidium oscillator slaved to the atomic clocks from the GPS satellites.