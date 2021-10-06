'''
@Editor: Jinxing
@Description:
'''
import pandas as pd
from typing import List, Tuple, Optional, Union
from TechfinDataAPI.pandas_methods.extraction import group_by_index_name

class KeywordFirst:
    '''
    将某个keyword的index置顶，其他的顺移
    '''

    def __init__(self,
                 keyword: str = None):
        '''

        Args:
            keyword: 置顶的index_name,或者包含有index name中的关键词
        '''
        self.keyword = keyword or 'time'

    def __call__(self,
                 data: pd.DataFrame,
                 inplace: bool = False
                 ) -> Optional[pd.DataFrame]:
        '''
        输入data返回新的置顶后的dataset

        Args:
            data: df
            inplace: 是否在原有数据上进行改动

        Returns:
            可能是inplace也可能是新的数据集
        '''

        level_names = list(data.index.names)
        if self.keyword in level_names[0]:
            return data
        for i, name in enumerate(level_names):
            if self.keyword in name:
                rank = [r for r in range(len(level_names))]
                rank.pop(i)
                rank = [i] + rank
                if not inplace:
                    return data.reorder_levels(rank)
                else:
                    data = data.reorder_levels(rank)
        print('关键词不存在在数据的index中')
        return data


def date_first(data):
    '''
    特制的Keywordfirst
    '''
    return KeywordFirst('date')(data)

def level_swap(data: pd.DataFrame,
               index: Union[list[int], tuple[int]]) -> None:
    '''
    交换a,b两个index的level (Inplace)

    Args:
        data: 数据
        index: 【a: int ,b: int】

    Returns: None
    '''
    if len(index) != 2:
        raise Exception('目前只支持两个index间的操作')
    try:
        data = data.swaplevel(*index)
    except:
        raise Exception('index和dataframe不匹配')


def date_mean_fill(data) -> None:
    '''
    使用date mean来填充缺失值

    Args:
        data: df

    Returns:
        None
    '''
    data.fillna(value=group_by_index_name(data, 'trade_date').mean(), inplace=True)


def hist_fill(data: pd.DataFrame,
              method: str = 'ffill'
              ) -> None:
    '''
    使用往期的数据来对因子进行填充 (Inplace)

    Args:
        data: df
        method: 和pandas的fillna method一致

    Returns:
        None
    '''
    temp = data.sort_values(by=['stock_code', 'trade_date']).fillna(method=method)
    data.fillna(value=temp, inplace=True)

