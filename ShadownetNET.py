#Preambule
from netCDF4 import Dataset
import os
import numpy as np

#Inladen data
file1 = 'Data1.nc'
ncdf = Dataset(file1, mode='r')

#Uithalen van de variabelen
Lon = ncdf.variables['longitude'][:]
Lat = ncdf.variables['latitude'][:]
Time = ncdf.variables['time'][:]
Level = ncdf.variables['level'][:]
#RV = ncdf.variables['RV'][:]

#
Templevel1 = ncdf.variables['slp'][:]
