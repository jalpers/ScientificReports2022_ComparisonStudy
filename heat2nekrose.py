# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 16:09:31 2021

@author: Maximilian Rötzer
"""
import vtk
from vtk.util import numpy_support
import numpy as np
import matplotlib.pyplot as plt
import cv2

from skimage import measure
from scipy import ndimage
from pydicom import dcmread
import shutil

def heat2nekrose(file_input, file_output, threshold):

    reader = vtk.vtkDICOMImageReader()
    reader.SetFileName(file_input)
    reader.Update()
    


    
   
    imageData = reader.GetOutput()

    pointData = imageData.GetPointData()

    assert (pointData.GetNumberOfArrays()==1)
   
    arrayData = pointData.GetArray(0)
    
   
    ArrayDicom = numpy_support.vtk_to_numpy(arrayData)

    array = (ArrayDicom.reshape((60,60), order='F'))
    
    
    array = np.rot90(array)
    
    array = ndimage.median_filter(array, size=3)
    
    img_bw = np.zeros((60,60))
    img_bw[array >= threshold] = 1
    
    #_________________________________________
    g = np.array(img_bw,dtype="uint8")
    kernel1 = np.array((
        [0, -1, 0],
        [1, 1, 1],
        [0, -1, 0]), dtype="int")

    img_hm_1 = cv2.morphologyEx(g, cv2.MORPH_HITMISS, kernel1)
    
    kernel1 = np.array((
        [0, 1, 0],
        [-1, 1,- 1],
        [0, 1, 0]), dtype="int")
    img_hm_2 = cv2.morphologyEx(g, cv2.MORPH_HITMISS, kernel1)
    
   
    img_bw2 = img_bw - img_hm_1 -img_hm_2
        
    labels = measure.label(img_bw2, background=0,connectivity = 1) 
    largest_area = np.argmax(np.bincount(labels.flat)[1:])+1
    largestCC = labels == largest_area

    nekrose2 =np.multiply(largestCC , 1)
   
    
    

    labels = measure.label(img_bw, background=0,connectivity = 1) 
    largest_area = np.argmax(np.bincount(labels.flat)[1:])+1
    largestCC = labels == largest_area
    
   
    ds = dcmread(file_input)
    ds.pixel_array[:,:] = nekrose2
    ds.PixelData = ds.pixel_array.tobytes()   
    ds.save_as(file_output)    
  
def nekrose_korrektur(file_input_last_timestp, file_input_current_timstp, folder_output):
    dicom_last = dcmread(file_input_last_timestp)
    img_last = np.uint8(dicom_last.pixel_array)
    
    dicom_now = dcmread(file_input_current_timstp)
    img_now = np.uint8(dicom_now.pixel_array)

    sum_last = np.sum(img_last)
    sum_now = np.sum(img_now)
    plt.imshow(img_now)
    plt.show()
    if(sum_now  > sum_last*1.8):
        print('korrektur')
        orient_last = dicom_last[0x0020,0x0037].value[1]
        #print(orient_last)
        # plt.imshow(img_last)
        # plt.show()
        orient_now = dicom_now[0x0020,0x0037].value[1]
        #print(orient_now)
        # plt.imshow(img_now)
        # plt.show()
        if orient_last !=orient_now :
            img_last= np.rot90(img_last)

        dicom_now.pixel_array[:,:] = img_last
        dicom_now.PixelData = dicom_now.pixel_array.tobytes()

        dicom_now.save_as(folder_output)
        plt.imshow(dicom_now.pixel_array)
        plt.show()
        

    else:  
        shutil.copyfile(file_input_current_timstp, folder_output)
        

def nekrose_correctur_erase(file_input_last_timestp, file_input_current_timstp, folder_output):
    dicom_last = dcmread(file_input_last_timestp)
    img_last = np.uint8(dicom_last.pixel_array)
    
    dicom_now = dcmread(file_input_current_timstp)
    img_now = np.uint8(dicom_now.pixel_array)

    sum_last = np.sum(img_last)
    sum_now = np.sum(img_now)
    plt.imshow(img_now)
    plt.show()
    img_zeros = np.zeros((60,60))
    if(sum_now  > sum_last*1.8):
        print('corrupted Data -------------------------------------------------------')


        dicom_now.pixel_array[:,:] = img_zeros
        dicom_now.PixelData = dicom_now.pixel_array.tobytes()

        dicom_now.save_as(folder_output)
        return True

    else:  
        shutil.copyfile(file_input_current_timstp, folder_output)
        return False
    
    