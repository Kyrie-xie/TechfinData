'''
@Editor: Jinxing
@Description:
    对数据的一些统计情况进行总结
'''

import pandas as pd
import numpy as np
from typing import List, Union


def na_locate(data: pd.DataFrame,
              **kwargs) -> np.array:
    '''
    返回缺失值在数据中的位置 （row，col）

    Args:
        data: 数据

    Returns:
        缺失值的位置 in numpy.array
    '''
    x = np.array(kwargs.get('data_na') or data.isna())
    return np.argwhere(x)


def na_col(data: pd.DataFrame,
           show_all: bool = True,
           **kwargs) -> pd.Series:
    '''
    返回（所给的）col中存在多少缺失值

    Args:
        data: df
        show_all: 时候展示所有（考虑到有数据集过大）

    Returns:
        pd.Series
    '''
    if show_all:
        pd.set_option('display.max_columns', None)
    if 'data_na' in kwargs:
        return kwargs.get('data_na').sum(0).to_frame().T
    else:
        return data.isna().sum(0).to_frame().T


def na_total(data,
             **kwargs):
    if 'data_na' in kwargs:
        return kwargs.get('data_na').sum().sum()
    else:
        return data.isna().sum().sum()


def stock_count_by_date(data: pd.DataFrame,
                        by_list: bool = True,
                        index_name: str = 'trade_date',
                        **kwargs) -> Union[pd.Series, List[int]]:
    '''
    返回时间versus股票数目，查看股票数量在时序上的变化

    Args:
        data: df
        by_list: yes - 返回list
                 no  - 返回pd.Series, 保留时间数据
        index_name: 作为x轴的index的名字

    Returns:
        在时间上的股票数的pd.series or list
    '''
    try:
        _p = (kwargs.get('index_names') or data.index.names).index(index_name)
        res = data.apply(lambda x: 1, axis=1).groupby(data.index.get_level_values(_p)).sum()
        return res if not by_list else list(res)
    except:
        raise KeyError('没有该index')


def na_info(data: pd.DataFrame,
            by_array: bool = True,
            index_name: str = 'trade_date',
            **kwargs) -> Union[np.array, pd.DataFrame]:
    '''
    返回在y天时，因子x上的缺失值数量的array或者dataframe

    Args:
        data: dataframe
        by_array: yes: return with array
                  no:  return pd.DataFrame
        index_name: 满足未来的不同的数据集的需要

    Returns:
        array or pd.df
    '''
    try:
        _p = (kwargs.get('index_names') or data.index.names).index(index_name)
        data_na = kwargs.get('data_na') or data.isna()
        data_na = data_na.groupby(data_na.index.get_level_values(_p)).sum()
        return np.array(data_na) if by_array else data_na
    except:
        raise KeyError('没有该index')


