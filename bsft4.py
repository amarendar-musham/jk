__author__ = 'ashwin'


######################################################################################
#                   Pythonic implementation of Pachori's
#                  Features based on Fourier-Bessel series
######################################################################################

import numpy as np
from scipy.special import jn, yn, jn_zeros, yn_zeros



######################################################################################
# Step 1: calculation of C_m
#
# As analogous to fourier series, the more number of coefficients, the greater the
# Signal reconstruction.
# z_m are the first M roots of J_0
#
# The choice of M is quite non-trivial
# We know that in segmentation the entire frequency range is divided into segments
# let us, In this case consider the frequency range be divided into 8 segments,
# Each containing a 16 hz band
# We model this 16 hz band as a group of 16 frequency steps
# 16*8=128
# We can also choose any other segmentation method
#
#
# In Pachori's paper the frequency band is divided into 26 segments
######################################################################################


def cmcreate(x):

    N = len(x)
    M = N
    z_m = jn_zeros(0,M)
    c_m = np.zeros_like(z_m).astype(np.float32)
    for i in xrange(M):
        sum = 0
        for j in xrange(N):
            sum+=(j*x[j]*jn(0,(z_m[i]*j/N)))
        c_m[i] = (2*sum)/((jn(1,z_m[i])*N)**2)
    return c_m,M,N,z_m

##############################################################################
# Reconstruction of the signals from Bessel Coefficients
##############################################################################



def reconseg(bsl_coeff,M,N,z_m):
    
    segs=np.zeros((1,M),dtype=float)
    delta = np.zeros(N)
    for i in xrange(N):
        sum = 0
        for j in xrange(0,18):
            sum+=bsl_coeff[j]*(jn(0,(z_m[j]*i/N)))
        delta[i] = sum
    segs=np.vstack((segs,delta))
    
    theta = np.zeros(N)
    for i in xrange(N):
        sum = 0
        for j in xrange(19,32):
            sum+=bsl_coeff[j]*(jn(0,(z_m[j]*i/N)))
        theta[i] = sum
    segs=np.vstack((segs,theta))
    
    alpha = np.zeros(N)
    for i in xrange(N):
        sum = 0
        for j in xrange(33,64):
            sum+=bsl_coeff[j]*(jn(0,(z_m[j]*i/N)))
        alpha[i] = sum
    segs=np.vstack((segs,alpha))

    beta = np.zeros(N)
    for i in xrange(N):
        sum = 0
        for j in xrange(65,130):
            sum+=bsl_coeff[j]*(jn(0,(z_m[j]*i/N)))
        beta[i] = sum
    segs=np.vstack((segs,beta))


    gamma = np.zeros(N)
    for i in xrange(N):
        sum = 0
        for j in xrange(130,N):
            sum+=bsl_coeff[j]*(jn(0,(z_m[j]*i/N)))
        gamma[i] = sum
    segs=np.vstack((segs,gamma))

    return segs


def fbdecomp(x):
    c_m,M,N,z_m = cmcreate(x)
    segs = reconseg(c_m,M,N,z_m)
    return segs[1:len(segs)]

