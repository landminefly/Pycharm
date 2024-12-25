#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import pymysql

a = [5, 62, 72, 66, 3, 32, 12, 8, 35, 83, 6, 18]


def bubble_sort(arr):
    for i in range(len(arr) - 1):
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                temp = arr[j + 1]
                arr[j + 1] = arr[j]
                arr[j] = temp


print(a)
bubble_sort(a)
print(a)


def reverse(a, b):
    return b, a


tup = c, d = reverse(1, 2)
print(tup, c, d)
print(type(tup), type(c), type(d))
print(isinstance(tup, (float, tuple)))

# (a, b) = (12, 34)
# c, d = 12, 34

a = ("a", "b", "c")
b = (111, 222, 333)
c = zip(a, b)
print(dict(c))

a = b, c = 1, 2
print(type(a))
print(type(b))
print(type(c))

print(sys.path)

f = open("text.txt", "a")
f.write("111")
# f是否关闭
print(f.closed)
f.close()

with open("text.txt", "a") as file:
    file.write("222")
print(file.closed)


# 数据库

# conn = pymysql.connect(host = 'localhost01', user = 'root', password = '073412', database = 'dbtest2')
# cursor = conn.cursor()
# user = input("please input user:")
# passwd = input("please input password:")
# cursor.execute("SELECT user,passwd FROM test2 WHERE user = %s AND passwd = %s", (user,passwd))
# data = cursor.fetchall()
# print(data)
# cursor.close()
# conn.close()

# with pymysql.connect(host = 'localhost01', user = 'root', password = '073412', database = 'dbtest2') as conn:
#     cursor = conn.cursor()
#
#     # 二者皆可
#     user = 'bella'
#     passwd = '34567'
#     cursor.execute("INSERT INTO test2 VALUES (%s, %s)", (user, passwd))
#
#     value = ('aileen', '45678')
#     cursor.execute("INSERT INTO test2 VALUES %s", (value,))
#     conn.commit()


##########################################################################################################
##########################################################################################################

class A:
    # 像这种直接声明的一般都是类数据属性，与所有实例共享
    name = 'NAME'
    value = 127

    def __init__(self):
        # 实例数据属性一般不会直接声明，而是在 创建实例调用__init__时 或 创建实例后调用实例中的某个方法时，
        # 使用 self.新的实例数据属性名 直接进行赋值，就会创建相应的实例数据属性
        # 每个实例拥有各自的实例数据属性，不会互相干扰
        self.ins_name = 'INS_NAME'
        self.ins_value = 255

    # 可以直接通过类调用，第一个形参要求是cls，表示当前类
    @classmethod
    def method_a(cls):
        print("method_a")

    # 可以直接通过类调用，不存在cls形参
    @staticmethod
    def method_b():
        print("method_b")

    # 第一个形参要求是self，表示当前实例，因此要通过实例调用
    def method_c(self):
        print("method_c")


a = A()
a.method_a()
a.method_b()
a.method_c()

# 在类中修改类数据属性时，会同时修改其所有实例的对应类数据属性
# 除非实例先主动将其更改，在此之后该实例的该类数据属性不会再跟随类改变
a.name = 'CHANGED1'
print(a.name)
print(A.name)

A.name = 'CHANGED2'
print(a.name)
print(A.name)

##########################################################################################################
##########################################################################################################

string = "this is string example....wow!!! this is really string";
print(string.replace("is", "was"))
print(string.replace("is", "was", 4))


class Data:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __lt__(self, other):
        if self.age < other.age:
            return True
        else:
            return False

    def __repr__(self):
        return str((self.name, self.age))


d1 = Data('bella', 20)
d2 = Data('diana', 18)
d3 = Data('eileen', 23)
d4 = Data('ava', 19)

li = [d1, d2, d3, d4]

print(sorted(li))


##########################################################################################################
##########################################################################################################

# python 并不存在完全的类私有变量，因此需要遵守一个约定：如果某个变量名以下划线（_）开头，那它理应是一个私有变量，不应在类外使用
# 但是 python 提供了类私有变量的有限实现：
# 1.对于只有一个下划线开头的变量，虽然它被认为是私有的，但仍可在类外直接使用其变量名直接访问
# 2.而对于这种形式 __spam 的变量名（至少带有两个前缀下划线，至多一个后缀下划线），
#   如果想要在类外访问，就要使用 _classname__spam，其中 classname 为去除了前缀下划线的当前类名称。
#   这种改写不考虑标识符的句法位置，只要它出现在类定义内部就会进行
class B:
    __arg1 = 1
    _arg2 = 2

    def __init__(self, value):
        self.__arg3 = value

    def __method1(self):
        print("method1")

    def _method2(self):
        print("method2")


b = B(3)
print(b._B__arg3)
print(b._B__arg1)
print(b._arg2)

b._B__method1()
b._method2()

##########################################################################################################
##########################################################################################################
