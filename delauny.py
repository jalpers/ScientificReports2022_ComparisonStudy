# -*- coding: utf-8 -*-
"""
Created on Sun Jun 27 19:25:43 2021

@author: Maximilian Rötzer
"""
import pyvista as pv
import numpy as np
from pydicom import dcmread
import copy
def voxelize(dicom):
    dicom_reconstructed = copy.deepcopy(dicom)
    
    img = np.uint8(dicom.pixel_array)
    pnts = np.where(img > 0)
    x = pnts[0]
        #x.sort()
    y = pnts[1]
        #y.sort()
    z = pnts[2]
    vertices = np.array(list(zip(x, y,z)))
    polydata = pv.PolyData(vertices)

    surf = polydata.delaunay_3d(tol=0.001)
    
  
    voxels = pv.voxelize(surf, density=surf.length/100 )
    P = (voxels.points)
    P = P.astype(int)
    P = np.unique(P, axis=0)
    polydata = pv.PolyData(P)
    #polydata.plot(cpos="xy", show_edges=True)
    
    for row in P:
        dicom_reconstructed.pixel_array[row[0],row[1],row[2]] = 1
    
    dicom_reconstructed.PixelData = dicom_reconstructed.pixel_array.tobytes()
    
    #p = pv.Plotter()
    #p.add_mesh(voxels, color=True, show_edges=True, opacity=0.5)
    #p.add_mesh(surf, color="lightblue", opacity=0.5)
    #p.show()#cpos=cpos
    return dicom_reconstructed
    

root_input = "Path/Phantome/"
phantoms = [ "PerfusionPhantom_1","PerfusionPhantom_2","PerfusionPhantom_3","PerfusionPhantom_4","PerfusionPhantom_5","PerfusionPhantom_6","TempPhantom_1", "TempPhantom_2","Phantom_1","Phantom_2","Phantom_3","Phantom_4","Phantom_5"]
for i in range(len(phantoms)):
    file = root_input + phantoms[i] + "/HeatMap/lastStep/kontur/" +  phantoms[i]+"_kontur_3d.dcm"
    print(file)
    dicom = dcmread(file)       
    dicom_reconstructed = voxelize(dicom)
    dicom_reconstructed.save_as(root_input + "_results/" + phantoms[i] + "_delauny.dcm" )