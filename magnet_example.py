# Magnet Controller Examples
#
# Shows you how to use the magnet both with autopersist and without
#
# 

# Get a link to the magnet controller, with all the smart features
magnet = self.equip.get("Magnet Z")

# This is a reference to the interface, allows you to replicate pressing buttons on the GUI
# Note that the .Z is important for compatability with systems that have more than one axis
FieldControl.Z

#------------------------------------------------------------------------------------------
# OPTION 1 - Use the magnet with autopersist (recommended)
#
yield magnet.startSweeping() # Will automatically toggle the persistent switch and ramp to persistent field as needed. If autopersist is unchecked on GUI will do nothing.
###
###   YOUR PRE-EXISITNG CODE GOES HERE
###
yield magnet.doneSweeping() # Will automatically turn off the persistent switch and ramp the supply to zero, use when you are fully done with the magnet. If autopersist is unchecked on GUI will do nothing.
#------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------
# OPTION 2  - To turn off automatic features and set things manually.
# This is equivalent to unchecking autopersist on the main interface and handling persistent current yourself
#
if magnet.autopersist:
    FieldControl.Z.toggleAutoPersist(False) # Turns off autopersist in the GUI, but changes nothing about the magnet
if magnet.persist: # If the magnet is already persistent, ramp to the setting then turn on the heater
    magnet.setSetpoint(magnet.persist_B)
    # magnet.setRampRate(1) # You may want to set the ramp rate, otherwise will go at the last one used
    yield magnet.goToSetpoint()
    yield FieldControl.Z.togglePersist(False)
    

###
###   YOUR PRE-EXISITNG CODE GOES HERE
###

# Be sure to handel the state the magnet is in after you are done.

# If you want to persist the magnet and ramp down the supply manually
yield FieldControl.Z.togglePersist(True) # Makes the magnet persistent.
magnet.setSetpoint(0)
yield magnet.goToSetpoint()
#
# OR
#
# If you want to go back into autopersist mode and have it handle persisting the magnet
FieldControl.Z.toggleAutoPersist(True) # Turns off autopersist in the GUI, but changes nothing about the magnet
magnet.doneSweeping() # Will automatically turn off the persistent switch and ramp the supply to zero, use when you are fully done with the magnet.
# ------------------------------------------------------------------------------------------
