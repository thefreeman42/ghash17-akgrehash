#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 18:56:54 2017

@author: pasztorbarna
"""

import numpy as np


#v = 10
#e = 8
#c = 5
# Initialize matrix R: Video X Endpoints, number of requests
#R = np.random.randint(0,100,(v,e))
# Initialize matrix L: Video X Endpoints, Latency from datacenter
#L = np.random.randint(0,100,(v,e))
# r: all requests


    # average latency without optimization, latency: sum(R*L)/r
    # Initialize CE: Cache X Endpoints, latency from cache
    #CE = np.random.randint(0,100,(c,e))
    # Initialize CV: Cache X Videos, 1 if connected, 0 if not
    #CV = [np.random.randint(0,2,(c,v)),np.random.randint(0,2,(c,v)),np.random.randint(0,2,(c,v))]

def evaluate(R, L, CE, GEN):

    r = np.sum(R)
    avglat = np.sum(np.multiply(R,L))/np.float64(r)

    def cv_eval(GEN):

        # L_up matrix: Video X Endpoints, latency from of videos that are in cache
        L_up = np.zeros((GEN.shape[1], CE.shape[1]), dtype="float64")
        for i in range(GEN.shape[1]):
            for j in range(CE.shape[1]):
                # if all zero it raises an error
                tmp = np.multiply(GEN.T[i, :], CE[:, j])
                if (np.nonzero(tmp)[0].shape[0] != 0):
                    minval = np.min(tmp[np.nonzero(tmp)])
                    #print(minval)
                    idmin = np.where(tmp==minval)[0][0]
                    #print(idmin)
                    L_up[i,j] = tmp[idmin]
        L_c = L.copy(z)
        # Update L from L'
        for i in range(L_up.shape[0]):
            for j in range(L_up.shape[1]):
                if (L_up[i,j] != 0):
                    L_c[i,j] = min([L_c[i,j],L_up[i,j]])
        return avglat - (np.sum(np.multiply(R,L_c))/np.float64(r))

    return list(map(cv_eval,GEN))

