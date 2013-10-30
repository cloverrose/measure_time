# -*- coding:utf-8 -*-
import sys

def fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib(n - 2) + fib(n - 1)


if __name__ == '__main__':
    n = int(sys.argv[1])
    fib(n)
