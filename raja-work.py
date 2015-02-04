#######################################################
# imports go here

import numpy as np
import scipy.signal as sc
import pywt as wt
import matplotlib.pyplot as p

#
#######################################################

wavelet2 = wt.Wavelet('db2')
wavelet4 = wt.Wavelet('db4')
wavelet6 = wt.Wavelet('db20')

'''
for i in xrange(1,6):

    [phi,psi,x] = wavelet2.wavefun(level= i)
    p.subplot(5,3,3*i-2)
    p.plot(np.abs(np.fft.fft(phi))[0:len(phi)/2+1])
    p.plot(np.abs(np.fft.fft(psi))[0:len(phi)/2+1],'r-')

    [phi,psi,x] = wavelet4.wavefun(level= i)
    p.subplot(5,3,3*i-1)
    p.plot(np.abs(np.fft.fft(phi))[0:len(phi)/2+1])
    p.plot(np.arange(len(phi)/2+1),np.abs(np.fft.fft(psi))[0:len(phi)/2+1],'r-')

    [phi,psi,x] = wavelet6.wavefun(level= i)
    p.subplot(5,3,3*i)
    p.plot(np.abs(np.fft.fft(phi))[0:len(phi)/2+1])
    p.plot(np.abs(np.fft.fft(psi))[0:len(phi)/2+1],'r-')

p.show()
'''

[phi,psi,x] = wavelet4.wavefun(level= 3)
l=len(psi)

print psi[0:len(psi):8],len(psi)


z=np.zeros(l)
z[l/2+1]=1
h=np.convolve(z,psi)
f=np.fft.fft(h)
f = f[0:len(f):16]
print len(f)
p.plot(abs(f)[0:len(f)/2])
p.figure(2)

p.stem(psi[0:len(psi):8])
p.show()

[-0.010597401784997278,0.032883011666982945,0.030841381835986965,-0.18703481171888114,-0.02798376941698385,0.6308807679295904,0.7148465705525415,0.23037781330885523]