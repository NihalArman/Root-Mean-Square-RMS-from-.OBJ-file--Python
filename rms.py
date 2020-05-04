# https://math.stackexchange.com/questions/99299/best-fitting-plane-given-a-set-of-points
# https://www.youtube.com/watch?v=DKt4HRBqH1I
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math

'''
N_POINTS = 9
TARGET_X_SLOPE = 50
TARGET_y_SLOPE = 3
TARGET_OFFSET  = 5
EXTENTS = 5
NOISE = 5

# create random data
xs = [np.random.uniform(2*EXTENTS)-EXTENTS for i in range(N_POINTS)]
ys = [np.random.uniform(2*EXTENTS)-EXTENTS for i in range(N_POINTS)]
zs = []
for i in range(N_POINTS):
    zs.append(xs[i]*TARGET_X_SLOPE + \
              ys[i]*TARGET_y_SLOPE + \
              TARGET_OFFSET + 5*np.random.normal(scale=NOISE))
'''
# xs=[0.686157,2.686157,0.686157,2.686157,0.686157,1.686157,2.686157,1.686157,1.686157]
# zs=[2.797302,1.797302,0.797302,0.797302,0.797302,0.797302,0.797302,0.797302,0.797302]
# ys=[1.611370,1.611370,-0.388630,-0.388630,0.611370,1.611370,0.611370,-0.388630,0.611370]

# Import mesh from OBJ-file
mesh_obj_path = r'C:\Users\Nihal\Desktop\average spectra\3D Mesh\7. Band 131\Mesh\3DF Zephyr\band131mesh.obj'
f = open(mesh_obj_path, "r")
filelines = f.readlines()
xx = []
yy = []
zz = []
for fileline in filelines:
    if 'v ' in fileline.lower():
        line = fileline.replace('v ', '')
        [x, y, z] = line.split(' ')
        print(x, y, z)
        xx.append(float(x))
        yy.append(float(y))
        zz.append(float(z))
xs = np.array(xx)
zs = np.array(yy)
ys = np.array(zz)

print(xs)
print(ys)
print(zs)

# plot raw data
plt.figure()
ax = plt.subplot(111, projection='3d')
ax.scatter(xs, ys, zs, color='b')

# do fit
tmp_A = []
tmp_b = []
for i in range(len(xs)):
    tmp_A.append([xs[i], ys[i], 1])
    tmp_b.append(zs[i])
b = np.matrix(tmp_b).T
A = np.matrix(tmp_A)
fit = (A.T * A).I * A.T * b
errors = b - A * fit
residual = np.linalg.norm(errors)

print("solution:")
print("%f x + %f y + %f = z" % (fit[0], fit[1], fit[2]))
print("errors:")
print(errors)
print("residual:")
print(residual)
# mean square root error
error = 0
nu = 0
for er in errors:
    error = error + er * er
    nu = nu + 1
rms = math.sqrt(error / nu)
print('rms: ', rms)

# plot plane
xlim = ax.get_xlim()
ylim = ax.get_ylim()
X, Y = np.meshgrid(np.arange(xlim[0], xlim[1]),
                   np.arange(ylim[0], ylim[1]))
Z = np.zeros(X.shape)
for r in range(X.shape[0]):
    for c in range(X.shape[1]):
        Z[r, c] = fit[0] * X[r, c] + fit[1] * Y[r, c] + fit[2]
ax.plot_wireframe(X, Y, Z, color='k')

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
# plt.show()

for angle in range(0, 360):
    ax.view_init(30, angle)
    ax.set_zlim3d(-1, 1)
    plt.draw()
    plt.pause(.001)

