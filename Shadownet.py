#%% Preambule and Data loading
from netCDF4 import Dataset
import os
from pylab import * 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
#from mpl_toolkits.basemap import Basemap, cm

#Inladen data
file1 = 'C:\Users\Mark\Desktop\Programmering\Shadowdata\Data3.nc'
ncdf = Dataset(file1, mode='r')
file2 = 'C:\Users\Mark\Desktop\Programmering\Shadowdata\Data4.nc'
ncdf2 = Dataset(file2, mode='r')

#Uithalen van de variabelen
Lon = ncdf.variables['longitude'][:]
Lat = ncdf.variables['latitude'][:]
Time = ncdf.variables['time'][:]

Lon_0 = Lon.mean()
Lat_0 = Lat.mean()
#%% Tracking
Lattrack = []
Longtrack = []
Tijdtrack = []
Ptrack = []
Numbertrack = []
for Tijdind in range(0,40):
    #Tijd keuze:
    Dag = 15+np.floor(Tijdind/4)
    Maand = 10
    Jaar = 1999
    Tijdstap = Tijdind-(Dag-15)*4 #1 = 0:00, 2 = 6:00, 3 = 12:00, 4 = 18:00
    if Maand == 8:
        Tijd = 4*(Dag-1)+ Tijdstap-1
    if Maand == 9:
        Tijd = 4*(Dag-1+31)+ Tijdstap-1
    if Maand == 10:
        Tijd = 4*(Dag-1+31+30)+ Tijdstap-1
    if Maand == 11:
        Tijd = 4*(Dag-1+31+30+31)+ Tijdstap-1
        
    
    Pres = ncdf.variables['msl'][Tijd][:][:]
    Temp = ncdf2.variables['t'][Tijd][:][:]
    U = ncdf2.variables['u'][Tijd][:][:]
    V = ncdf2.variables['v'][Tijd][:][:]
    VELO = np.sqrt(np.multiply(V,V)+np.multiply(U,U))
    #Temp = ncdf2.variables['t'][Tijd][:][:][:]
    #U = ncdf2.variables['u'][Tijd][:][:][:]
    #V = ncdf2.variables['v'][Tijd][:][:][:]
    
    #Temp850 = Temp[1][:][:]
    #Temp1000 = Temp[2][:][:]
    #U850 = U[2][:][:]
    #V850 = V[2][:][:]
    #VELO850 = sqrt(multiply(V850,V850)+multiply(U850,U850))
    
    #Temp_units = ncdf2.variables['t'].units
    
    # Pressure Minima finding
    AREA = 8 #Amount degrees around the wind maximum to search for Pmin
    AREA2 = AREA*4 #Adjusted to resolution
    latco = []
    longco = []
    for i in range(0,360):
        for j in range(0,560):
            if VELO[i,j]>=25:                    
                if len(latco)==0:
                    latco.append(i)
                    longco.append(j)
                if len(latco)>0:
                    if len(latco)==1:
                        if ((i-latco[len(latco)-1])**2+(j-longco[len(longco)-1])**2)>1800:
                            latco.append(i)
                            longco.append(j)
                    if len(latco)==2:
                        if ((i-latco[len(latco)-2])**2+(j-longco[len(longco)-2])**2)>1800 and ((i-latco[len(latco)-1])**2+(j-longco[len(longco)-1])**2)>1800:
                            latco.append(i)
                            longco.append(j)
                    if len(latco)==3:
                        if ((i-latco[len(latco)-3])**2+(j-longco[len(longco)-3])**2)>1800 and ((i-latco[len(latco)-2])**2+(j-longco[len(longco)-2])**2)>1800 and ((i-latco[len(latco)-1])**2+(j-longco[len(longco)-1])**2)>1800:
                            latco.append(i)
                            longco.append(j)
                    if len(latco)>=4:
                        if ((i-latco[len(latco)-4])**2+(j-longco[len(longco)-4])**2)>1800 and ((i-latco[len(latco)-3])**2+(j-longco[len(longco)-3])**2)>1800 and ((i-latco[len(latco)-2])**2+(j-longco[len(longco)-2])**2)>1800 and ((i-latco[len(latco)-1])**2+(j-longco[len(longco)-1])**2)>1800:
                            latco.append(i)
                            longco.append(j)

    d=0
    while d<len(longco):
        if longco[d]+AREA2>550:
            del longco[d]
            del latco[d]
        else:
            d=d+1
   
    matrixp = []
    latcop = []
    longcop = []
    latind = []
    longind = []
    pminvec = []
    pmins = []
    for i in range(0,len(longco)):
        for x in range(0,AREA2*2):
            for y in range(0,AREA2*2):
                matrixp.append(Pres[latco[i]+x-AREA2,longco[i]+y-AREA2])
        pminvec.append(min(enumerate(matrixp),key=(lambda x: x[1]))[0])
        pmins.append(matrixp[pminvec[i]])
        pmin = pminvec[i]
        matrixp = []
        latind.append(-AREA2+round(pmin/(2*AREA2))+latco[i])
        longind.append((pmin-(pmin/(AREA2*2))*(AREA2*2)-AREA2)+longco[i])
    
    testlat = latind
    testlong = longind
            
    for i in range(0,len(latind)):
        latcop.append(90-round(latind[i],2)/4)
        longcop.append(-100+round(longind[i],2)/4)
    k=0
    while k<len(latcop):
        if (latcop[k]>75):
            del longcop[k]
            del latcop[k]
            del pmins[k]
        else:
            k=k+1
        
    
    k=1
    while k<len(latcop):
        if (longcop[k]-longcop[k-1])**2+(latcop[k]-latcop[k-1])**2<200:
            if pmins[k]<pmins[k-1]:
                del longcop[k-1]
                del latcop[k-1]
                del pmins[k-1]
            elif pmins[k]>=pmins[k-1]:
                del longcop[k]
                del latcop[k]
                del pmins[k]
        else:
            k=k+1
    k=2
    while k<len(latcop):
        if (longcop[k]-longcop[k-2])**2+(latcop[k]-latcop[k-2])**2<200:
            if pmins[k]<pmins[k-2]:
                del longcop[k-2]
                del latcop[k-2]
                del pmins[k-2]
            elif pmins[k]>=pmins[k-2]:
                del longcop[k]
                del latcop[k]
                del pmins[k]
        else:
            k=k+1
    k=3
    while k<len(latcop):
        if (longcop[k]-longcop[k-3])**2+(latcop[k]-latcop[k-3])**2<200:
            if pmins[k]<pmins[k-3]:
                del longcop[k-3]
                del latcop[k-3]
                del pmins[k-3]
            elif pmins[k]>=pmins[k-3]:
                del longcop[k]
                del latcop[k]
                del pmins[k]
        else:
            k=k+1
    
        
    k=1
    while k<len(latcop):
        if (longcop[k]-longcop[k-1])**2+(latcop[k]-latcop[k-1])**2<200:
            if pmins[k]<pmins[k-1]:
                del longcop[k-1]
                del latcop[k-1]
                del pmins[k-1]
            elif pmins[k]>=pmins[k-1]:
                del longcop[k]
                del latcop[k]
                del pmins[k]
        else:
            k=k+1
    k=2
    while k<len(latcop):
        if (longcop[k]-longcop[k-2])**2+(latcop[k]-latcop[k-2])**2<200:
            if pmins[k]<pmins[k-2]:
                del longcop[k-2]
                del latcop[k-2]
                del pmins[k-2]
            elif pmins[k]>=pmins[k-2]:
                del longcop[k]
                del latcop[k]
                del pmins[k]
        else:
            k=k+1
    k=3
    while k<len(latcop):
        if (longcop[k]-longcop[k-3])**2+(latcop[k]-latcop[k-3])**2<200:
            if pmins[k]<pmins[k-3]:
                del longcop[k-3]
                del latcop[k-3]
                del pmins[k-3]
            elif pmins[k]>=pmins[k-3]:
                del longcop[k]
                del latcop[k]
                del pmins[k]
        else:
            k=k+1
    Ptrack.append(pmins)
    Lattrack.append(latcop)
    Longtrack.append(longcop)
    lop=[]
    for z in range(0,len(pmins)):
        lop.append(Tijd)
    Tijdtrack.append(lop)
    print "Number of storms on", int(Dag)," Oktober at ", int(Tijdstap*6),":00 is ",len(longcop)
    
    Numbvec=[]
    
    for numb in range(1,len(Ptrack[len(Ptrack)-1])+1):
        if len(Tijdtrack)==1:
            Numbvec.append(numb)
        else:
            Numbvec2=[]
            for numbef in range(1,len(Ptrack[len(Ptrack)-2])+1):
                if (Lattrack[len(Lattrack)-1][numb-1]-Lattrack[len(Lattrack)-2][numbef-1])**2 + (Longtrack[len(Longtrack)-1][numb-1]-Longtrack[len(Longtrack)-2][numbef-1])**2 < 50:
                    Numbvec2.append(Numbertrack[len(Lattrack)-2][numbef-1])
                elif (Lattrack[len(Lattrack)-1][numb-1]-Lattrack[len(Lattrack)-2][numbef-1])**2 + (Longtrack[len(Longtrack)-1][numb-1]-Longtrack[len(Longtrack)-2][numbef-1])**2 >= 50:
                    if len(Numbvec)==0:
                        Numbvec2.append(1+max([item for sublist in Numbertrack for item in sublist]))
                    elif len(Numbvec)>0:
                        Numbvec2.append(1+max([max([item for sublist in Numbertrack for item in sublist]),max(Numbvec)]))
            if len(Tijdtrack)>=3:
                for numbef in range(1,len(Ptrack[len(Ptrack)-3])+1):
                    if (Lattrack[len(Lattrack)-1][numb-1]-Lattrack[len(Lattrack)-3][numbef-1])**2 + (Longtrack[len(Longtrack)-1][numb-1]-Longtrack[len(Longtrack)-3][numbef-1])**2 < 50:
                        Numbvec2.append(Numbertrack[len(Lattrack)-3][numbef-1])
                    elif (Lattrack[len(Lattrack)-1][numb-1]-Lattrack[len(Lattrack)-3][numbef-1])**2 + (Longtrack[len(Longtrack)-1][numb-1]-Longtrack[len(Longtrack)-3][numbef-1])**2 >= 50:
                        if len(Numbvec)==0:
                            Numbvec2.append(1+max([item for sublist in Numbertrack for item in sublist]))
                        elif len(Numbvec)>0:
                            Numbvec2.append(1+max([max([item for sublist in Numbertrack for item in sublist]),max(Numbvec)]))
            if len(Tijdtrack)>=4:
                for numbef in range(1,len(Ptrack[len(Ptrack)-4])+1):
                    if (Lattrack[len(Lattrack)-1][numb-1]-Lattrack[len(Lattrack)-4][numbef-1])**2 + (Longtrack[len(Longtrack)-1][numb-1]-Longtrack[len(Longtrack)-4][numbef-1])**2 < 50:
                        Numbvec2.append(Numbertrack[len(Lattrack)-4][numbef-1])
                    elif (Lattrack[len(Lattrack)-1][numb-1]-Lattrack[len(Lattrack)-4][numbef-1])**2 + (Longtrack[len(Longtrack)-1][numb-1]-Longtrack[len(Longtrack)-4][numbef-1])**2 >= 50:
                        if len(Numbvec)==0:
                            Numbvec2.append(1+max([item for sublist in Numbertrack for item in sublist]))
                        elif len(Numbvec)>0:
                            Numbvec2.append(1+max([max([item for sublist in Numbertrack for item in sublist]),max(Numbvec)]))
            if len(Tijdtrack)>=5:
                for numbef in range(1,len(Ptrack[len(Ptrack)-5])+1):
                    if (Lattrack[len(Lattrack)-1][numb-1]-Lattrack[len(Lattrack)-5][numbef-1])**2 + (Longtrack[len(Longtrack)-1][numb-1]-Longtrack[len(Longtrack)-5][numbef-1])**2 < 50:
                        Numbvec2.append(Numbertrack[len(Lattrack)-5][numbef-1])
                    elif (Lattrack[len(Lattrack)-1][numb-1]-Lattrack[len(Lattrack)-5][numbef-1])**2 + (Longtrack[len(Longtrack)-1][numb-1]-Longtrack[len(Longtrack)-5][numbef-1])**2 >= 50:
                        if len(Numbvec)==0:
                            Numbvec2.append(1+max([item for sublist in Numbertrack for item in sublist]))
                        elif len(Numbvec)>0:
                            Numbvec2.append(1+max([max([item for sublist in Numbertrack for item in sublist]),max(Numbvec)]))

            Numbvec.append(min(Numbvec2))
                        
    Numbertrack.append(Numbvec)

