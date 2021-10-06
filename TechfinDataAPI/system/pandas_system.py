'''
@Editor: Jinxing
@Description:
'''
from TechfinDataAPI.pandas_methods import *
from copy import deepcopy
from typing import Union, Callable


# 一个对(时间，股票)*因子的pandas.dataFrame进行数据预处理的系统
class PdSys:
    def __init__(self,
                 data: Union[pd.DataFrame, str],
                 reader: Callable[[str], pd.DataFrame] = None,
                 func_intro: bool = True) -> None:
        """
        :param data: 需要被处理的数据或者途径
        :param reader: 读取器
        :param func_intro: 是否展示功能的介绍（推荐打开）

        :return None
        """

        if reader != None:
            self.df_ = reader(data)
        else:
            self.df_ = data

        print('录入数据完毕')

        # 日期优先：
        self.df_ = date_first(self.df_)

        print('################################################ \n ')

        self.index = self.df_.index
        self.backup_ = []
        self.backUp('Raw dataset')
        if func_intro:
            print('################################################ \n ')
            print('备份完成： 使用 .recover()还原')


    def show_col(self,
                 num: int = None):
        pd.set_option('display.max_columns', num)

    def show_row(self,
                 num: int = None):
        pd.set_option('display.max_rows', num)

    def na_col(self):
        return na_col(self.df_)

    def group_by_index_name(self,
                index_name: str,
                function: str = 'mean',
                inplace: bool = False):

        temp = group_by_index_name(self.df_, index_name)
        if function == 'mean':
            temp = temp.mean()
        elif function == 'sum':
            temp = temp.sum()
        elif function == 'var':
            temp = temp.var()
        else:
            print('目前的方程只支持sum， mean， var')

        if inplace:
            self.df_ = temp
        else:
            return temp

    def na_info(self):
        na_info(self.df_)

    def na_factor_plot(self,
                  num: int = 50,
                  figSize: tuple = (15, 15)):
        na_factor_plot(self.df_, num, figSize)

    def na_total(self):
        print(na_total(self.df_))


    def na_factor_time_plot(self):
        na_factor_time_plot(self.df_)

    def drop_col(self,
                cols: List[str]):
        col_remove(self.df_,
                  cols)

    def baseFill(self,
                 method,
                 sub_method):
        print('Before the fillna:')
        self.na_total()
        method(self.df_, method=sub_method)
        print('After the fillna')
        self.na_total()
        return self.na_col()

    def date_mean_fill(self, ):
        self.baseFill(date_mean_fill, 'mean')

    def histFill(self,
                 method='ffill'):
        self.baseFill(hist_fill, sub_method='ffill')

    def backUp_note(self):
        for i, ele in enumerate(self.backup_):
            print('#{}: {} \n'.format(i, ele[1]))

    def backUp(self,
               note: str = 'No Record',
               remove_last=False):
        self.backup_.append([deepcopy(self.df_), note])
        print('backUp finishes')
        if remove_last:
            if len(self.backup_) > 1:
                self.backUp_remove(-2)

    def recover(self,
                i=-1):
        self.df_ = deepcopy(self.backup_[-1][0])
        print('已恢复到第{}号模型'.format(i))

    def backUp_remove(self,
                     i: int = -1):
        #         if type(i)!= int or i<0 or i > len(self.backup_)-1:
        #             raise Error('正整数且在列表内。使用.backUp_note()查看')
        self.backup_.pop(i)

    def cov_heatmap(self):
        cov_heatmap(self.df_)

    def corr_heatmap(self):
        corr_heatmap(self.df_)

    def keyword_extract(self,
                   keyword: str,
                   index: Union[str, int] = 0):
        return keyword_extract(self.df_, keyword, index)

    def date_norm(self,
                  index_name: str = 'trade_date'):
        self.df_ = index_norm(self.df_,
                              index_name = index_name)
        print('按照每日数据完成了normalization')

    def after_date(self,
                  date: str,
                  index_name: str='trade_date',
                  inplace: bool = True):
        if inplace:
            self.df_ = after_date(self.df_, date, index_name)
            print('提取完毕')
        else:
            return after_date(self.df_, date, index_name)

    def code_sample(self,
                    frac: float,
                    keyword: str = 'stock_code',
                    inplace: bool = True,
                   ):
        if inplace:
            self.df_ = random_sample(self.df_,
                                    frac=frac,
                                    index_name=keyword
                                    )
        else:
            return random_sample(self.df_,
                                 frac=frac,
                                 index_name=keyword
                                 )

    def __call__(self):
        return self.df_

    def __len__(self):
        # date的天数
        return len(np.unique(self.df_.index.get_level_values(0)))

    def __getitem__(self, date: str) -> Union[pd.DataFrame, pd.Series]:
        # 直接提取某一天的数据
        return self.df_.loc[date]


