import sys, os, gc
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
from matplotlib.figure import Figure
import wx
import numpy as np
import matplotlib.pyplot as mp
import math as m
import scipy.io as sc
import scipy.stats as st
from time import *
from xlwt import Workbook
from xlwt.Style import *
from array import *
from PIL import Image



currentmatfile = 0




class Eeg_Gui(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, id, title,(-1,-1),wx.Size(600,600))

		self.current_signal_val=None
		self.current_plot1_txt = None
		self.current_daub_value= None
		self.current_record_value = None
		self.current_channel_value = 0
		self.current_mean_value = 0
		self.current_median_value = 0
		self.current_mode_value = 0
		self.current_kurtosis_value = 0
		self.current_skew_value = 0
		self.current_variance_value = 0


		menubar= wx.MenuBar()
		self.panel = wx.Panel(self)
		self.combo = wx.ComboBox(self.panel, 4, '',(400,500),choices="",name="record")
		self.combo2 = wx.ComboBox(self.panel, 4, '',(100,500),choices="",name="Channel")
		self.combo.Bind(wx.EVT_COMBOBOX, self.OnSelectRecord)
		self.combo2.Bind(wx.EVT_COMBOBOX, self.OnSelectChannel)
		self.st1 = wx.StaticText(self.panel, label="record",pos=(350,505))
		self.st2 = wx.StaticText(self.panel, label="Channel",pos=(40,505))
		self.st0 = wx.StaticText(self.panel, label="DAUBECHIES WAVECOFF ANALYSIS:",pos=(690,50))


		self.st3 = wx.StaticText(self.panel, label="mean:",pos=(700,100))
		self.st4 = wx.StaticText(self.panel, label="mode:",pos=(700,150))
		self.st5 = wx.StaticText(self.panel, label="median:",pos=(700,200))
		self.st6 = wx.StaticText(self.panel, label="kurtosis:",pos=(700,250))
		self.st7 = wx.StaticText(self.panel, label="skew:",pos=(700,300))
		self.st8 = wx.StaticText(self.panel, label="variance:",pos=(700,350))

		self.init_plot()
		file = wx.Menu()

		load = wx.MenuItem(file,1,'&load')
		file.AppendItem(load)
		self.Bind(wx.EVT_MENU , self.loadmatfile , id = 1)


		quit = wx.MenuItem(file,2,'&Quit')
		file.AppendItem(quit)
		self.Bind(wx.EVT_MENU , self.OnQuit , id = 2)

		menubar.Append(file , '&File')


		tools = wx.Menu()

		daub = wx.MenuItem(tools,3,'&daub')
		tools.AppendItem(daub)
		self.Bind(wx.EVT_MENU , self.daubtran , id = 3)

		export2xl = wx.MenuItem(tools,5,'&export2xls')
		tools.AppendItem(export2xl)
		self.Bind(wx.EVT_MENU , self.SaveData , id = 5)

		menubar.Append(tools , '&Tools')

		helper = wx.Menu()

		helpmenu = wx.MenuItem(helper,4,'&About')
		helper.AppendItem(helpmenu)
		self.Bind(wx.EVT_MENU , self.OnHelp , id = 4)

		menubar.Append(helper , '&help')

		self.SetMenuBar(menubar)


		self.SetMinSize((950, 600))
		self.SetMaxSize((950, 600))



	def OnHelp(self, e):

		description = """EEGAnalyser is an simple electro encephalogram
		analyser for chbmit data. Its features include plotting of invidual 
		channels within records and their corresponding daubechies plots.
		"""

		licence = """EEGAnalyser is free software; you can redistribute 
		it and/or modify it under the terms of the GNU General Public License as 
		published by the Free Software Foundation; either version 2 of the License, 
		or (at your option) any later version.
		
		EEGAnalyser is distributed in the hope that it will be useful, 
		but WITHOUT ANY WARRANTY; without even the implied warranty of 
		MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
		See the GNU General Public License for more details. You should have 
		received a copy of the GNU General Public License along with File Hunter; 
		if not, write to the Free Software Foundation, Inc., 59 Temple Place, 
		Suite 330, Boston, MA  02111-1307  USA"""


		info = wx.AboutDialogInfo()


		info.SetName('EEGAnalyser')
		info.SetVersion('0.0.alpha')
		info.SetDescription(description)
		info.SetCopyright('(C) 2013 G.Raja Sumant,Ashok Ashwin')

		info.SetLicence(licence)
		info.AddDeveloper('Ashok Ashwin')
		info.AddDocWriter('G.Raja Sumant')


		wx.AboutBox(info)

	def ClearDaub(self):
		self.st3.SetLabel("mean: ")
		self.st4.SetLabel("median: ")
		self.st5.SetLabel("mode: ")
		self.st6.SetLabel("kurtosis: ")
		self.st7.SetLabel("skew: ")
		self.st8.SetLabel("variance: ")

	def OnSelectRecord(self,event):
		self.current_record_value = self.combo.GetValue()
		self.current_channel_value = 0
		self.combo2.SetValue(str(self.current_channel_value))
		self.current_plot1_txt="plotting "+ self.current_record_value + " channel " + str(self.current_channel_value)
		self.current_signal_val=self.mat[self.current_record_value][0]
		self.draw_plot1(self.current_signal_val,self.current_plot1_txt)
		self.ClearDaub()

		i=0
		print self.mat[self.current_record_value]
		while i < self.mat[self.current_record_value].shape[0]:
			self.combo2.Append(str(i))
			i=i+1

	def OnSelectChannel(self,event):
		self.current_channel_value = int(self.combo2.GetValue())
		print self.current_channel_value
		self.current_signal_val=self.mat[self.current_record_value][self.current_channel_value]
		self.current_plot1_txt="plotting "+ self.current_record_value + " channel " + str(self.current_channel_value)
		self.draw_plot1(self.current_signal_val,self.current_plot1_txt)
		self.ClearDaub()

	def OnQuit(self,event):
		self.Close()

	def init_plot(self):
		self.dpi = 100
		self.fig = Figure()
		self.canvas = FigCanvas(self.panel, -1,self.fig)
		self.axes = self.fig.add_subplot(211)
		self.axes.set_axis_bgcolor('black')
		self.axes.set_title('no file loaded', size=12)
		self.line1=self.axes.plot(np.arange(len(np.linspace(0,13))),np.linspace(0,13))
		self.axes2 = self.fig.add_subplot(212)
		self.axes2.set_axis_bgcolor('black')
		self.axes2.set_title('no file loaded', size=12)
		self.line2=self.axes2.plot(np.arange(len(np.linspace(0,13))),np.linspace(0,13))




	def draw_plot1(self,a,txt):

		del self.axes.lines[0]
		self.fig.clf()
		self.axes = self.fig.add_subplot(211)
		self.axes.set_axis_bgcolor('white')
		self.axes.set_title(txt, size=12)
		self.line1,=self.axes.plot(a)
		self.canvas.draw()


	def draw_plot2(self,a,txt):
		self.draw_plot1(self.current_signal_val,self.current_plot1_txt)
		self.axes2 = self.fig.add_subplot(212)
		self.axes2.set_axis_bgcolor('white')
		self.axes2.set_title(txt, size=12)
		self.line2=self.axes2.plot(a)
		self.canvas.draw()


	def loadmatfile(self,event):
		dlg = wx.FileDialog(self,message="Choose a file",wildcard = "*.mat")

		if dlg.ShowModal() == wx.ID_OK:
			path = dlg.GetPath()
			print path + " is loaded"
			self.mat=sc.loadmat(path)
			self.combo.Clear()
			self.combo2.Clear()

			for record in self.mat.keys():
				if type(self.mat[record]) != type(''):
					self.combo.Append(record)

			self.current_signal_val=self.mat[self.mat.keys()[0]][0]


			self.current_plot1_txt="plotting "+ self.mat.keys()[0] + " channel " + "0"
			self.draw_plot1(self.current_signal_val,self.current_plot1_txt)

			i=0
			while i < self.mat[self.mat.keys()[0]].shape[0]:
				self.combo2.Append(str(i))
				i=i+1

		dlg.Destroy()




	def daubtran(self,event):
		h0=(1+m.sqrt(3))/(4*m.sqrt(2))
		h1=(3+m.sqrt(3))/(4*m.sqrt(2))
		h2=(3-m.sqrt(3))/(4*m.sqrt(2))
		h3=(1-m.sqrt(3))/(4*m.sqrt(2))

		g0 = h3
		g1 = -h2
		g2 = h1
		g3 = -h0

		a=self.current_signal_val
		n=len(self.current_signal_val)
		print self.current_plot1_txt
		if (n>=4):
			half = n >> 1
			tmp=[0]*n
			i=0
			j=0
			while (j<n-3):
				tmp[i]      = a[j]*h0 + a[j+1]*h1 + a[j+2]*h2 + a[j+3]*h3
				tmp[i+half] = a[j]*g0 + a[j+1]*g1 + a[j+2]*g2 + a[j+3]*g3
				j += 2
				i +=1
				tmp[i]      = a[n-2]*h0 + a[n-1]*h1 + a[0]*h2 + a[1]*h3
				tmp[i+half] = a[n-2]*g0 + a[n-1]*g1 + a[0]*g2 + a[1]*g3
		self.current_daub_value=tmp
		self.draw_plot2(self.current_daub_value,"daubechies plot")

		self.current_mean_value = np.mean(self.current_daub_value)
		self.current_median_value = np.median(self.current_daub_value)
		self.current_mode_value = int(st.mode(self.current_daub_value)[0])
		self.current_kurtosis_value = st.kurtosis(self.current_daub_value)
		self.current_skew_value = st.skew(self.current_daub_value)
		self.current_variance_value = st.tvar(self.current_daub_value)

		self.st3.SetLabel("mean: "+str(self.current_mean_value))
		self.st4.SetLabel("median: "+str(self.current_median_value))
		self.st5.SetLabel("mode: "+str(self.current_mode_value))
		self.st6.SetLabel("kurtosis: "+str(self.current_kurtosis_value))
		self.st7.SetLabel("skew: "+str(self.current_skew_value))
		self.st8.SetLabel("variance: "+str(self.current_variance_value))


	def SaveData(self,event):
		if self.current_daub_value != None:
			self.book = Workbook()
			sheet1 = self.book.add_sheet('analysed data')
			sheet1.write(0,0,"mean:")
			sheet1.write(0,1,self.current_mean_value)
			sheet1.write(1,0,"median:")
			sheet1.write(1,1,self.current_median_value)
			sheet1.write(2,0,"mode:")
			sheet1.write(2,1,self.current_mode_value)
			sheet1.write(3,0,"kurtosis:")
			sheet1.write(3,1,self.current_kurtosis_value)
			sheet1.write(4,0,"skew:")
			sheet1.write(4,1,self.current_skew_value)
			sheet1.write(5,0,"variance:")
			sheet1.write(5,1,self.current_variance_value)
			sheet1.write(6,0,"wavecoeff:")
			i = 0
			while i < len(self.current_daub_value):
				sheet1.write(7+i,0,"wavecoff(" + str(i) + ")")
				sheet1.write(7+i,1,self.current_daub_value[i])
				i=i+1
			dialog = wx.FileDialog ( self,message = "choose a filename" ,wildcard = "*.xls",  style = wx.SAVE)
			if dialog.ShowModal() == wx.ID_OK:
				name=dialog.GetPath()
				print 'Selected:', name
			else:
				print 'Nothing was selected.'
			dialog.Destroy()

			self.canvas.print_figure(name + ".png", dpi=self.dpi)
			file_in = name + ".png"
			img = Image.open(file_in)
			file_out = name + ".bmp"
			print len(img.split()) # test
			if len(img.split()) == 4:
				# prevent IOError: cannot write mode RGBA as BMP
				r, g, b, a = img.split()
				img = Image.merge("RGB", (r, g, b))
				img.save(file_out)
			else:
				img.save(file_out)
			sheet1.insert_bitmap(file_out, 0, 4)
			os.remove(file_in)
			os.remove(file_out)
			if name.endswith(".xls"):
				self.book.save(name)
			else:
				self.book.save(name+".xls")




def main():
	app=wx.App()
	frame=Eeg_Gui(None,-1,'EEGAnalyser')
	frame.Show()
	app.MainLoop()

main()
