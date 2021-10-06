'''
@Editor: Jinxing
@Description:
    一些装饰器
'''
import functools, time


def time_consumption(func):
    '''
    装饰器：
        在结束func后print所用的时间
    '''
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - t0 #用时
        name = func.__name__
        arg_lst = []
        if args:
            arg_lst.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            pairs = ['%s=%r'%(k,w) for k, w in sorted(kwargs.items())]
            arg_lst.append(', '.join(pairs))
        arg_str = ', '.join(arg_lst)
        print('[using time: {}s]\t {}({})'.format(elapsed, name, arg_str))
        return result
    return clocked







if __name__ == '__main__':
    # Example
    @time_consumption
    def s(x,y):
        return x+y
    print( s(x = 3,y=4))