#%% Manual adjustments
for j in range(0,len(Numbertrack)):
    for i in range(0,len(Numbertrack[j])):
        if Numbertrack[j][i]==8:
            Numbertrack[j][i]=3
    
#%% Plot around the storm
tijd = 31
number = 4
timevector = Tijdtrack[tijd-1][0]

Pres = ncdf.variables['msl'][timevector][:][:]
Temp = ncdf2.variables['t'][timevector][:][:]
U = ncdf2.variables['u'][timevector][:][:]
V = ncdf2.variables['v'][timevector][:][:]
VELO = np.sqrt(np.multiply(V,V)+np.multiply(U,U))

plt.figure(num=None, figsize=(10, 8), dpi=100, facecolor='w', edgecolor='k')
#Map
m = Basemap(llcrnrlon=Longtrack[tijd-1][number-1]-20,llcrnrlat=Lattrack[tijd-1][number-1]-15,urcrnrlon=Longtrack[tijd-1][number-1]+20,urcrnrlat=Lattrack[tijd-1][number-1]+15,
            resolution='l',projection='cyl',
            lat_ts=40,lat_0=Lat_0,lon_0=Lon_0)


#m = Basemap(llcrnrlon=-100,llcrnrlat=0,urcrnrlon=40,urcrnrlat=90,
#            resolution='l',projection='cyl',
#            lat_ts=40,lat_0=Lat_0,lon_0=Lon_0)

