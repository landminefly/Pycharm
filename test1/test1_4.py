class A:
    def __init__(self, i=100):
        self.i = i


class B(A):
    def __init__(self, j=0):
        self.j = j


b = B()
# print(b.i)
print(b.j)