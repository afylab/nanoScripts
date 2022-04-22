'''
Example script for taking a two dimensional voltage sweep.
Gives the convention for the data vault file.

Modify as appropriate for a given measurement
'''
#Importing python packages
import numpy as np

#Defining parameters of experiment
start_top_gate = -3.6
end_top_gate = -3.9
start_bottom_gate = 0
end_bottom_gate = 9
num_points_slow_axis =100
num_points_fast_axis = 8000

top_gate_out_channel = 0
bottom_gate_out_channel = 1

bottom_gate_voltages = np.linspace(start_bottom_gate,end_bottom_gate,num_points_fast_axis)
top_gate_voltages = np.linspace(start_top_gate,end_top_gate,num_points_slow_axis)
fast_axis_time_delay = 10000 #in us

#Importing equipment
sample_dac = self.equip.get('Sample DAC')
dv = yield self.equip.get_datavault()

#Opening datavault file
dv.new('2D SQUID gate sweep',['Trace_retrace','Bottom gate index','Top gate index','Bottom gate value','Top gate value'],['SQUID 1','Current X','SQUID 2','SQUID 3'])

#Ramp the top gate, bottom gate, and current set to their initial values, starting from zero
top_gate_start_ramp = yield sample_dac.buffer_ramp([top_gate_out_channel],[0,1,2,3],[0],[top_gate],1000,1000)
bottom_gate_start_ramp = yield sample_dac.buffer_ramp([bottom_gate_out_channel],[0,1,2,3],[0],[start_bottom_gate],1000,1000)

top_gate_index = 0
bottom_gate_indices = list(range(num_points_fast_axis))

self.looptimer.start_loop_timer(len(top_gate_voltages) - 1) 
for i in range(len(top_gate_voltages) - 1):
	yield ScanControl.blink()
	data_trace = yield sample_dac.buffer_ramp([bottom_gate_out_channel],[0,1,2,3],[start_bottom_gate],[end_bottom_gate],num_points_fast_axis,fast_axis_time_delay)
	data_retrace = yield sample_dac.buffer_ramp([bottom_gate_out_channel],[0,1,2,3],[end_bottom_gate],[start_bottom_gate],num_points_fast_axis,fast_axis_time_delay)
	next_slow_axis_value = yield sample_dac.buffer_ramp([top_gate_out_channel],[0,1,2,3],[top_gate_voltages[i]],[top_gate_voltages[i+1]],500,1000)
	
	data_retrace = np.asarray(data_retrace)
	data_retrace = np.flip(data_retrace,axis=1)
	
	for k in range(num_points_fast_axis):
		trace_data = [0,bottom_gate_indices[k],top_gate_index,bottom_gate_voltages[k],top_gate_voltages[i],data_trace[0][k],data_trace[1][k],data_trace[2][k],data_trace[3][k]]
		retrace_data = [1,bottom_gate_indices[k],top_gate_index,bottom_gate_voltages[k],top_gate_voltages[i],data_retrace[0][k],data_retrace[1][k],data_retrace[2][k],data_retrace[3][k]]
		dv.add(trace_data)
		dv.add(retrace_data)
	top_gate_index += 1
	self.looptimer.next() # Tell the timer this iteration is done, will update the timing information on the interface.


data_trace = yield sample_dac.buffer_ramp([bottom_gate_out_channel],[0,1,2,3],[start_bottom_gate],[end_bottom_gate],num_points_fast_axis,fast_axis_time_delay)
data_retrace = yield sample_dac.buffer_ramp([bottom_gate_out_channel],[0,1,2,3],[end_bottom_gate],[start_bottom_gate],num_points_fast_axis,fast_axis_time_delay)

data_retrace = np.asarray(data_retrace)
data_retrace = np.flip(data_retrace,axis=1)

for k in range(num_points_fast_axis):
	trace_data = [0,bottom_gate_indices[k],top_gate_index,bottom_gate_voltages[k],top_gate_voltages[i],data_trace[0][k],data_trace[1][k],data_trace[2][k],data_trace[3][k]]
	retrace_data = [1,bottom_gate_indices[k],top_gate_index,bottom_gate_voltages[k],top_gate_voltages[i],data_retrace[0][k],data_retrace[1][k],data_retrace[2][k],data_retrace[3][k]]
	dv.add(trace_data)
	dv.add(retrace_data)

restore_top_gate = yield sample_dac.buffer_ramp([top_gate_out_channel],[0,1,2,3],[end_top_gate],[start_top_gate],1000,1000)
