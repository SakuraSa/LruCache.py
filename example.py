#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    Author:cleverdeng
    E-mail:clverdeng@gmail.com
"""

#time cost check helper
from time import time

class Timer(object):
    def __init__(self, print_cost=False, formatter="time cost: %(cost).3fs"):
        object.__init__(self)
        self.print_cost = print_cost
        self.formatter  = formatter
        self.running    = False
        self.begain     = None
        self.end        = None
        self.cost       = None

    def __enter__(self):
        self.running = True
        self.begain  = time()
        return self

    def __exit__(self, *args):
        self.running = False
        self.end     = time()
        self.cost    = self.end - self.begain
        if self.print_cost:
            print self.formatter % {
                'begain': self.begain,
                'end': self.end,
                'cost': self.cost
            }


#example
from lru import CachedFunction


def fibonacci(n):
    if n <= 2:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


@CachedFunction()
def fibonacci_cached(n):
    if n <= 2:
        return 1
    else:
        return fibonacci_cached(n - 1) + fibonacci_cached(n - 2)

if __name__ == '__main__':
    scale = 35
    print "begain testing with scale %d ..." % scale
    with Timer(True, "normal time cost: %(cost).3fs") as timer0:
        print fibonacci(scale)
    with Timer(True, "cached time cost: %(cost).3fs") as timer1:
        print fibonacci_cached(scale)
    print "time cost is 1 / %d" % int(timer0.cost / timer1.cost)