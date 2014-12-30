#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PyQt4 tutorial 

"""

import sys
from PyQt4 import QtGui
import numpy as np
import scipy.io as sio
from pyqtgraph import *

class Example(QtGui.QMainWindow):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):

        self.current_signal_val=None

        exitAction = QtGui.QAction(QtGui.QIcon('delete85.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(QtGui.qApp.quit)
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)

        importAction = QtGui.QAction(QtGui.QIcon('download168.png'),'Import',self)
        importAction.setShortcut('Ctrl+I')
        importAction.triggered.connect(self.importconnect)
        self.toolbar.addAction(importAction)

        self.cw = QtGui.QWidget()

        self.plot1 = PlotWidget(name='Display')
        self.chCombo = QtGui.QComboBox()
        self.lbl = QtGui.QLabel("Channel")
        self.Data = QtGui.QComboBox()
        self.lbl2 = QtGui.QLabel("Data")

        self.hbox1 = QtGui.QHBoxLayout()
        self.hbox1.addWidget(self.plot1)
        self.hbox2 = QtGui.QHBoxLayout()
        self.hbox2.addWidget(self.lbl)
        self.hbox2.addWidget(self.chCombo)
        self.hbox2.addWidget(self.lbl2)
        self.hbox2.addWidget(self.Data)

        self.vbox1 = QtGui.QVBoxLayout()

        self.vbox1.addLayout(self.hbox1)
        self.vbox1.addLayout(self.hbox2)

        self.p1 = self.plot1.plot()
        self.p1.setData( np.random.random(90))

        self.cw.setLayout(self.vbox1)
        self.setCentralWidget(self.cw)
        self.setWindowTitle('JPredict')
        self.show()

    def importconnect(self):
        self.chCombo.clear()
        self.Data.clear()
        self.fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file','',"Mat files(*.mat)")
        print self.fname
        self.mat=sio.loadmat(str(self.fname))
        for record in self.mat.keys():
            if type(self.mat[record]) != type(''):
                self.Data.addItem(record)

        self.current_signal_val=self.mat[self.mat.keys()[0]][0]
        self.p1.setData(self.current_signal_val)
        i=0
        while i < self.mat[self.mat.keys()[0]].shape[0]:
            self.chCombo.addItem(str(i))
            i=i+1

    def dataclick(self):
        pass

    def channelclick(self):
        pass


def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()