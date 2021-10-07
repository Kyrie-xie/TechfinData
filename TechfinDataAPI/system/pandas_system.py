'''
@Editor: Jinxing
@Description:
    根据当前任务做的module
        比较符合 （date，stock）*factor数据
'''
from TechfinDataAPI.pandas_methods import *
from copy import deepcopy
from typing import Union, Callable


# 一个对(时间，股票)*因子的pandas.dataFrame进行数据预处理的系统
class PdSys:
    _property: dict = {}
    def __init__(self,
                 data: Union[pd.DataFrame, str],
                 reader: Optional[Callable[[str], pd.DataFrame]] = None,
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
        print('使用help（）来查看可用的命令')

    def start(self):
        self._property['index_names'] = self.df_.index.names
        self._property['data_na'] = self.df_.isna()
        temp = np.array(self.df_.index)
        for index_level, index_name in enumerate(self._property['index_names']):
            self._property[index_name] = np.unique(temp[:, index_level])

    def show_col(self,
                 num: int = None):
        pd.set_option('display.max_columns', num)

    def show_row(self,
                 num: int = None):
        pd.set_option('display.max_rows', num)

    def na_col(self):
        return na_col(self.df_)

    def group_function(self,
                index_name: str,
                function: str = 'mean',
                inplace: bool = False) -> Optional[pd.DataFrame]:
        """
        在指定的index上进行的group wrapping
        :param index_name: 例如‘trade_date',数据中的一个index名字
        :param function: mean, sum, var
        :param inplace: 定义新的数据为系统数据或者返回新的数据
        """

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
        """
        返回在y天时，因子x上的缺失值数量的array或者dataframe
        """
        na_info(self.df_)

    def na_factor_plot(self,
                  num: int = 50,
                  figSize: tuple = (15, 15)) ->None:
        """
        plot缺失值最多的num个因子在时序下的缺失值变化
        :param num: 展示的因子
        :param figSize: 图像大小
        """
        na_factor_plot(self.df_, num, figSize)

    def na_total(self):
        """
        nan的数目
        :return: nan的数目
        """
        print(na_total(self.df_))

    def na_factor_time_plot(self):
        """
        在y天，因子x的缺失值plot
        """
        na_factor_time_plot(self.df_)

    def drop_col(self,
                cols: List[str]) -> None:
        """
        去除某些col
        :param cols: 去除的col名字
        """
        col_remove(self.df_,
                  cols)

    def baseFill(self,
                 method,
                 sub_method):
        """
        一个关于填充的base （class），为inplace的 function
        :param method: 填充的办法， 为function
        :param sub_method: mean或者其他
        """
        print('Before the fillna:')
        self.na_total()
        method(self.df_, method=sub_method)
        print('After the fillna')
        self.na_total()
        return self.na_col()

    def date_mean_fill(self, ):
        """
        使用当天因子的mean来填充缺失值
        """
        self.baseFill(date_mean_fill, 'mean')

    def histFill(self,
                 method='ffill'):
        """
        使用往期一天的因子（同资产）进行填充
        :param method: 默认ffill
        :return: In-place
        """
        self.baseFill(hist_fill, sub_method='ffill')

    def backUp_note(self):
        """
        当前的备份信息进行打印
        """
        for i, ele in enumerate(self.backup_):
            print('#{}: {} \n'.format(i, ele[1]))

    def backUp(self,
               note: str = 'No Record',
               remove_last=False):
        """
        将当前的数据集备份
        :param note: 备份时候的备注
        :param remove_last: 是否替换掉上一个
        :return: None
        """
        self.backup_.append([deepcopy(self.df_), note])
        print('backUp finishes')
        if remove_last:
            if len(self.backup_) > 1:
                self.backUp_remove(-2)

    def recover(self,
                i: int=-1):
        """
        恢复第几个备份
        :param i:
        :return:
        """
        if i >= len(self.backup_) or i<0:
            raise Exception
        self.df_ = deepcopy(self.backup_[-1][0])
        print('已恢复到第{}号模型'.format(i))

    def backUp_remove(self,
                     i: int = -1):
        """
        移除第i个备份
        :param i:
        """
        self.backup_.pop(i)

    def cov_heatmap(self):
        """
        因子间的cov heatmap
        :return:
        """
        cov_heatmap(self.df_)

    def corr_heatmap(self):
        """
        因子间的corr heatmap
        :return:
        """
        corr_heatmap(self.df_)

    def keyword_extract(self,
                   keyword: str,
                   index: Union[str, int] = 0):
        """
        在index上提取出keyword的子数据集
        :param keyword:
        :param index:
        """
        return keyword_extract(self.df_, keyword, index)

    def date_norm(self,
                  index_name: str = 'trade_date'):
        """
        在当天做normalization
        :param index_name:
        """
        self.df_ = index_norm(self.df_,
                              index_name = index_name)
        print('按照每日数据完成了normalization')

    def after_date(self,
                  date: str,
                  index_name: str='trade_date',
                  inplace: bool = True):
        """
        只保留出在第date天之后的数据，可选是否inplace
        :param date:
        :param index_name:
        :param inplace:
        """
        if inplace:
            self.df_ = after_date(self.df_, date, index_name)
            print('提取完毕')
        else:
            return after_date(self.df_, date, index_name)

    def code_sample(self,
                    frac: float,
                    index_name: str = 'stock_code',
                    inplace: bool = True,
                   ):
        """
        随机在index上根选取出frac比例的股票,股票的出现和消失同市场保持一致
        :param frac:
        :param index_name:
        :param inplace:
        :return:
        """
        if inplace:
            self.df_ = random_sample(self.df_,
                                    frac=frac,
                                    index_name=index_name
                                    )
        else:
            return random_sample(self.df_,
                                 frac=frac,
                                 index_name=index_name
                                 )

    def __call__(self):
        return self.df_

    def __len__(self):
        """
        返回天数
        :return:
        """
        return len(np.unique(self.df_.index.get_level_values(0)))

    def __getitem__(self, date: str) -> Union[pd.DataFrame, pd.Series]:
        """
        提取日期数据
        :param date:输入你想要的日期
        :return:
        """
        return self.df_.loc[date]


