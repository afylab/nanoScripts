'''
Example script for taking a voltage sweep at each point in a 2D space.
Gives the convention for the data vault file.

Modify as appropriate for a given measurement
'''

#Importing python packages
import numpy as np

#Defining parameters of experiment
top_gate = -3.756 # Held contant during scan, ramped to zero after measurement

# Fast axis is scanning the gate, at constant position
start_bottom_gate = 7.4 
end_bottom_gate = 8.5
num_points_fast_axis = 700 
fast_axis_time_delay = 10000 #in us

# DAC output channels for the gates
top_gate_out_channel = 0
bottom_gate_out_channel = 1

#Implementing rotation afterwards

# Center of the scan area, also center of rotation
center_x = 0e-6
center_y = 0e-6

# Coordinates defined relative to the center point, i.e. scan starts from
# x_start_actual = xstart + center_x
x_start = -5e-6  #Start x position of scan relative to center
x_end = 5e-6 #End x position of scan relative to center
y_start = -5e-6 #Start y position of scan relative to center
y_end = -5e-6 #End y position of scan relative to center

num_x_points = 100
num_y_points = 50

rot_angle = 0 * np.pi/180 # Rotation angle

x_points = np.linspace(x_start, x_end, num_x_points)
y_points = np.linspace(y_start,y_end , num_y_points)

# Perform the rotation
X,Y = np.meshgrid(x_points,y_points)
Xr = np.cos(rot_angle)*X + np.sin(rot_angle)*Y
Yr = -np.sin(rot_angle)*X + np.cos(rot_angle)*Y

Xnew = Xr + center_x
Ynew = Yr + center_y


bottom_gate_voltages = np.linspace(start_bottom_gate,end_bottom_gate,num_points_fast_axis)
bottom_gate_indices = list(range(num_points_fast_axis))

#Importing equipment
sample_dac = self.equip.get('Sample DAC')
dv = yield self.equip.get_datavault()

#Opening datavault file
dv.new('SQUID 1D gate sweep vs 2D position',['Trace_retrace','Bottom gate index','Bottom gate value','Top gate value','x index','y index','x coordinate', 'y coordinate'],['Current X','SQUID 1','Voltage X','SQUID 2'])
#Collecting all inputs in case you screw up which input is which, you can salvage the measurement

top_gate_start_ramp = yield sample_dac.buffer_ramp([top_gate_out_channel],[0,1,2,3],[0],[top_gate],1000,1000)
bottom_gate_start_ramp = yield sample_dac.buffer_ramp([bottom_gate_out_channel],[0,1,2,3],[0],[start_bottom_gate],1000,1000)

#Managing position
self.looptimer.start_loop_timer(num_x_points*num_y_points) 
for n in range(num_x_points):
    for m in range(num_y_points):
        yield ScanControl.setPosition(Xnew[m,n], Ynew[m,n])
        
        yield ScanControl.blink()
        
        #Gate Sweep
        data_trace = yield sample_dac.buffer_ramp([bottom_gate_out_channel],[0,1,2,3],[start_bottom_gate],[end_bottom_gate],num_points_fast_axis,fast_axis_time_delay)
        data_retrace = yield sample_dac.buffer_ramp([bottom_gate_out_channel],[0,1,2,3],[end_bottom_gate],[start_bottom_gate],      num_points_fast_axis,fast_axis_time_delay)
        
        data_retrace = np.asarray(data_retrace)
        data_retrace = np.flip(data_retrace,axis=1)
        
        for k in range(num_points_fast_axis):
            trace_data = [0,bottom_gate_indices[k],bottom_gate_voltages[k],top_gate,n,m,Xnew[m,n],Ynew[m,n],data_trace[0][k],data_trace[1][k],data_trace[2][k],data_trace[3][k]]
            retrace_data = [1,bottom_gate_indices[k],bottom_gate_voltages[k],top_gate,n,m,Xnew[m,n],Ynew[m,n],data_retrace[0][k],data_retrace[1][k],data_retrace[2][k],data_retrace[3][k]]
            dv.add(trace_data)
            dv.add(retrace_data)
        self.looptimer.next() # Tell the timer this iteration is done, will update the timing information on the interface.
        
top_gate_end_ramp = yield sample_dac.buffer_ramp([top_gate_out_channel],[0,1,2,3],[top_gate],[0],1000,1000)
bottom_gate_end_ramp = yield sample_dac.buffer_ramp([bottom_gate_out_channel],[0,1,2,3],[start_bottom_gate],[0],1000,1000)
