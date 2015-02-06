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
import interpol3
import bsft4


class Example(QtGui.QMainWindow):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):

        self.current_signal_val= np.random.random(400)
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
        
        EMDAction = QtGui.QAction(QtGui.QIcon('EMD.png'),'EMD',self)
        EMDAction.setShortcut('Ctrl+E')
        EMDAction.triggered.connect(self.EMDClick)
        self.toolbar.addAction(EMDAction)
        
        FBAction = QtGui.QAction(QtGui.QIcon('FB.png'),'FB',self)
        FBAction.setShortcut('Ctrl+E')
        FBAction.triggered.connect(self.FBClick)
        self.toolbar.addAction(FBAction)


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
        # Wavelet GUI

        self.wavelettabwidget = QtGui.QTabWidget()
        self.wavelettab = QtGui.QWidget()
        self.waveletlayout = QtGui.QVBoxLayout()

        self.wavelettabwidget.addTab(self.wavelettab,"CWT")
        self.waveletplot = ImageView()
        self.waveletlayout.addWidget(self.waveletplot)
        self.waveletplot.show()
        self.wavelettab.setLayout(self.waveletlayout)
        self.vbox1.addWidget(self.wavelettabwidget)
        ############################################################

        #################################################################
        #EMD GUI

        self.emdtab = QtGui.QWidget()
        self.emdlayout = QtGui.QVBoxLayout()
        self.wavelettabwidget.addTab(self.emdtab,"EMD")
        self.p1 = PlotWidget(name='IMF1')
        self.p1.setLabel('left','IMF1')
        self.emdlayout.addWidget(self.p1)

        self.p2 = PlotWidget(name='IMF2')
        self.p2.setLabel('left','IMF2')
        self.emdlayout.addWidget(self.p2)

        self.p3 = PlotWidget(name='IMF3')
        self.p3.setLabel('left','IMF3')
        self.emdlayout.addWidget(self.p3)

        self.p4 = PlotWidget(name='IMF4')
        self.p4.setLabel('left','IMF4')
        self.emdlayout.addWidget(self.p4)

        self.p5 = PlotWidget(name='IMF5')
        self.p5.setLabel('left','IMF5')
        self.emdlayout.addWidget(self.p5)

        self.p_res = PlotWidget(name='IMF_res')
        self.p_res.setLabel('left','IMF_res')
        self.emdlayout.addWidget(self.p_res)

        self.emdtab.setLayout(self.emdlayout)
        #################################################################
        
        #################################################################
        # Fourier-Bessel 
        
        self.FBtab = QtGui.QWidget()
        self.FBlayout = QtGui.QVBoxLayout()
        self.wavelettabwidget.addTab(self.FBtab,"FB")
        self.f1 = PlotWidget(name='delta')
        self.f1.setLabel('left','delta')
        self.FBlayout.addWidget(self.f1)

        self.f2 = PlotWidget(name='theta')
        self.f2.setLabel('left','theta')
        self.FBlayout.addWidget(self.f2)

        self.f3 = PlotWidget(name='alpha')
        self.f3.setLabel('left','alpha')
        self.FBlayout.addWidget(self.f3)

        self.f4 = PlotWidget(name='beta')
        self.f4.setLabel('left','beta')
        self.FBlayout.addWidget(self.f4)

        self.f5 = PlotWidget(name='gamma')
        self.f5.setLabel('left','gamma')
        self.FBlayout.addWidget(self.f5)

        self.FBtab.setLayout(self.FBlayout)
        #################################################################


        self.p0 = self.plot1.plot()
        self.p0.setData( self.current_signal_val)

        self.cw.setLayout(self.vbox1)
        self.setCentralWidget(self.cw)
        self.setWindowTitle('Conativa')
        self.show()

    def importconnect(self):
        self.chCombo.clear()
        self.Data.clear()
        self.fname = QtGui.QFileDialog.getOpenFileName( self, 'Open file','',"Mat files(*.mat)")
        #print self.fname
        self.mat=sio.loadmat(str(self.fname))
        for record in self.mat.keys():
            if type(self.mat[record]) != (type('')):
                self.Data.addItem(record)


        self.current_data = self.mat.keys()[0]
        self.current_signal_val=self.mat[self.current_data][0]

        self.p0.setData(self.current_signal_val)
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
        self.p0.setData(self.current_signal_val)

    def updateWaveletplot(self,data):

         self.waveletplot.setImage(data.T)

    def updateEMDplot(self,data):

         self.p1.plotItem.clear()
         self.p2.plotItem.clear()
         self.p3.plotItem.clear()
         self.p4.plotItem.clear()
         self.p5.plotItem.clear()
         self.p_res.plotItem.clear()

         self.p1.plotItem.plot(data[1])
         self.p2.plotItem.plot(data[2])
         self.p3.plotItem.plot(data[3])
         self.p4.plotItem.plot(data[4])
         self.p5.plotItem.plot(data[5])
         self.p_res.plotItem.plot(data[6])
        
    def updatefbplot(self,data):

         self.f1.plotItem.clear()
         self.f2.plotItem.clear()
         self.f3.plotItem.clear()
         self.f4.plotItem.clear()
         self.f5.plotItem.clear()

         self.f1.plotItem.plot(data[0])
         self.f2.plotItem.plot(data[1])
         self.f3.plotItem.plot(data[2])
         self.f4.plotItem.plot(data[3])
         self.f5.plotItem.plot(data[4])

    def WaveletClick(self):

        self.waveletThread = WaveletThread(self.updateWaveletplot,self.current_signal_val)
        self.waveletThread.start()

    def EMDClick(self):

        self.emdthread = EMDthread(self.updateEMDplot  ,  self.current_signal_val)
       # print self.current_signal_val
        self.emdthread.start()
        
    def FBClick(self):

        self.fbthread = FBthread(self.updatefbplot  ,  self.current_signal_val)
        #print self.current_signal_val
        self.fbthread.start()




class WaveletThread(QtCore.QThread):

    finished = QtCore.pyqtSignal(type(np.array([0])))
    def __init__(self,ret_function,*args):
        super(WaveletThread, self).__init__(parent = None)
        self.input = np.array(args)[0]
       # print self.input.shape
        self.finished.connect(ret_function)


    def run(self):
        scales = wave.autoscales( self.input.shape[0], 1,0.25,'dog',2)
        self.finished.emit(wave.cwt(self.input,1,scales,'dog',2) )


class EMDthread(QtCore.QThread):
    finished = QtCore.pyqtSignal(type(np.array([0])))
    def __init__(self,ret_function,*args):
        super( EMDthread ,self).__init__()
        self.input = np.array(args)[0]
        print self.input.shape
        self.finished.connect(ret_function)

    def run(self):
        self.finished.emit(interpol3.emd(self.input,6))

class FBthread(QtCore.QThread):
    finished = QtCore.pyqtSignal(type(np.array([0])))
    def __init__(self,ret_function,*args):
        super( FBthread ,self).__init__()
        self.input = np.array(args)[0]
        print self.input.shape
        self.finished.connect(ret_function)

    def run(self):
        self.finished.emit(bsft4.fbdecomp(self.input))





def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()