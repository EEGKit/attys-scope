# -*- coding: utf-8 -*-
"""
@author: Bernd Porr, mail@berndporr.me.uk

"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading

# attys channel to be plotted from 
channel = 7

#That's our ringbuffer which accumluates the samples
#It's emptied every time when the plot window below
#does a repaint
ringbuffer = []

# for the thread below
doRun = True

# This reads the data from the socket in an endless loop
# and stores the data in a buffer
def readstdin():
    global ringbuffer
    global channel
    while doRun:
        try:
            # check if data is available
            data = sys.stdin.readline()
            values = np.array(data.split(','),dtype=np.float32)
            ringbuffer.append(values[channel])
        except:
            sys.exit()


# start reading data from socket
t = threading.Thread(target=readstdin)
t.start()

# now let's plot the data
fig, ax = plt.subplots()
# that's our plotbuffer
plotbuffer = np.zeros(500)
# plots an empty line
line, = ax.plot(plotbuffer)
# axis
ax.set_ylim(-2, 2)


# receives the data from the generator below
def update(data):
    global plotbuffer
    # add new data to the buffer
    plotbuffer=np.append(plotbuffer,data)
    # only keep the 500 newest ones and discard the old ones
    plotbuffer=plotbuffer[-500:]
    # set the new 500 points of channel 9
    line.set_ydata(plotbuffer)
    return line,

# this checks in an endless loop if there is data in the ringbuffer
# of there is data then emit it to the update funnction above
def data_gen():
    global ringbuffer
    #endless loop which gets data
    while True:
        # check if data is available
        if not ringbuffer == []:
            result = ringbuffer
            ringbuffer = []
            yield result

# start the animation
ani = animation.FuncAnimation(fig, update, data_gen, interval=100)

# show it
plt.show()

# stop the thread which reads the data
doRun = False
# wait for it to finish
t.join()

print("finished")
