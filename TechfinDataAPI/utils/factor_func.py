'''
@Editor: Jinxing
@Description:
'''
import pandas as pd
import numpy as np


def Schimidt(df: pd.DataFrame,
             factor_list: list):
    '''
    输入dataframe和希望消除相关性的变量list
    '''

    factors1 = df[factor_list]
    col_name = factors1.columns
    factors1 = factors1.values

    R = np.zeros((factors1.shape[1], factors1.shape[1]))
    Q = np.zeros(factors1.shape)
    for k in range(0, factors1.shape[1]):
        R[k, k] = np.sqrt(np.dot(factors1[:, k], factors1[:, k]))
        Q[:, k] = factors1[:, k] / R[k, k]
        for j in range(k + 1, factors1.shape[1]):
            R[k, j] = np.dot(Q[:, k], factors1[:, j])
            factors1[:, j] = factors1[:, j] - R[k, j] * Q[:, k]

    Q = pd.DataFrame(Q, columns=col_name)
    return Q

