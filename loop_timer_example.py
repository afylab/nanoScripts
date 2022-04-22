#
# An example of how to use the loop timer which displays timing information for a script on the scripting window GUI
#

import numpy as np

N = 15

# Start the timer, tell it the number of loops so that it can tell you the % complete. 
# If you omit the argument it will still display timing information for each iteration.
# If you have multiple loops in a script, calling this again will reset it.
self.looptimer.start_loop_timer(N) 
for i in range(N):
    # Do stuff
    yield self.sleep(1+0.25*np.random.rand())
    
    # end of the loop
    self.looptimer.next() # Tell the timer this iteration is done, will update the timing information on the interface.
