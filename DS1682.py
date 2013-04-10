#!/usr/bin/python
"""
DS1682
  A Python class to read and reset the Maxim DS1682 Elapsed Time and Event Counter.
  Based on data-sheet found: http://datasheets.maximintegrated.com/en/ds/DS1682.pdf

REQUIRES:
  Adafruit's I2C library for the Raspberry Pi 
  https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code.git

NOTE: 
  The Write protect commands of this chip have not been implemented
  in this code, but should be easy enough to add for those that want/need it.

TODO:
  Integer to byte array to set Elapsed Time Counter to value other than zero
  Integer to byte array to set Event Counter to value other than zero

AUTHOR:
  Michael Cone
  https://github.com/mrmikee/python-ds1682.git
"""
 
import time
from datetime import datetime, timedelta

from Adafruit_I2C import Adafruit_I2C

# ===========================================================================
# DS1682 Class
# ===========================================================================

class DS1682 :
  i2c = None

  # DS1682 Registers
  __DS1682_CONF_REGISTER           = 0x00  #  Configuration Register
  __DS1682_ALARM_REG_LOW           = 0x01  #  Alarm Register Low Byte
  __DS1682_ALARM_REG_LOW_MID       = 0x02  #  Alarm Register Low Middle Byte
  __DS1682_ALARM_REG_HIGH_MID      = 0x03  #  Alarm Register High Middle Byte
  __DS1682_ALARM_REG_HIGH          = 0x04  #  Alarm Register High Byte
  __DS1682_ETC_LOW                 = 0x05  #  Elapsed Time Counter Low Byte
  __DS1682_ETC_LOW_MID             = 0x06  #  Elapsed Time Counter Low Middle Byte
  __DS1682_ETC_HIGH_MID            = 0x07  #  Elapsed Time Counter High Middle Byte
  __DS1682_ETC_HIGH                = 0x08  #  Elapsed Time Counter High Byte
  __DS1682_EVENT_LOW               = 0x09  #  Event Counter Low Byte
  __DS1682_EVENT_HIGH              = 0x0A  #  Event Counter High Byte
  __DS1682_USER_MEM_1              = 0x0B  #  User Memory Byte 1
  __DS1682_USER_MEM_2              = 0x0C  #  User Memory Byte 2
  __DS1682_USER_MEM_3              = 0x0D  #  User Memory Byte 3
  __DS1682_USER_MEM_4              = 0x0E  #  User Memory Byte 4
  __DS1682_USER_MEM_5              = 0x0F  #  User Memory Byte 5
  __DS1682_USER_MEM_6              = 0x10  #  User Memory Byte 6
  __DS1682_USER_MEM_7              = 0x11  #  User Memory Byte 7
  __DS1682_USER_MEM_8              = 0x12  #  User Memory Byte 8
  __DS1682_USER_MEM_9              = 0x13  #  User Memory Byte 9
  __DS1682_USER_MEM_10             = 0x14  #  User Memory Byte 10
                                   # 0x15-0x1C NOT USED
  __DS1682_RESET_CMD               = 0x1D  #  Reset Command
  __DS1682_WRITE_DISABLE           = 0x1E  #  Write Disable Command
  __DS1682_WRITE_MEM_DISABLE       = 0x1F  #  Write Memory Disable Command

  # Private Fields
  _etc_low      = 0
  _etc_low_mid  = 0
  _etc_high_mid = 0
  _etc_high     = 0
  _event_low    = 0
  _event_high   = 0
  
  # Constructor
  def __init__(self, address=0x6b, debug=False):
    self.i2c = Adafruit_I2C(address)
    self.address = address
    self.debug = debug

  def readRawETC(self):
    "Reads the ETC data from the IC"
    self._etc_low = self.i2c.readU8(self.__DS1682_ETC_LOW)
    self._etc_low_mid = self.i2c.readU8(self.__DS1682_ETC_LOW_MID)
    self._etc_high_mid = self.i2c.readU8(self.__DS1682_ETC_HIGH_MID)
    self._etc_high = self.i2c.readU8(self.__DS1682_ETC_HIGH)
    if (self.debug):
      self.showETCData()
    return (self._etc_high << 24) + (self._etc_high_mid << 16) + (self._etc_low_mid << 8) + self._etc_low

  def showETCData(self):
    "Displays the ETC values for debugging purposes"
    print "DBG: ETC_LOW = %6d" % (self._etc_low)
    print "DBG: ETC_LOW_MID = %6d" % (self._etc_low_mid)
    print "DBG: ETC_HIGH_MID = %6d" % (self._etc_high_mid)
    print "DBG: ETC_HIGH = %6d" % (self._etc_high)
    test = (self._etc_high << 24) + (self._etc_high_mid << 16) + (self._etc_low_mid << 8) + self._etc_low
    tmp = (test/4)
    print "DBG: TEST = 1/4seconds=%8d  (seconds=%8d)" % (test, tmp)
    sec = timedelta(seconds=tmp)
    d = datetime(1,1,1) + sec
    print("Time NOW = %s" % ( datetime.now() ) )
    print("YEAR:MONTH:DAYS:HOURS:MIN:SEC")
    print("%d:%d:%d:%d:%d:%d" % (d.year-1, d.month-1, d.day-1, d.hour, d.minute, d.second))
      
  def resetETC(self, H=0, HM=0, LM=0, L=0):
    "reset ETC values to Zero"
    self.i2c.write8(self.__DS1682_ETC_HIGH, H)
    time.sleep(0.009)  # Wait
    self.i2c.write8(self.__DS1682_ETC_HIGH_MID, HM)
    time.sleep(0.009)  # Wait
    self.i2c.write8(self.__DS1682_ETC_LOW, L)
    time.sleep(0.009)  # Wait
    self.i2c.write8(self.__DS1682_ETC_LOW_MID, LM)
    time.sleep(0.009)  # Wait
    self.i2c.write8(self.__DS1682_ETC_LOW, L)
    time.sleep(0.009)  # Wait

  def readRawEvent(self):
    "read the Event Counter Raw Value"
    self._event_low = self.i2c.readU8(self.__DS1682_EVENT_LOW)
    self._event_high = self.i2c.readU8(self.__DS1682_EVENT_HIGH)
    if (self.debug):
      self.showEvent()
    return (self._event_high << 8) + (self._event_low)
    
  def showEvent(self):
    "show the Event Register Values if debug"
    print "DBG: EVENT_LOW = %6d" % (self._event_low)
    print "DBG: EVENT_HIGH = %6d" % (self._event_high)
    test = (self._event_high << 8) + (self._event_low) 
    print "DBG: Event Test = %d" % (test)
    
  def resetEvent(self, H=0, L=0):
    "reset the Event Registers"
    self.i2c.write8(self.__DS1682_EVENT_HIGH, H)
    time.sleep(0.009)  # Wait
    self.i2c.write8(self.__DS1682_EVENT_LOW, L)
    time.sleep(0.009)  # Wait

