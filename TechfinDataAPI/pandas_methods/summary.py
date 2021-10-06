'''
@Editor: Jinxing
@Description:
    对数据的一些统计情况进行总结
'''

import pandas as pd
import numpy as np
from typing import List, Union


def na_locate(data: pd.DataFrame) -> np.array:
    '''
    返回缺失值在数据中的位置 （row，col）

    Args:
        data: 数据

    Returns:
        缺失值的位置 in numpy.array
    '''
    x = np.array(data.isna())
    return np.argwhere(x)


def na_col(data: pd.DataFrame,
           show_all: bool = True) -> pd.Series:
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
    return data.isna().sum(0).to_frame().T


def na_total(data):
    return data.isna().sum().sum()


def stock_count_by_date(data: pd.DataFrame,
                        by_list: bool = True,
                        index_name: str = 'trade_date') -> Union[pd.Series, List[int]]:
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
    if index_name not in data.index.names[0]:
        raise Exception('当前只支持标的在主index上的dataframe')
    res = data.apply(lambda x: 1, axis=1).groupby(data.index.get_level_values(0)).sum()
    return res if not by_list else list(res)


def na_info(data: pd.DataFrame,
            by_array: bool = True,
            index_name: str = 'trade_date') -> Union[np.array, pd.DataFrame]:
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
    if index_name not in data.index.names[0]:
        raise Exception('当前只支持标的在主index上的dataframe')
    data_na = data.isna()
    data_na = data_na.groupby(data_na.index.get_level_values(0)).sum()
    return np.array(data_na) if by_array else data_na

