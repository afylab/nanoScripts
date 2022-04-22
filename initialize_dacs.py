'''
Initilize all the DAC-ADCs currently connected
'''
dac = self.equip.cxn.dac_adc
dev = yield dac.list_devices()

for k in dev:
	yield dac.select_device(k[0])
	yield dac.initialize()