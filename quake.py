# P-Wave Earthquake detector
# Copyright 2011, Casey Halverson
# see README for license

import time
import sys
import serial
import os

log = "/var/log/quake.txt"                    # location for log file
serial_port = "/dev/tty.usbserial-A600aiqR"   # name of serial port (do an ls /dev/*usbserial* to find yours)
notify_script = "/Users/quake/script.sh &"    # some system os command to run if we get a quake, make it & to prevent blocking
tweet_script = "/Users/quake/tweet.sh &"      # an additional script that is ran on a quake, make it & to prevent blocking

f = open(log,"a")

ser = serial.Serial(serial_port,9600)

one = 0

while 1==1:
  bit = ser.read(1)                           # read one bit (0 or 1 ascii)  Arduino spits out a 0 on connection, although, we will get a single 0 every x million reads
  one = one + 1                               # increment our keep alive counter
  if one == 500000000:                        # print a keep alive every 7 days or so
     at = str(time.asctime())                 # grab human time
     t = str(time.time())                     # grab epoc
     print "["+at+"."+t+"] Keep alive"        # print keepalive
     f.write("["+at+"."+t+"] Keep alive\n")   # write keepalive to file
     one = 0                                  # reset our keepalive counter
  if bit == "0":                              # did we actually get a 0?
     at = str(time.asctime())                 # grab human time
     t = str(time.time())                     # grab epoc
     print "["+at+"."+t+"] Possible motion, reading another bit to verify"      # every x million reads, you will actually get a 0 for no reason. filter out this bug
     noquake = 1                              # this can be removed, no reason to keep it
     ccount = 1                               # reset our ccount value so we can check a swath of reads
     while 1==1:                              # additional 0 bit detection
         ccount = ccount + 1                  # increment our counter
         bit = ser.read(1)                    # get more data fromt he arduino
         if ccount > 2000:  break             # if after 2000 reads we didn't see any more, go back to normal
         if bit == "0":  break                # if we see an additional 0, something is happening
     if bit == "0":                           # OMGWTF!? EARTHQUAKE loop
      print "["+at+"."+t+"] Earthquake! telling the interweb! capturing signature! hope the power doesn't go out!"            # we are faster than the earthquake, so it'll probably not happen
      f.write("["+at+"."+t+"] Earthquake! telling the interweb! capturing signature! hope the power doesn't go out!\n[")      # write this to the log
      os.system(notify_script)                             # run notify script
      os.system(tweet_script)                              # run a twitter script
      timeout = int(time.time()) + 120                     # setup a quake timeout to 120 seconds
      buffer = ""                                          # clear the quake bitmap buffer
      at = str(time.asctime())                             # grab human time
      t = str(time.time())                                 # grab epoc
      while 1==1:                                          # start our quake bitmap routine
        bit = ser.read(1)                                  # grab a bit
        if bit != "":                                      # if we get a 0 or a 1...
           buffer = buffer + str(bit)                      # start making a buffer
           if len(buffer) > 256:                           # if we have 256 bytes in our buffer..
              f.write("["+str(t)+"]: ")                    # write a timestamp to file
              f.write(str(buffer)+"\n")                    # dump quake bitmap to file
              print str(t)+" "+buffer                      # duplicate above in console
              buffer = ""                                  # clear the buffer
              at = str(time.asctime())                     # grab human time for the next cycle
              t = str(time.time())                         # grab epoc for next cycle
        if bit == "0":                                     # if we got a 0 above, bump the expire time another 2 minutes
           timeout = int(time.time()) + 120                # if we got a 0 above, bump the expire time another 2 minutes
        if bit == "1":                                     # if we got a 1 (no movement from sensor) 
           if int(time.time()) > timeout:                  # if we are past 2 minutes
              at = str(time.asctime())                     # grab epoc
              t = str(time.time())                         # grab human time
              print "["+at+"."+t+"]  2 minute timeout from shaking, going back"                 # say we are done with the quake on the console
              f.write("]\n["+at+"."+t+"]  2 minute timeout from shaking, going back\n")         # write the same to the file
              break                                                                             # break us out of this crazy thing
  