lon, lat = np.meshgrid(Lon, Lat)
xi, yi = m(lon, lat)

# Plot Data
cs = m.contourf(xi,yi,VELO,35)
KS= m.contour(xi,yi,Pres/100,10,linewidth=3.0,colors='k')
#RS= m.contour(xi,yi,VELO,10,linewidth=3.0,cmap=cm.gray)
#cs = m.contourf(xi,yi,VELO10,20,cmap=cm.gray)
plt.clabel(KS, inline=1, fontsize=8, fmt='%1.0f')
#plt.clabel(RS, inline=1, fontsize=8, fmt='%1.0f')
#RS= m.contour(xi,yi,VELO10,8,colors='k')
#plt.clabel(RS, inline=1, fontsize=8, fmt='%1.0f')
#plt.xticks(np.arange(min(Lon), max(Lon)+1, 20))
#plt.yticks(np.arange(min(Lat), max(Lat)+1, 10))

m.drawparallels(np.arange(0., 91., Lattrack[tijd-1][number-1]), labels=[1,0,0,0], fontsize=12)
m.drawmeridians(np.arange(-100., 40., 100+Longtrack[tijd-1][number-1]), labels=[0,0,0,1], fontsize=12)

m.drawcoastlines()

cbar = m.colorbar(cs, location='bottom', pad="10%")
#cbar.set_label('Kelvin')

