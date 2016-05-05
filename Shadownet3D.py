#%% 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
X, Y, Z = axes3d.get_test_data(0.05)
ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)

fig = plt.figure()
ax = fig.gca(projection='3d')
X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.set_zlim(-1.01, 1.01)

ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%0.02f'))

fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()


plt.show()

#%% Advanced 3D plot
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm

fig = plt.figure(num=None, figsize=(10, 8), dpi=100, facecolor='w', edgecolor='k')
ax = fig.gca(projection='3d')
#X, Y, Z = axes3d.get_test_data(0.1)
X, Y, Z = (array([[-4,-2,0,2,4],[-4,-2,0,2,4],[-4,-2,0,2,4],[-4,-2,0,2,4],[-4,-2,0,2,4]]),
           array([[-4,-4,-4,-4,-4],[-2,-2,-2,-2,-2],[0,0,0,0,0],[2,2,2,2,2],[4,4,4,4,4]])
           ,array([[1,1,1,1,1],[1,2,2,2,1],[1,2,3,2,1],[1,2,2,2,1],[1,1,-1,1,1]]))
           
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, alpha=0.3)
cset = ax.contourf(X, Y, Z, zdir='z', offset=-2, cmap=cm.coolwarm)
cset = ax.contourf(X, Y, Z, zdir='x', offset=-5, cmap=cm.coolwarm)
cset = ax.contourf(X, Y, Z, zdir='y', offset=5, cmap=cm.coolwarm)

ax.set_xlabel('X')
ax.set_xlim(-5, 5)
ax.set_ylabel('Y')
ax.set_ylim(-5, 5)
ax.set_zlabel('Z')
ax.set_zlim(-2, 5)

plt.show()

#%% Loaded 3D data
vari=2
file3 = 'C:\Users\Mark\Desktop\Programmering\Shadowdata\Data5.nc'
ncdf3 = Dataset(file3, mode='r')
levels = ncdf3.variables['level'][:]

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

if vari == 1:
    VAR = Pres
elif vari==2:
    VAR = VELO

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm

#Boundaries
centerlong=Longgat[Numbertime]
centerlat=Latgat[Numbertime]


fig = plt.figure(num=None, figsize=(10, 8), dpi=100, facecolor='w', edgecolor='k')
ax = fig.gca(projection='3d')
K=[]
VEC=[]
Y=[]
for i in range(0,len(Lon)):
    j = round(-100.+round(i/4.,2),2)
    VEC.append(j)
for i in range(0,len(Lat)):
    K.append(VEC)
for i in range(0,len(Lat)):
    E = np.zeros((len(Lon)),dtype='d')+i/4.
    Y.append(E)
Z=VAR
Z=Z[::-1]
Zlat=[]
Zlong=[]
for i in range (0,len(Lat)):
    Zlat.append(Z[centerlat*4])
    F = np.zeros((len(Lon)),dtype='d')+Z[centerlat*4][i]
    Zlong.append(F)
Zlat=array(Zlat)
X=array(K)
Y=array(Y)
Zlong=array(Zlong)
Ztest=Z
Xn=X[(centerlat*4-60):(centerlat*4+60+1)]
Yn=Y[(centerlat*4-60):(centerlat*4+60+1)]
Zn=Z[(centerlat*4-60):(centerlat*4+60+1)]
Zlatn=Zlat[(centerlat*4-60):(centerlat*4+60+1)]
Zlongn=Zlong[(centerlat*4-60):(centerlat*4+60+1)]
X=[]
Y=[]
Z=[]
Zlat=[]
Zlong=[]
for r in range(0,121):
    X.append(Xn[r][((centerlong+100)*4-80):((centerlong+100)*4+80+1)])
    Y.append(Yn[r][((centerlong+100)*4-80):((centerlong+100)*4+80+1)])
    Z.append(Zn[r][((centerlong+100)*4-80):((centerlong+100)*4+80+1)])
    Zlat.append(Zlatn[r][((centerlong+100)*4-80):((centerlong+100)*4+80+1)])
    Zlong.append(Zlongn[r][((centerlong+100)*4-80):((centerlong+100)*4+80+1)])
    
X=array(X)
Y=array(Y)
Z=array(Z)
Zlat=array(Zlat)
Zlong=array(Zlong)
m=Basemap(llcrnrlon=centerlong-20,llcrnrlat=centerlat-15,urcrnrlon=centerlong+20,urcrnrlat=centerlat+15,
            resolution='l',projection='cyl',
            lat_ts=40,lat_0=Lat_0,lon_0=Lon_0)
ax.add_collection3d(m.drawcoastlines(linewidth=0.25))
ax.add_collection3d(m.drawcountries(linewidth=0.35))
ax.plot_surface(X, Y, Z, rstride=15, cstride=15, alpha=0.2, color="red")
cset = ax.contourf(X, Y, Z, 15, zdir='z', offset=0.)
#cset = ax.contourf(X, Y, Z, 15, zdir='z', offset=0.)
matplotlib.rcParams['contour.negative_linestyle'] = 'solid'
cset = ax.contour(X, Y, Zlong, 10, zdir='x', offset=centerlong-20,colors='k')
cset = ax.contour(X, Y, Zlat, 10, zdir='y', offset=centerlat+15,colors="black")



#ax.add_collection3d()
#cset = ax.contourf(X[centerlat*4], Y[centerlat*4], Z[centerlat*4], 10, zdir='y', offset=90)

ax.set_xlabel('Longitude')
ax.set_xlim(centerlong-20, centerlong+20)
ax.set_ylabel('Latitude')
ax.set_ylim(centerlat-15, centerlat+15)
ax.set_zlabel('Wind at 850 hPa')
ax.set_zlim(0, 50)
#ax.add_collection3d(m.drawmeridians(np.arange(-100., 40., 20), labels=[1,0,0,0], fontsize=12))
#plt.rcParams['lines.linewidth'] = 2
#ax.w_xaxis.gridlines.set_lw(1.0)
#ax.w_yaxis.gridlines.set_lw(3.0)
#ax.w_zaxis.gridlines.set_lw(3.0)
#ax.grid(True)
ax.view_init(elev=50., azim=-50)

ax.grid(linewidth=20)
plt.show()