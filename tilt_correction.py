'''
Script to determine tilt correction for a sample. Requires specifying a starting point and how far to move in x and y. 
It will auto load the tilt correction into the ScanControl window. 
Assumes that the approach window is set up properly for a PID frequency feedback approach to the surface. 
Returns to the specified starting position after it's done
'''

#Start position. At 4K, -20e-6 is the bottom left corner corresponding to 0 volts in x and y
start_x = -20e-6
start_y = -20e-6

#Movement in x, and y from which the tilt will be determined in meters
delta_x = 40e-6
delta_y = 40e-6

#Script starts below
#-----------------------------------------------------------------------------#

@inlineCallbacks
def approachAtPosition(x,y):
    yield Approach.withdraw(20e-6)
    yield ScanControl.setPosition(x, y)
    #Once in position, approach
    yield self.sleep(30)
    yield Approach.setPLLThreshold()
    yield Approach.startPIDConstantHeightApproachSequence()
    returnValue(Approach.contactHeight)

contact_height = yield approachAtPosition(start_x, start_y)
contact_height_plusx = yield approachAtPosition(start_x + delta_x, start_y)
contact_height_plusy = yield approachAtPosition(start_x, start_y + delta_y)

yield Approach.withdraw(20e-6)

#Return to the original position
yield ScanControl.setPosition(start_x, start_y)

import numpy as np

tilt_x = np.arctan((contact_height - contact_height_plusx)/ delta_x)* 180.0 / np.pi
tilt_y = np.arctan((contact_height - contact_height_plusy)/ delta_y)* 180.0 / np.pi

ScanControl.lineEdit_XTilt.setText(formatNum(tilt_x))
ScanControl.updateXTilt()
ScanControl.lineEdit_YTilt.setText(formatNum(tilt_y))
ScanControl.updateYTilt()