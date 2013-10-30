# -*- coding:utf-8 -*-
import os.path
import subprocess
import sys


def fib(n):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fibonacci')
    p = subprocess.Popen([path, str(n)])
    p.wait()


if __name__ == '__main__':
    n = int(sys.argv[1])
    fib(n)