plt.title('10m Wind speed and Mean sea level pressure', fontsize=14)

plt.show()
#plt.savefig('Test.png')

#%% Plot map with datapoints
plt.figure(num=None, figsize=(10, 8), dpi=100, facecolor='w', edgecolor='k')
#Map
m = Basemap(llcrnrlon=-100,llcrnrlat=0,urcrnrlon=40,urcrnrlat=90,
            resolution='l',projection='cyl',
            lat_ts=40,lat_0=Lat_0,lon_0=Lon_0)

lon, lat = np.meshgrid(Lon, Lat)
xi, yi = m(lon, lat)

Longi = [item for sublist in Longtrack for item in sublist]
Latti = [item for sublist in Lattrack for item in sublist]

m.scatter(Longi,Latti)
m.drawparallels(np.arange(0., 91., 30.), labels=[1,0,0,0], fontsize=12)
m.drawmeridians(np.arange(-100., 40., 20.), labels=[0,0,0,1], fontsize=12)
m.drawcoastlines()

plt.title('Locations stormpoints', fontsize=14)

plt.show()


#%% Plot total map around storm
tijd = 36
number = 4
timevector = Tijdtrack[tijd-1][0]

Pres = ncdf.variables['msl'][timevector][:][:]
Temp = ncdf2.variables['t'][timevector][:][:]
U = ncdf2.variables['u'][timevector][:][:]
V = ncdf2.variables['v'][timevector][:][:]
VELO = np.sqrt(np.multiply(V,V)+np.multiply(U,U))

plt.figure(num=None, figsize=(10, 8), dpi=100, facecolor='w', edgecolor='k')
m = Basemap(llcrnrlon=-100,llcrnrlat=0,urcrnrlon=40,urcrnrlat=90,
            resolution='l',projection='cyl',
            lat_ts=40,lat_0=Lat_0,lon_0=Lon_0)

Longo=Longtrack[tijd-1]
Latto=Lattrack[tijd-1]

lon, lat = np.meshgrid(Lon, Lat)
xi, yi = m(lon, lat)
cs = m.contourf(xi,yi,VELO,35)
KS= m.contour(xi,yi,Pres/100,10,linewidth=3.0,colors='k')
plt.clabel(KS, inline=1, fontsize=8, fmt='%1.0f')

