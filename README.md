python-ds1682
=============

A Python class to read and reset the Maxim DS1682 Elapsed Time and Event Counter.
Based on data-sheet found: http://datasheets.maximintegrated.com/en/ds/DS1682.pdf

REQUIRES:
=========
  Adafruit's I2C library for the Raspberry Pi 
  https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code.git

NOTE:
=====
  The Write protect commands of this chip have not been implemented
  in this code, but should be easy enough to add for those that want/need it.

TODO:
=====
  Integer to byte array to set Elapsed Time Counter to value other than zero
  Integer to byte array to set Event Counter to value other than zero

AUTHOR:
=======
  Michael Cone
  https://github.com/mrmikee/python-ds1682.git
  
