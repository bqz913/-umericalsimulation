import numpy as np

def masspoint2element(masspoints, boundaryx, boundaryy):
    """ 連結されている質点を算出

    引数:
        masspoints:2次元配列。masspoints[X座標の要素数,
                                        Y座標の要素数,
                                        x:0、y:1、z:2]
        boundaryx:x座標の最小値・最大値[最小値, 最大値]
        boundaryy:y座標の最小値・最大値[最小値, 最大値]
    返り値:
        elements:4次元のarray。elements[masspointに対応する位置,
                                        masspointに対応する位置,
                                        連結されてる質点(基本サイズは4だが、4個ない場合NaNで埋めている),
                                        x:0, y:1, z:2]
    """
    elements = np.zeros([int(boundaryx[1] - boundaryx[0] + 1), int(boundaryy[1] - boundaryy[0]) + 1, 4, 3])
    for i in range(elements.shape[0]):
        for j in range(elements.shape[1]):
            if i > 0:
                elements[i, j, 0] = masspoints[i - 1, j]
            else:
                elements[i, j, 0] = None
            if i < elements.shape[0] - 1:
                elements[i, j, 1] = masspoints[i + 1, j]
            else:
                elements[i, j, 1] = None
            if j > 0:
                elements[i, j, 2] = masspoints[i, j - 1]
            else:
                elements[i, j, 2] = None
            if j < elements.shape[1] - 1:
                elements[i, j, 3] = masspoints[i, j + 1]
            else:
                elements[i, j, 3] = None

    return elements

def T_calc(masspoint, elements_masspoint, l0, k):
    """ 質点にかかる張力を算出

    引数：
        masspoint:質点。x:0、y:0、z:0
        elements_masspoint:masspointに連結されている質点[質点数,
                                                        x:0、y:0、z:0]
        l0:自然長
        k:ばね定数
    返り値：
        T:masspointにかかる張力[x:0、y:1、z:2]
    """
    not_nan_bool = np.all(~np.isnan(elements_masspoint), axis=1)
    n = np.count_nonzero(not_nan_bool)
    T_one = [[0, 0, 0]] * n
    for element, i in zip(elements_masspoint[not_nan_bool], range(n)):
        vector = element - masspoint
        length = np.linalg.norm(vector)
        #print(f"length={length}")
        vector_unit = vector / length
        length_diff = length - l0
        if length_diff < 0:
            T_one[i] = 0
        else:
            T_one[i] = k * length_diff * vector_unit
    T = np.sum(T_one, axis=0)
    return T

def F2dist(F, m, v0, dist0, dt):
    """運動方程式を用い、dt(s)後の力F(N)から変位dist(m)を求める

    引数:
        F:masspointにかかる力[x:0、y:1、z:2]
        m:masspointの質量
        v0:初速度(m/s)[x:0、y:1、z:2]]
        dist0:初位置(m)[x:0、y:1、z:2]]
        dt:計算ステップ区切り(s)
    返り値:
        dist:変位[x:0、y:1、z:2]
    """
    a = F / m
    v = v0 + a * dt
    dist = dist0 + v * dt
    return dist

def masspoints_constraints(masspoints, masspoints_constraints_index, masspoints_constraints_value):
    """拘束条件を付ける

    引数:
        masspoints:全ての質点
        masspoints_constraints_index:拘束条件を与える質点のインデックス
        masspoints_constraints_value:拘束条件を与えるXYZ座標
    返り値:
        masspoints:拘束条件によって矯正された質点
    """
    for i, j in zip(masspoints_constraints_index, masspoints_constraints_value):
        masspoints[i[0], i[1]] = j
        masspoints[i[0], i[1]] = j
        masspoints[i[0], i[1]] = j
        masspoints[i[0], i[1]] = j

    return masspoints