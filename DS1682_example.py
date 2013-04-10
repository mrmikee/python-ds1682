#!/usr/bin/python

from DS1682 import DS1682

# ===========================================================================
# Example Code
# ===========================================================================

# Create an instance : Debug calls the print commands
ds = DS1682(0x6b, debug=True)

#read the ETC in 1/4 second intervals
raw = ds.readRawETC()

# convert to seconds
seconds = raw/4 
print "Hobbs Time: %.3f Hours" % ((seconds/3600.0))

# Read the Event Counter
e_count = ds.readRawEvent()
print "Events: %d" % (e_count)

# Reset the Elapsed Time Counter to zero
#ds.resetETC()

# Reset the Event Counter to zero
#ds.resetEvent()

