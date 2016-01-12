# Raspberry Pi NTP Server Clock and Statistics LCD Display
This is a simple Python program for displaying time and statistics on an [Adafruit CharPlate LCD for Raspberry Pi](https://www.adafruit.com/products/1110) on a Raspberry Pi NTP Server.

A lot o people (aka. Time-nuts) are using Raspberry Pi's for setting up an very accurate NTP server. You can use the Raspberry Pi GPIO pins and feed it a [PPS time pulse](https://en.wikipedia.org/wiki/Pulse-per-second_signal) and optimise the kernel so both the kernel and the NTP server uses the PPS signal to discipline it to an accurate (depending on the PPS source) NTP server. Sources for the signals are usually a [GPSDO](https://en.wikipedia.org/wiki/GPS_disciplined_oscillator) (or any GPS that outputs a PPS signal) or a Rubidium clock.

I wanted to have a display to see the accuracy, how many connected users and naturally the time, so this is the result. Future plans include changing the background color if something is out of spec. 
## Views
The clock displays several views. They rotate round according to a list with a time value for how long to display each view. It's easy to rearrange or remove views you don't need. 

#### Big Clock
![Big Clock LCD Display](https://github.com/jacken/Raspberry-Pi-ntp-server-LCD-display/blob/master/images/big-clock.jpg)
First and formost, if you have a server that is synced to atomic clocks, you want to see the time. The "Big Clock" code was written by [Adrian Allan](http://allan.me/2015/10/30/a-very-simple-raspberry-pi-clock-using-adafruit-16x2-lcd-pi-plate/) and adapted for my use.

#### Offset and OS Jitter
![Offset and OS Jitter LCD Screen](https://github.com/jacken/Raspberry-Pi-ntp-server-LCD-display/blob/master/images/offset.jpg)
This view shows the current NTP clock offset and the Operating System jitter.

#### Precision and Stability
![Precision and Stability LCD Display](https://github.com/jacken/Raspberry-Pi-ntp-server-LCD-display/blob/master/images/precision.jpg)
Here you can see the current clock precision in µs. It also shows the system stability in parts per million.

#### Connected users and the highest connection count by a user
As described above. It shows how many computers that is currently connected to your NTP server. The second line shows the highest number of connections from a single user.

More views and switching the RGB backlight color if out of spec are planned...


[^gpsdo]: GPS disciplined oscillator, usually a controlled oven heated crystal or a Rubidium oscillator slaved to the atomic clocks from the GPS satellites.