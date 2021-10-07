'''
@Editor: Jinxing
@Description:
'''
import time
from collections import defaultdict
class a:
    dic = defaultdict(None)

    def __getitem__(self, key):
        return self.dic[key]

    def __setitem__(self, key, value):
        self.dic[key] = value

    def a(self,x):
        return x+1

def test(**kwargs):
    print(str('c' in kwargs))
    a = getattr(kwargs, 'a', 3)
    b = getattr(kwargs, 'b', 4)
    kwargs['c'] = 3

    return a + b


if __name__ == '__main__':
    # Content
    start = time.time()
    d = {'b':3}
    d['a'] = 100
    print(test())
    print(test())
    print('Time Consumption: {}'.format(time.time() - start))
