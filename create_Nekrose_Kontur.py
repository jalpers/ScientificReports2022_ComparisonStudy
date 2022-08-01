# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 18:26:03 2021

@author: Maximilian Rötzer
"""
import heat2nekrose 
import nekrose2kontur
import SortFiles 
from pydicom import dcmread
import numpy as np
import matplotlib
import matplotlib.pyplot as plt



slices_angle = ["0","22_5","45","67_5","90","112_5","135","157_5" ]
slices_time = { "0","90","45","135_5","22_5","112_5","67_5","157_5" };
tStep = 13
threshold = 0
root_input = "Path/Phantome/"
phantoms = [ "PerfusionPhantom_1",
"PerfusionPhantom_2",
"PerfusionPhantom_3",
"PerfusionPhantom_4",
"PerfusionPhantom_5",
"PerfusionPhantom_6",
"TempPhantom_1",
"TempPhantom_2",
"Phantom_1",
"Phantom_2",
"Phantom_3",
"Phantom_4",
"Phantom_5"
]	
tsteps = [14,14,14,14,14,13,13,13,14,13,13,13,13]
thresh = [57,57,61,61,61,56,53,54,52,52,52,52,51,]

print(len(phantoms) == len(tsteps)==len(thresh))
#for i in range(len(phantoms)):
for i in range(len(phantoms)):
    initial_path = root_input+phantoms[i] + "/HeatMap/"
    SortFiles.sortFiles(initial_path, tsteps[i])

    path = initial_path + 'lastStep/'
    fileInput = path + slices_angle[7] + '_'+ str(tsteps[i]-1) + '.IMA'
    filenekrose_previous_tstp = path + slices_angle[7] +'_'+ str(tsteps[i]-1) + '_nekrose' + '.dcm'
    heat2nekrose.heat2nekrose(fileInput,filenekrose_previous_tstp ,threshold)



    for a in range(len(slices_angle)):
        fileInput = path + slices_angle[a] + '_' + str(tsteps[i]) + '.IMA'
        fileOutput = path + 'nekrose/'+ slices_angle[a] + '.dcm'
        heat2nekrose.heat2nekrose(fileInput,fileOutput ,thresh[i])
        
        fileOutput_korrektur = path + 'nekrose_korrektur/'+ slices_angle[a] + '.dcm'
        isCorrected = heat2nekrose.nekrose_correctur_erase(filenekrose_previous_tstp ,fileOutput,fileOutput_korrektur)
        
        dicom = dcmread(fileOutput_korrektur)
        img = np.uint8(dicom.pixel_array)
        # plt.imshow(img)
        # plt.show()
        #print(isCorrected)
        if not isCorrected:
            filenekrose_previous_tstp =fileOutput_korrektur
        fileInput = fileOutput_korrektur
        fileOutput = path + 'kontur/'+ slices_angle[a] + '.dcm'
        nekrose2kontur.nekrose2kontur(fileInput,fileOutput )