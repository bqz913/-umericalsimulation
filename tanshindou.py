import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
from IPython.display import HTML

# figure
fig = plt.figure()
ax = Axes3D(fig)
ax.set_xlim(1, 3)
ax.set_ylim(1, 3)
ax.set_zlim(-3, 3)

# 初期条件
j = np.array([[-1, 1, 0], [1, 1, 0], [-1, -1, 0], [1, -1, 0]])
i = np.array([0, 0, 3])
t = 0
k = 0.1
l0 = math.sqrt(2)
m = 1
v0 = 0
a = 0
dt = 0.05

# 計算
e = [0] * 4
T = [0] * 4
dxyz = []
ims = []
X, Y = np.meshgrid([1, 2, 3], [1, 2, 3])
Z = np.array([[0,0,0], [0,3,0], [0,0,0]])
artist = ax.plot_wireframe(X, Y, Z)
for _ in range(2000):
    for n in range(4):
        l = np.linalg.norm(j[n] - i)
        e[n] = (j[n]-i)/l
        T[n] = k*(l-l0)*e[n]
    a = (T[0]+T[1]+T[2]+T[3])/m
    v0 = v0 + a * dt
    i = i + v0*dt + (1/2)*a*(dt**2)
    dxyz.append(i)
    # X = [i[0], j[0][0], j[1][0], j[2][0], j[3][0]]
    # Y = [i[2], j[0][2], j[1][2], j[2][2], j[3][2]]
    # Z = [i[1], j[0][1], j[1][1], j[2][1], j[3][1]]
    Z = np.array([[0,0,0], [0,i[2],0], [0,0,0]])
    old_artist = artist
    artist = ax.plot_wireframe(X, Y, Z)
    ax.collections.remove(old_artist)
    plt.pause(0.01)
    #ims.append(artist)
    print(_)



#ani = animation.ArtistAnimation(
#      fig,  # Figureオブジェクト
#      ims,  # サブプロット(Axes)のリスト
#      interval=0.5,  # サブプロットの更新頻度(ms)
#      )
#ani.save('test.mp4', writer='ffmpeg',dpi=100)
#HTML(ani.to_html5_video())
#plt.plot(range(len(z)),z)
#print(ani)
#plt.show()