'''
@Editor: Jinxing
@Description:
    在pandas里面根据某些需求提取子区域
'''
import pandas as pd
import numpy as np
from typing import List, Union


############
# 子数据提取 #
############
def data_split(data: pd.DataFrame,
               fracs: Union[np.array, List[float]]) -> List[pd.DataFrame]:
    '''
    Description:
        将dataframe根据某种格式分解成多个子dataframe

    Args:
        data: 数据
        fracs: training, (validation), test set 的比例。
                e.g. [8,2] = 0.8 training, 0.2 test
                     [8,1,1] = 0.8 training, 0.1 val, 0.1 test

    Returns:
            于fracs占同样比例的子dataframe
    '''

    if type(fracs) != np.ndarray:
        fracs = np.array(fracs)
    fracs = fracs / sum(fracs)
    fracs = np.insert(fracs, 0, 0).cumsum()
    print(fracs)
    output = []
    m = data.shape[0]
    for i in range(len(fracs) - 1):
        output.append(data.iloc[int(fracs[i] * m): int(fracs[i + 1] * m)])
    return output


def col_generate(index: Union[List, int],
                 keyword: str) -> List[str]:
    '''
    生成对应的col names，用于批量生成'factor_i'

    Args:
        index: factor的代号list
        keyword: 默认‘factor_’， 可以输入自己dataset的关键词名进行生成

    Returns:
        keyword + str(x)
    '''

    if type(index) == int:
        return [keyword + str(index)]
    elif type(index) == list:
        return [keyword + str(i) for i in index]
    else:
        raise Exception('需要是数字或者是数字组成的list')


def col_remove(data: pd.DataFrame,
               cols: List[str]):
    '''
    去除某些col

    Args:
        data: dataframe
        cols: col names

    Return: None
    '''
    data.drop(columns=cols, inplace=True)


def group_by_index_name(data: pd.DataFrame,
                        index_name: str):
    '''
    在指定的index上进行的group wrapping

    Args:
        data: dataframe
        index_name: 例如‘trade_date',数据中的一个index名字

    Returns:
        以inde_name为单位的group wrappings
    '''

    if index_name not in data.index.names:
        raise Exception('没有这个index')
    position = list(data.index.names).index(index_name)
    temp = data.groupby(data.index.get_level_values(position))
    return temp


def index_norm(data: pd.DataFrame,
               index_name: str = 'trade_date') -> pd.DataFrame:
    '''
    在每日截面数据的基础上进行标准化操作，不支持inplace操作，所以需要重新对数据赋值

    Args:
        data: dataframe
        index_name: 默认 trade_date，如果未来数据index名字有改动可以进行调整

    Returns:
        标准化后的数据
    '''
    data = data.groupby(index_name).transform(lambda x: (x - x.mean()) / (x.std(ddof=1) + 1e-5))
    return data


def keyword_extract(data: pd.DataFrame,
                    keyword: str,
                    index: Union[int, str] = 0) -> pd.DataFrame:
    '''
    在某个index上，提取出含有keyword（可以是list）的dataframe rows

    Args:
        data: dataframe
        keyword: 你想要提取的关键词（例如股票名字，或者某一日期）
        index: index的level或者名字

    Returns:
        提取后的df
    '''

    if type(index) != int:
        # 名字输入
        index = data.index.names.index(index)

    def func(_input,
             _index,
             _keyword):
        if _input[_index] in _keyword:
            return True
        else:
            return False

    return data[list(map(lambda x: func(x, index, keyword), data.index))]


def after_date(data: pd.DataFrame,
               date: str,
               index_name: str = 'trade_date') -> pd.DataFrame:
    '''
    # 在时序上提取出在after_date上的数据

    Args：
        data: dataframe
        after_date：新数据的所有日期都会在这一天之后
        index_name: 默认为trade_date， 如果未来数据有变可以单独设置

    Returns:
        新的数据集
    '''
    position = data.index.names.index(index_name)
    a = np.unique(data.index.get_level_values(position))
    return data.loc[a[a > date]]


def random_sample(data: pd.DataFrame,
                  frac: float,
                  index_name: str = 'stock_code',
                  ) -> pd.DataFrame:
    '''
    在给的index上的提取frac比例sample

    Args:
        data: dataframe
        frac: 抽取的比例
        index_name: index名字

    Returns:
         新的数据
    '''
    if frac >= 1:
        raise Exception('请重新检查输入的比例')
    position = data.index.names.index(index_name)
    stock_name_ = np.unique(data.index.get_level_values(position))
    random_stock_ = np.random.choice(stock_name_, int(frac * len(stock_name_)), replace=False)
    return keyword_extract(data, random_stock_, position, )

