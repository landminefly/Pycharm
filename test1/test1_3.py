#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
# from test1_1.test1_1_1 import _method1, __method2, _A
from enum import Enum
import traceback
import re

print(sys.path)

# 与类的私有变量类似，python也有模块私有变量的约定：
# 如果某个变量名以下划线（_）开头，那它理应是一个私有变量，不应在模块外使用
# 但是 python 却没有提供模块私有变量的任何实现，
# 也就是说，被认为是私有的变量，仍能正常访问，全靠程序员自觉

# _method1()
# __method2()
# print(_A._arg1)

# 如果仅仅是想在函数中访问全局变量，而并不对其进行赋值或修改
# 那么可以直接输入变量名访问，解释器会一层层往外找的
a = 10


def test1():
    print(a)


test1()


# 如果想在函数中访问并修改全局变量，那就必须先使用global关键字显式声明该全局变量
def test2():
    global a
    a = a + 1
    print(a)


test2()
print(a)

GD = Enum('GD', ('GZ', 'QY', 'SZ'))
for item in GD.__members__.items():
    print(item)
li = [item[0] for item in GD.__members__.items() if item[0] == 'QY']
print(li)


class GD(Enum):
    GZ = '广州'
    QY = '清远'
    SZ = '深圳'


ite = iter(GD)
n = 0
while True:
    try:
        print(next(ite))
    except StopIteration:
        # 使用以下方式打印异常
        traceback.print_exc()
        break
    else:
        n += 1
        print("迭代{}次".format(n))


class A:
    pass


print(A.__class__.__class__.__class__.__class__.__class__.__class__.__class__)

##########################################################################################################
##########################################################################################################

a = '<img src="https://abc.jpg">'

# 使用 re.search，它返回的不是字符串，而是一个对象
# 使用 group() 转为字符串，或者 span() 转为匹配子串在原串中的下标
search = re.search('<img (src)="(.*)">', a)
# group(0) 是一个完整的匹配子串，group(1)表示第一个分组，以此类推
# <img src="https://abc.jpg">
print(search.group(0))
# src
print(search.group(1))
# https://abc.jpg
print(search.group(2))
# 元组，('src', 'https://abc.jpg')
print(search.group(1, 2))
# 元组，('src', 'https://abc.jpg')
print(search.groups())

# 使用 re.findall，它貌似只会返回所有匹配子串中的分组而不是完整的匹配子串，除非匹配子串没有分组
findall = re.findall('<img (src)="(.*)">', a)
# [('src', 'https://abc.jpg')]
print(findall)
findall = re.findall('<img src=".*">', a)
# ['<img src="https://abc.jpg">']
print(findall)

# 使用 re.sub
b = '111-222-333'
b1 = re.sub('-', '_', b, 1)
print(b1)  # 111_222-333


# value表示一个匹配子串，类似于re.search的返回结果，它不是字符串，而是一个对象
# 使用 group() 转为字符串，或者 span() 转为匹配子串在原串中的下标
def exchange(value):
    if value.group() == '_':
        return '*'
    if value.group() == '-':
        return '%'


# 第二个参数（即表示替换内容的参数）可以是一个函数
b2 = re.sub('-|_', exchange, b1)
print(b2)  # 111*222%333

# ?在正则的其他作用：转换为懒惰模式
string = "123abc"
# ?在任何量词 *、 +、? 或 {} 后面缺省，则默认为贪婪模式，匹配尽可能多的字符
result = re.search("\d+", string)
print(result.group(0))  # "123"
# ?写在任何量词 *、 +、? 或 {} 后面，表示懒惰模式，匹配尽可能少的字符
result = re.search("\d+?", string)
print(result.group(0))  # "1"


##########################################################################################################
##########################################################################################################

# 将属性名全部改为大写
class MetaB(type):
    def __new__(mcs, name, parents, attrs):
        attrs_name = [name for name in attrs.keys() if not name.startswith('__')]
        upper_attrs_name = [name.upper() for name in attrs_name]
        for i in range(len(attrs_name)):
            if attrs_name[i] in attrs:
                value = attrs[attrs_name[i]]
                del attrs[attrs_name[i]]
                attrs[upper_attrs_name[i]] = value
        return super().__new__(mcs, name, parents, attrs)


class B(metaclass = MetaB):
    attr_one = 1
    attr_two = 2

    @staticmethod
    def method_one():
        print("method_one")


print(B.ATTR_ONE)
print(B.ATTR_TWO)
B.METHOD_ONE()


class A:
    def __init__(self, i=100):
        self.i = i
class B(A):
    def __init__(self, j=0):
        self.j = j


b = B()
print(b.i)
print(b.j)
