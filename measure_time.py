# -*- coding:utf-8 -*-
"""
Usage
=====
$ time python measure_time.py N

Setup
=====
$ gcc fibonacci.c -o fibonacci
"""

import os
import time
import resource
import sys
import os.path
import subprocess
import fibonacci


def show_time_info():
    os_times = os.times()
    time_clock = time.clock()
    time_time = time.time()
    resource_self = resource.getrusage(resource.RUSAGE_SELF)
    resource_children = resource.getrusage(resource.RUSAGE_CHILDREN)

    print('os.times() = {0}'.format(os_times))
    print('time.clock() = {0}'.format(time_clock))
    print('time.time() = {0}'.format(time_time))
    print('resource.getrusage(resource.RUSAGE_SELF).ru_utime = {0}'.format(resource_self.ru_utime))
    print('resource.getrusage(resource.RUSAGE_SELF).ru_stime = {0}'.format(resource_self.ru_stime))
    print('resource.getrusage(resource.RUSAGE_CHILDREN).ru_utime = {0}'.format(resource_children.ru_utime))
    print('resource.getrusage(resource.RUSAGE_CHILDREN).ru_stime = {0}'.format(resource_children.ru_stime))

    return [os_times,
            time_clock,
            time_time,
            resource_self,
            resource_children]


def show_time_delta(end, start):
    os_times_delta = tuple([e - s for e, s in zip(end[0], start[0])])
    time_clock_delta = end[1] - start[1]
    time_time_delta = end[2] - start[2]
    resource_self_utime_delta = end[3].ru_utime - start[3].ru_utime
    resource_self_stime_delta = end[3].ru_stime - start[3].ru_stime
    resource_children_utime_delta = end[4].ru_utime - start[4].ru_utime
    resource_children_stime_delta = end[4].ru_stime - start[4].ru_stime

    print('Delta: os.times() = {0}'.format(os_times_delta))
    print('Delta: time.clock() = {0}'.format(time_clock_delta))
    print('Delta: time.time() = {0}'.format(time_time_delta))
    print('Delta: resource.getrusage(resource.RUSAGE_SELF).ru_utime = {0}'.format(resource_self_utime_delta))
    print('Delta: resource.getrusage(resource.RUSAGE_SELF).ru_stime = {0}'.format(resource_self_stime_delta))
    print('Delta: resource.getrusage(resource.RUSAGE_CHILDREN).ru_utime = {0}'.format(resource_children_utime_delta))
    print('Delta: resource.getrusage(resource.RUSAGE_CHILDREN).ru_stime = {0}'.format(resource_children_stime_delta))

    return (os_times_delta,
            time_clock_delta,
            time_time_delta,
            resource_self_utime_delta,
            resource_self_stime_delta,
            resource_children_utime_delta,
            resource_children_stime_delta)


def validation_os_times(
        os_times_delta,
        time_clock_delta,
        time_time_delta,
        resource_self_utime_delta,
        resource_self_stime_delta,
        resource_children_utime_delta,
        resource_children_stime_delta):
    print('Diff: os.times()[0], resource.getrusage(resource.RUSAGE_SELF).ru_utime = {0}'.format(
        abs(os_times_delta[0] - resource_self_utime_delta)))
    print('Diff: os.times()[1], resource.getrusage(resource.RUSAGE_SELF).ru_stime = {0}'.format(
        abs(os_times_delta[1] - resource_self_stime_delta)))
    print('Diff: os.times()[2], resource.getrusage(resource.RUSAGE_CHILDREN).ru_utime = {0}'.format(
        abs(os_times_delta[2] - resource_children_utime_delta)))
    print('Diff: os.times()[3], resource.getrusage(resource.RUSAGE_CHILDREN).ru_stime = {0}'.format(
        abs(os_times_delta[3] - resource_children_stime_delta)))
    print('Diff: os.times()[4], time.time() = {0}'.format(
        abs(os_times_delta[4] - time_time_delta)))
    print('Diff: os.times()[0], time.clock() = {0}'.format(
        abs(os_times_delta[0] - time_clock_delta)))


def check(func, title):
    print('#' * 80)
    print(title)
    print('#' * 80)
    start = show_time_info()
    func()
    print('-' * 80)
    end = show_time_info()
    print('-' * 80)
    deltas = show_time_delta(end, start)
    print('-' * 80)
    validation_os_times(*deltas)


def check_self_py():
    """
    現在のプロセスでフィボナッチを計算
    """
    def func():
        fibonacci.fib(35)
    check(func, 'check_self_py')


def check_subprocess_py():
    """
    子プロセス(Pythonプログラム)でフィボナッチを計算
    """
    def func():
        p = subprocess.Popen(['python', 'fibonacci.py', '35'])
        p.wait()
    check(func, 'check_subprocess_py')


def check_subprocess_c():
    """
    子プロセス(Cプログラム)でフィボナッチを計算
    """
    def func():
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fibonacci')
        p = subprocess.Popen([path, '40'])
        p.wait()
    check(func, 'check_subprocess_c')


def check_subsubprocess_py_c():
    """
    子プロセス(Pythonプログラム)のさらに子プロセス（Cプログラム）でフィボナッチを計算
    """
    def func():
        p = subprocess.Popen(['python', 'fibonacci_wrapper.py', '40'])
        p.wait()
    check(func, 'check_subsubprocess_py_c')


def check_sleep():
    """
    現在のプロセスでsleep
    """
    def func():
        time.sleep(3)
    check(func, 'check_sleep')


def measure_in_subprocess():
    """
    子プロセス(measure_time.py)で計測
    """
    for x in range(5):
        p = subprocess.Popen(['python', 'measure_time.py', str(x)])
        p.wait()


if __name__ == '__main__':
    x = int(sys.argv[1])
    if x == 0:
        check_self_py()
    elif x == 1:
        check_subprocess_py()
    elif x == 2:
        check_subprocess_c()
    elif x == 3:
        check_subsubprocess_py_c()
    elif x == 4:
        check_sleep()
    elif x == -1:
        measure_in_subprocess()
