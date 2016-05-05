import numpy as np
import matplotlib.pyplot as plt
import math as M
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap, cm
#import pyfits as pf

#Find data
file = open("C:\Users\Mark\Desktop\Programmering\Shadowdata\Time=0.txt", "r")
lines = file.readlines()
file.close()

#Create Variables
Pres = []
Lat = []
Lon = []
for j in range(0,180):
    Lat.append(j*0.5)
for j in range(0,280):
    Lon.append(j*0.5)
for j in range(0,len(lines)):
    Pres.append(float(lines[j]))
Pres2 = np.zeros((181, 281))
for j in range(0,len(Lat)):
    for i in range(0,len(Lon)):
        Pres2[j-1][i-1]=(Pres[j*280+i-1])

#Testplot
fig = plt.figure(figsize=(8,8))
ax = fig.add_axes([0.1,0.1,0.8,0.8])
# create polar stereographic Basemap instance.
m = Basemap(llcrnrlon=-100.,llcrnrlat=0.,urcrnrlon=-20.,urcrnrlat=57.,
            projection='lcc',lat_1=20.,lat_2=40.,lon_0=-60.,
            resolution ='l',area_thresh=1000.)
# draw coastlines, state and country boundaries, edge of map.
m.drawcoastlines()
m.drawstates()
m.drawcountries()
# draw parallels.
parallels = np.arange(0.,90,10.)
m.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
# draw meridians
meridians = np.arange(180.,360.,10.)
m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)
# draw filled contours.
clevs = [0,1,2.5,5,7.5,10,15,20,30,40,50,70,100,150,200,250,300,400,500,600,750]
cs = m.contourf(Lon,Lat,Pres2,clevs,cmap=cm.s3pcpn)
# add colorbar.
cbar = m.colorbar(cs,location='bottom',pad="5%")
cbar.set_label('mm')
# add title
plt.title('Hoi')
plt.show()