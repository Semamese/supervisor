import numpy as np

def find_circle_center(A, B, C):
    """
    计算通过三点 A, B, C 的外接圆圆心
    :param A: (x1, y1)
    :param B: (x2, y2)
    :param C: (x3, y3)
    :return: (xc, yc) 圆心坐标
    """
    x1, y1 = A
    x2, y2 = B
    x3, y3 = C

    # 计算两个中点
    M1 = ((x1 + x2) / 2, (y1 + y2) / 2)
    M2 = ((x2 + x3) / 2, (y2 + y3) / 2)

    # 计算垂直方向斜率
    if x2 - x1 == 0:  # 竖直线情况
        slope_AB = None
    else:
        slope_AB = (y2 - y1) / (x2 - x1)

    if x3 - x2 == 0:  # 竖直线情况
        slope_BC = None
    else:
        slope_BC = (y3 - y2) / (x3 - x2)

    # 计算中垂线斜率（垂直于 AB 和 BC）
    if slope_AB is None:  # AB 竖直
        slope_perp_AB = 0
    elif slope_AB == 0:  # AB 水平
        slope_perp_AB = None
    else:
        slope_perp_AB = -1 / slope_AB

    if slope_BC is None:  # BC 竖直
        slope_perp_BC = 0
    elif slope_BC == 0:  # BC 水平
        slope_perp_BC = None
    else:
        slope_perp_BC = -1 / slope_BC

    # 计算两条中垂线的交点
    if slope_perp_AB is None:  # 第一条垂直
        xc = M1[0]
        yc = slope_perp_BC * (xc - M2[0]) + M2[1]
    elif slope_perp_BC is None:  # 第二条垂直
        xc = M2[0]
        yc = slope_perp_AB * (xc - M1[0]) + M1[1]
    else:
        # 解 y - M1_y = slope_perp_AB * (x - M1_x)
        # 和 y - M2_y = slope_perp_BC * (x - M2_x)
        A = np.array([
            [-slope_perp_AB, 1],
            [-slope_perp_BC, 1]
        ])
        b = np.array([
            M1[1] - slope_perp_AB * M1[0],
            M2[1] - slope_perp_BC * M2[0]
        ])
        xc, yc = np.linalg.solve(A, b)

    return xc, yc

