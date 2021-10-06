'''
@Editor: Jinxing
@Description: 负责文件的读取
'''
import pickle
from typing import Any

def pkl_reader(file_path:str) -> Any:
    '''
    description：
        读取pkl类数据
    '''
    # load : get the data from file
    data = pickle.load(open(file_path, "rb"))
    # loads : get the data from var
    #     data = pickle.load(var)
    return data


