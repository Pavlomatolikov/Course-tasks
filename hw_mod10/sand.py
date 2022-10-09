def a(b, c=1, **kwargs):
    print(b)
    print(c)
    for i in kwargs.values():
        print(i)


test = a(c=44, d=88, b=33)
