# You can activate either loop (TempControl.loop1 or TempControl.loop2) from the
# scripting module as shown below.
# Control settings for the loops, such as PID values or which thermometer to feedback on
# should be set in the software GUI or front panel

yield TempControl.loop1.setSetpoint(1.5)
yield TempControl.loop1.setRange("Low")
yield TempControl.loop1.heaterOn()

# Do experiment
yield self.sleep(10)

yield TempControl.loop1.heaterOff()