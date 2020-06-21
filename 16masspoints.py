import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
from func_define import *

# figure
fig = plt.figure()
ax = Axes3D(fig)
ax.view_init(elev=14, azim=-23)
ax.set_xlim(-10, 10)
ax.set_ylim(-50, 50)
ax.set_zlim(-10, 10)

# 初期条件
# 質点位置・元質点に連結されている質点位置
boundaryx = [-10, 10]
boundaryy = [-10, 10]
countx = boundaryx[1] - boundaryx[0] + 1
county = boundaryy[1] - boundaryy[0] + 1
xs = np.linspace(*boundaryx, countx)
ys = np.linspace(*boundaryy, county)
X, Y = np.meshgrid(xs, ys)
Z = np.zeros([countx, county])
Z[10, 10] = -40
masspoints = np.dstack([X, Y, Z])
masspoints_constraints_index = [[0,0], [0,20], [20,0], [20,20], [10,10]]
masspoints_constraints_value = [masspoints[masspoints_constraints_index[0][0], masspoints_constraints_index[0][1]], \
                                masspoints[masspoints_constraints_index[1][0], masspoints_constraints_index[1][1]], \
                                masspoints[masspoints_constraints_index[2][0], masspoints_constraints_index[2][1]], \
                                masspoints[masspoints_constraints_index[3][0], masspoints_constraints_index[3][1]], \
                                masspoints[masspoints_constraints_index[4][0], masspoints_constraints_index[4][1]]]
#　パラメータ
dt = 0.01   # 計算区切り
k = 10     # ばね定数
l0 = 1      # 自然長
m = 0.01       # 質量
v0 = [0, 0, 0]      # 初速度
roop = 2000     # 計算ループ数
# 変数整理
masspoints_x_count = masspoints.shape[0]
masspoints_y_count = masspoints.shape[1]
elements = masspoint2element(masspoints, boundaryx, boundaryy)

# 張力計算
T = np.zeros([masspoints_x_count, masspoints_y_count, 3])
dist = np.zeros([masspoints_x_count, masspoints_y_count, 3])
artists = []
for _ in range(roop):
    for i in range(masspoints_x_count):
        for j in range(masspoints_y_count):
            dist0 = masspoints[i, j]
            T[i, j] = T_calc(masspoints[i, j], elements[i, j], l0, k)
            F = T[i, j] - [0, 0, 3]
            dist[i, j] = F2dist(F, m, v0, dist0, dt)

    masspoints = dist
    masspoints = masspoints_constraints(masspoints, masspoints_constraints_index, masspoints_constraints_value)
    elements = masspoint2element(masspoints, boundaryx, boundaryy)
    if _ % 5 == 0:
        im = ax.plot(dist[:,:,0].flatten(), dist[:,:,2].flatten(), dist[:,:,1].flatten(), marker="o", c='k', linestyle='None')
        artists.append(im)
    print(_)

ani = animation.ArtistAnimation(fig, artists, interval=100)
#ani.save('kusa.gif', writer="pillow")
plt.show()