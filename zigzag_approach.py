'''
Script to measure the amount of creep by repeated touchdowns.
'''
import numpy as np
import time

#Position, in X and Y, -20 zeros the X and Y outputs for normal operation.
pos_x = -20e-6
pos_y = -20e-6

# The final height you want to get to.
final_height = 300e-9

sequence = [5e-6, 1e-6, 0.75e-6, 0.5e-6] # The sequence of steps to approach
time_sequence = [30, 60, 60, 100] # How long to wait for each step, in minutes

# The time interval to wait between touchdowns in minutes, after done approaching
time_interval = 60

# The Zig-Zag parameters, Zig must be larger than Zag
zig = 0.5e-6
zag = 0.4e-6

if len(time_sequence) != len(sequence):
    raise ValueError("time sequence must match approach sequence.")

# Datavault Setup
dv = yield self.equip.get_datavault()
yield dv.new("Creep Measurement",["time (s)"], ["Contact Height (um)", "Withdraw Distance (um)"])
dset = yield dv.current_identifier()
print("Saving To:", dset)

t0 = time.time()

@inlineCallbacks
def touchdown(widthdraw_dist, last_contact, last_time):
    yield Approach.setHeight(widthdraw_dist)
    yield self.sleep(30)
    yield Approach.setPLLThreshold()
    yield Approach.startZigZagApproach(zig, zag)
    contact_height = Approach.contactHeight
    now = time.time() - t0
    dv.add((now, contact_height, widthdraw_dist))
    print("Touchdown", round(now/3600), contact_height, widthdraw_dist)
    if last_contact != 0:
        creep = (contact_height - last_contact)*1e9
        rate = creep/((now-last_time)/3600)
        print("Crept", round(creep,1), "nm", round(rate,1), "nm/hour")
    returnValue((contact_height, now))

# Start fully widthdrawn, change value if you want to start somewhere else
yield Approach.withdraw(20e-6)
yield ScanControl.setPosition(pos_x, pos_y)
yield self.sleep(60)

last_contact = 0
last_time = 0

for i in range(len(sequence)):
    last_contact, last_time = yield touchdown(sequence[i], last_contact, last_time)
    for j in range(time_sequence[i]): # Do repeated sleeps to make it easier to abort the script
        yield self.sleep(60)

print("Done Approaching. Going to final height and measuring creep.")
for i in range(12):
    last_contact, last_time = yield touchdown(final_height, last_contact, last_time)
    for j in range(time_interval): # Do repeated sleeps to make it easier to abort the script
        yield self.sleep(60)
