#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

a = [[1, 2], 123, '''abc''']
a = a * 3
b = True and False
print(a, len(a), 123 in a, b, type(5 // 2))

# for i in a:
#     print(str(i) + "\n")

a = (1,)
print(a)

a = "Diana"
b = {a: 18}
print(b)

print("ab{}".format("111"))
print("ab%s" % "111")

print("""这是一个多行字符串的实例
多行字符串可以使用制表符
TAB ( \t )。
也可以使用换行符 [ \n ]。
""")

a = {"Diana": 18, "Bella": 19}
a.pop("Diana")
print("Diana" in a)

a = 1
if a:
    print("111")

a = {"a": 111}
print(type(a))
a.clear()
a = {}
print(type(a))

# string = input()
# print(string)

print(os.getcwd())

dic = {"diana": 18, "ava": 19, "bella": 20}
print(dic)
print(dic.items())
print(dic.keys())
print(dic.values())
