'''
A script to measure the transfer function near the working point of the nSOT.
Works by sweeping the field between two points and measuring the feedback values
then calculates the Feedback voltage per tesla.
'''
start_field = 0.032 #in Tesla
end_field = 0.033 #in Tesla

dac_chnl = 2 #DAC Channel reading the feedback voltage on the nSOT char DAC

meas_time = 10 #Time to average per point in seconds

#----------------------------------------------------------------------------#
import time
import numpy as np

magnet = self.equip.get("Magnet Z")
dac = self.equip.get('nSOT DAC')

# If the magnet is auto-persisted, ramp up the supply to the setpoint
yield magnet.startSweeping()

yield magnet.setSetpoint(start_field) 
yield magnet.goToSetpoint(wait=True)

startfield_volts = []
tzero = time.process_time()
t = tzero

while t-tzero <= meas_time:
    volts = yield dac.read_voltage(dac_chnl)
    startfield_volts.append(volts)
    t = time.process_time()
    
yield magnet.setSetpoint(end_field) 
yield magnet.goToSetpoint()

endfield_volts = []
tzero = time.process_time()
t = tzero

while t-tzero <= meas_time:
    volts = yield dac.read_voltage(dac_chnl)
    endfield_volts.append(volts)
    t = time.process_time()

v1 = np.average(startfield_volts)
v2 = np.average(endfield_volts)

yield magnet.setSetpoint(start_field) 
yield magnet.goToSetpoint(wait=True)

print('Slope in volts per tesla is: ' + str((v2-v1)/(end_field - start_field)))

# If the magnet is auto-persisted, ramp down the supply to the setpoint
yield magnet.doneSweeping()
