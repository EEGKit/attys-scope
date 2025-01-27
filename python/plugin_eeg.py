#!/usr/bin/python3
"""
Requires pyqtgraph.

Copyright (c) 2018-2022, Bernd Porr <mail@berndporr.me.uk>
see LICENSE file.

Plots the different EEG bands.
"""

CH1 = 7

# Bandstop frequency
fbs = 50 # Hz

import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets
import numpy as np
from scipy import signal
import iir_filter
from attys_scope_plugin_comm import AttysScopeReader

app = pg.mkQApp()

class QtPanningPlot:

    # duration of the scrolling window
    twin = 5
    # scale in V
    a = 100

    def __init__(self,title):
        self.fs = 250
        self.title = title
        self.channelCallback = False

        self.ylabel = ["EEG","gamma","beta","alpha","theta","delta"]
        self.n = len(self.ylabel)

        self.pw = [False]*self.n
        self.plt = [False]*self.n
        self.data = [[]]*self.n
        self.bpiir = [False]*self.n

        self.mw = QtWidgets.QMainWindow()
        self.mw.setWindowTitle('EEG')
        self.mw.resize(800,800)
        self.cw = QtWidgets.QWidget()
        self.mw.setCentralWidget(self.cw)
        self.l = QtWidgets.QVBoxLayout()
        self.cw.setLayout(self.l)
        
        for i in range(self.n):
            self.pw[i] = pg.PlotWidget()
            self.pw[i].setYRange(-self.a,self.a)
            self.pw[i].setLabel('bottom', 't/sec')
            self.pw[i].setLabel('left',self.ylabel[i]+'/uV')
            self.l.addWidget(self.pw[i])
            self.plt[i] = self.pw[i].plot()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)
        
        self.mw.show()

    def update(self):
        for i in range(self.n):
            self.data[i] = self.data[i][-int(self.twin*self.fs):]
            if self.data[i]:
                d = np.hstack(self.data[i])
                t = np.linspace(0,len(d)/self.fs,len(d))
                self.pw[i].setXRange(0,len(d)/self.fs)
                self.plt[i].setData(x=t,y=d)

    def addData(self,d):
        for i in range(self.n):
            self.data[i].append(self.bpiir[i].filter(d*1E6))

    def setFs(self,fs):
        self.fs = fs
        frange = [
            [0.1,100],
            [30,100],
            [13,30],
            [8,13],
            [4,8],
            [0.1,4]
        ]
        for i in range(self.n):
            bpsos = signal.butter(2, frange[i], output='sos', btype='bandpass', fs=fs)
            self.bpiir[i] = iir_filter.IIR_filter(bpsos)

##############################################################################
## main

bsiir = False
        
qtPanningPlot = QtPanningPlot("EEG bands")

# init the filters once we know the sampling rate
def callbackFs(fs):
    global bsiir
    hpfc = 0.5 # highpass freq
    bssos = signal.butter(2, [fbs-1,fbs+2], output='sos', btype='bandstop', fs=fs)
    bsiir = iir_filter.IIR_filter(bssos)
    qtPanningPlot.setFs(fs)

def callbackSetChannel(c):
    global channel
    channel = c

# process data with the filters set up
def callbackData(data):
    global CH1,bsiir
    v = bsiir.filter(data[CH1])
    qtPanningPlot.addData(v)

    
attysScopeReader = AttysScopeReader(callbackData,callbackFs)
attysScopeReader.start()

# showing all the windows
pg.exec()

attysScopeReader.stop()

print("Finished")