m.scatter(Longo,Latto,s=np.pi*5**2, c='white', alpha=0.85)
m.drawparallels(np.arange(0., 91.,30.), labels=[1,0,0,0], fontsize=12)
m.drawmeridians(np.arange(-100., 40.,20.), labels=[0,0,0,1], fontsize=12)
m.drawcoastlines()

cbar = m.colorbar(cs, location='bottom', pad="10%")
plt.title('10m Wind speed and Mean sea level pressure', fontsize=14)
plt.show()


#%% Plot one specific stormtrack
Number = 3
#Filter
Numbi = [item for sublist in Numbertrack for item in sublist]
Longi = [item for sublist in Longtrack for item in sublist]
Latti = [item for sublist in Lattrack for item in sublist]
Pressi = [item for sublist in Ptrack for item in sublist]

Longgat=[]
Latgat=[]
Presgat=[]

for i in range(0,len(Numbi)):
    if Numbi[i]==Number:
        Longgat.append(Longi[i])
        Latgat.append(Latti[i])
        Presgat.append(Pressi[i])


plt.figure(num=None, figsize=(10, 8), dpi=100, facecolor='w', edgecolor='k')
#Map
m = Basemap(llcrnrlon=-100,llcrnrlat=0,urcrnrlon=40,urcrnrlat=90,
            resolution='l',projection='cyl',
            lat_ts=40,lat_0=Lat_0,lon_0=Lon_0)

lon, lat = np.meshgrid(Lon, Lat)
xi, yi = m(lon, lat)

m.scatter(Longgat,Latgat)
m.drawparallels(np.arange(0., 91., 30.), labels=[1,0,0,0], fontsize=12)
m.drawmeridians(np.arange(-100., 40., 20.), labels=[0,0,0,1], fontsize=12)
m.drawcoastlines()

plt.title('Location specific storm', fontsize=14)

plt.show()

plt.plot(array(Presgat)/100)
plt.ylim([940,1010])
plt.ylabel('Pressure in hPa')
plt.show()

#%% Plot one specific stormtrack
Numbertime = 18
Number = 3
#Filter
Numbi = [item for sublist in Numbertrack for item in sublist]
Longi = [item for sublist in Longtrack for item in sublist]
Latti = [item for sublist in Lattrack for item in sublist]
Pressi = [item for sublist in Ptrack for item in sublist]
Tijdi = [item for sublist in Tijdtrack for item in sublist]

Longgat=[]
Latgat=[]
Presgat=[]
Tijdgat=[]

for i in range(0,len(Numbi)):
    if Numbi[i]==Number:
        Longgat.append(Longi[i])
        Latgat.append(Latti[i])
        Presgat.append(Pressi[i])
        Tijdgat.append(Tijdi[i])
        
timevector=Tijdgat[Numbertime]

Pres = ncdf.variables['msl'][timevector][:][:]
Temp = ncdf2.variables['t'][timevector][:][:]
U = ncdf2.variables['u'][timevector][:][:]
V = ncdf2.variables['v'][timevector][:][:]
VELO = np.sqrt(np.multiply(V,V)+np.multiply(U,U))

plt.figure(num=None, figsize=(10, 8), dpi=100, facecolor='w', edgecolor='k')
m = Basemap(llcrnrlon=Longgat[Numbertime]-20,llcrnrlat=Latgat[Numbertime]-15,urcrnrlon=Longgat[Numbertime]+20,urcrnrlat=Latgat[Numbertime]+15,
            resolution='l',projection='cyl',
            lat_ts=40,lat_0=Lat_0,lon_0=Lon_0)

lon, lat = np.meshgrid(Lon, Lat)
xi, yi = m(lon, lat)
cs = m.contourf(xi,yi,VELO,35)
KS= m.contour(xi,yi,Pres/100,10,linewidth=3.0,colors='k')
plt.clabel(KS, inline=1, fontsize=8, fmt='%1.0f')
m.drawparallels(np.arange(0., 91., Latgat[Numbertime]), labels=[1,0,0,0], fontsize=12)
m.drawmeridians(np.arange(-100., 40., 100+Longgat[Numbertime]), labels=[0,0,0,1], fontsize=12)
m.drawcoastlines()
cbar = m.colorbar(cs, location='bottom', pad="10%")

plt.title('Individual storm at a specific point in time (Wind and slp)', fontsize=14)
plt.show()

