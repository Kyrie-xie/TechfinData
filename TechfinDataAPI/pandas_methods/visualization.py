'''
@Editor: Jinxing
@Description:
    基于另一个summary模块里面的代码，对数据的一些统计情况进行可视化
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Union
import seaborn as sns
from TechfinDataAPI.pandas_methods.summary import (na_info, stock_count_by_date, )


def na_factor_plot(data: pd.DataFrame,
                   num: int = 5,
                   fig_size_=(15, 15),
                   **kwargs) -> None:
    '''
    plot缺失值最多的k个因子在时序下的缺失值变化

    Args:
        data: df
        num: 展示的因子数
        fig_size_: 图像尺寸

    Returns:
        None
    '''
    na_array = na_info(data, True, **kwargs)
    num = min(data.shape[1], num)
    stock_number = stock_count_by_date(data, by_list=False, **kwargs)
    plt.figure(figsize=fig_size_)
    plt.plot(np.arange(na_array.shape[0]), stock_number)
    for i, factor in enumerate(na_array[:, na_array.sum(0).argsort()[-num:]].T):
        plt.plot(np.arange(na_array.shape[0]), factor)
    plt.legend(['Stock_num'])
    plt.xlabel('time')
    plt.ylabel('number')


def na_factor_time_plot(data: pd.DataFrame,
                        fig_size: Union[Tuple[int],List[int]] = (50, 50),
                        **kwargs) -> None:
    '''
    在y天，因子x的缺失值plot

    Args:
        data: df
        is_na: 是否已经在展示na的状态下
        fig_size: 图像的大小

    Returns:
        None
    '''
    plt.figure(figsize=fig_size)
    na_array1 = na_info(data, by_array=True, **kwargs)
    plt.imshow(na_array1)
    plt.colorbar(orientation='vertical')
    plt.xlabel('factor')
    plt.ylabel('time')
    plt.show()


def cov_heatmap(data: pd.DataFrame,
                _self: bool = False,
                **kwargs) -> None:
    '''
    因子间的covariance plot

    Args:
        data: df
        variance: 是否展示自身（可能会导致颜色不明显）

    Returns:
        None
    '''
    sns.set()
    plt.figure(figsize = (25,25))
    temp = data.cov().to_numpy()
    if _self != True:
        temp[np.arange(len(temp)), np.arange(len(temp))] = 0
    sns.heatmap(temp)


def corr_heatmap(data: pd.DataFrame,
              self_: bool = False,
                 **kwargs) -> None:
    '''
    因子间的covariance plot

    Args:
        data: df
        variance: 是否展示自身（可能会导致颜色不明显）

    Returns:
        None
    '''
    sns.set()
    plt.figure(figsize = (25,25))
    temp = data.corr().to_numpy()
    if self_ != True:
        temp[np.arange(len(temp)), np.arange(len(temp))] = 0
    ax = sns.heatmap(temp)


