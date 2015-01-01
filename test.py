#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
Conativa

https://blog.dlasley.net/2013/01/generic-worker-thread-pyqt/

"""

import scipy.io as sio
from pyqtgraph import *
from PyQt4 import QtGui,QtCore
import mlpy.wavelet as wave


class Example(QtGui.QMainWindow):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):

        self.current_signal_val= 0
        self.current_data = ''
        self.current_channel = 0

        self.current_signal_array = np.array([0])

        self.toolbar = self.addToolBar('Tool')


        importAction = QtGui.QAction(QtGui.QIcon('download168.png'),'Import',self)
        importAction.setShortcut('Ctrl+I')
        importAction.triggered.connect(self.importconnect)
        self.toolbar.addAction(importAction)

        waveletAction = QtGui.QAction(QtGui.QIcon('wavelets.png'),'Wavelet',self)
        waveletAction.setShortcut('Ctrl+W')
        waveletAction.triggered.connect(self.WaveletClick)
        self.toolbar.addAction(waveletAction)


        exitAction = QtGui.QAction(QtGui.QIcon('delete85.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(QtGui.qApp.quit)
        self.toolbar.addAction(exitAction)



        self.cw = QtGui.QWidget()

        self.plot1 = PlotWidget(name='Display')
        self.plot1.setMaximumHeight(200)



        self.chCombo = QtGui.QComboBox()
        self.chCombo.activated[str].connect(self.channelclick)
        self.lbl = QtGui.QLabel("Channel")

        self.Data = QtGui.QComboBox()
        self.Data.activated[str].connect(self.dataclick)
        self.lbl2 = QtGui.QLabel("Data")

        self.hbox1 = QtGui.QHBoxLayout()
        self.hbox1.addWidget(self.plot1)
        self.hbox2 = QtGui.QHBoxLayout()
        self.hbox2.addStretch(1)
        self.hbox2.addWidget(self.lbl)
        self.hbox2.addWidget(self.chCombo)
        self.hbox2.addStretch(1)
        self.hbox2.addWidget(self.lbl2)
        self.hbox2.addWidget(self.Data)

        self.vbox1 = QtGui.QVBoxLayout()
        self.vbox1.addLayout(self.hbox1)
        self.vbox1.addLayout(self.hbox2)


        ##############################################################
        self.wavelettabwidget = QtGui.QTabWidget()
        self.wavelettab = QtGui.QWidget()
        self.waveletlayout = QtGui.QVBoxLayout()

        self.wavelettabwidget.addTab(self.wavelettab,"cwt")
        self.waveletplot = ImageView()
        self.waveletlayout.addWidget(self.waveletplot)
        self.waveletplot.show()
        self.wavelettab.setLayout(self.waveletlayout)
        self.vbox1.addWidget(self.wavelettabwidget)
        ############################################################


        self.p1 = self.plot1.plot()
        self.p1.setData( np.random.random(90))



        self.cw.setLayout(self.vbox1)
        self.setCentralWidget(self.cw)
        self.setWindowTitle('Conativa')
        self.show()

    def importconnect(self):
        self.chCombo.clear()
        self.Data.clear()
        self.fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file','',"Mat files(*.mat)")
        print self.fname
        self.mat=sio.loadmat(str(self.fname))
        for record in self.mat.keys():
            if type(self.mat[record]) != (type('')):
                self.Data.addItem(record)


        self.current_data = self.mat.keys()[0]
        self.current_signal_val=self.mat[self.current_data][0]

        self.p1.setData(self.current_signal_val)
        i=0
        while i < self.mat[self.mat.keys()[0]].shape[0]:
            self.chCombo.addItem(str(i))
            i=i+1


    def dataclick(self, index):
        self.current_data = str(index)
        self.current_channel = 0
        self.current_signal_val=self.mat[self.current_data][0]
        self.updateplot()

    def channelclick(self,index):
        self.current_channel = int(index)
        self.current_signal_val=self.mat[self.current_data][self.current_channel]
        self.updateplot()

    def updateplot(self):
        self.p1.setData(self.current_signal_val)

    def updateWaveletplot(self,data):
         print data
         self.waveletplot.setImage(data.T)


    def WaveletClick(self):

        self.waveletThread = WaveletThread(self.updateWaveletplot,self.current_signal_val)
        self.waveletThread.start()




class WaveletThread(QtCore.QThread):

    finished = QtCore.pyqtSignal(type(np.array([0])))
    def __init__(self,ret_function,*args):
        super(WaveletThread, self).__init__(parent = None)
        self.input = np.array(args)[0]
        print self.input.shape
        self.finished.connect(ret_function)


    def run(self):
        print "ok"
        scales = wave.autoscales( self.input.shape[0], 1,0.25,'dog',2)
        self.finished.emit(wave.cwt(self.input,1,scales,'dog',2) )






def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()