# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 12:54:19 2021

@author: Maximilian Rötzer
"""
from pydicom import dcmread
import matplotlib.pyplot as plt
import numpy as np

def nekrose2kontur(file_input, file_output):
        dicom = dcmread(file_input)
        img = np.uint8(dicom.pixel_array)
        # plt.imshow(img)
        # plt.show()  
        kontur_img = np.zeros((60,60))
        orient = dicom[0x0020,0x0037].value[1]
        
        for v in range(60):
            border1 = 0 
            border2 = 0
            for w in range(60):
                if (border1 == 0):
                    if (orient == 0):
                        border1 = img[v,w]
                        kontur_img[v,w] = border1
                    else:
                        border1 = img[w,v]
                        kontur_img[w,v] = border1
                if (border2 == 0):
                    if (orient == 0):
                        border2 = img[v,60-w-1]
                        kontur_img[v,60-w-1] = border2 
                    else:
                        border2 = img[60-w-1,v]
                        kontur_img[60-w-1,v] = border2 
                if border1 ==1 and border2 ==1:
                    break
                    
        # plt.imshow(kontur_img)
        # plt.show()                
        dicom.pixel_array[:,:] = kontur_img
        dicom.PixelData = dicom.pixel_array.tobytes()   
        dicom.save_as(file_output)       
        
