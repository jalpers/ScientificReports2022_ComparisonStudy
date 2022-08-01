# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 16:39:58 2021

@author: Maximilian Rötzer
"""

import numpy as np
from pydicom import dcmread
import matplotlib.pyplot as plt
import EllipsoidTool as ElTo
import copy


def doEllipse(dicom):
    dicom_reconstructed = copy.deepcopy(dicom)
    for i in range(np.shape(np.uint8(dicom.pixel_array))[1]):
        img = np.uint8(dicom.pixel_array)[:,i,:]
                
        P = np.argwhere(img>0)
            
        if len(P)<5:
            continue
        
        ET = ElTo.EllipsoidTool()
        (center, radii, rotation) = ET.getMinVolEllipse(P, .01)
        
        
        img_size = img.shape
        img_reconstructed = np.zeros((60,60))
        
        for x in range(img_size[0]):
            for y in range(img_size[1]):
                coord= np.array([x, y])

                if ET.isInsideEllipsoid(coord, center, radii,rotation):
                    img_reconstructed[x,y] = 1

        dicom_reconstructed.pixel_array[:,i,:] = img_reconstructed
        #plt.imshow(dicom_reconstructed.pixel_array[:,i,:],cmap=plt.cm.gray)
    dicom_reconstructed.PixelData = dicom_reconstructed.pixel_array.tobytes()
    return dicom_reconstructed
       


root_input = "Path/Phantome/"
phantoms = [ "PerfusionPhantom_1","PerfusionPhantom_2","PerfusionPhantom_3","PerfusionPhantom_4","PerfusionPhantom_5","PerfusionPhantom_6","TempPhantom_1", "TempPhantom_2","Phantom_1","Phantom_2","Phantom_3","Phantom_4","Phantom_5"]
for i in range(len(phantoms)):
    file = root_input + phantoms[i] + "/HeatMap/lastStep/nekrose_korrektur/" +  phantoms[i]+"_nekrose_3d.dcm"
    print(file)
    dicom = dcmread(file)       
    dicom_reconstructed = doEllipse(dicom)
    dicom_reconstructed.save_as(root_input + "_results/" + phantoms[i] + "_ellipse.dcm" )