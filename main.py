from time import time, sleep


class DecorTimeCrit:
    def __init__(self, critical_time):
        self.critical_time = critical_time

    def benchmark(self, method):
        def helper(*args, **kwargs):
            time_start = time()

            res = method(*args, **kwargs)
            difference=time()-time_start
            if difference>self.critical_time:
                print(f'Warning! {method.__name__} slow. Time = {difference} sec.')
            else:
                pass
            return res

        return helper

    def __call__(self, cls):
        def helper(*args, **kwargs):
            for attr in dir(cls):
                #check if attribute is magic method or not
                if attr.startswith('__'):
                    continue

                method = getattr(cls, attr)
                # check if attribute is variable or method
                if callable(method):
                    decor_attr = self.benchmark(method)
                    setattr(cls, attr, decor_attr)
            #returning class with changed attributes
            return cls(*args, **kwargs)

        return helper




@DecorTimeCrit(critical_time=0.45)
class Test:
    def method_1(self):
        print('slow method start')
        sleep(1)
        print('slow method finish')

    def method_2(self):
        print('fast method start')
        sleep(0.1)
        print('fast method finish')






t = Test()

t.method_1()
t.method_2()

