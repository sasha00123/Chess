a = set()
b = set()
x = str(input())
while x != '':
    a.add(x)
    x = str(input())
    y = str(input())
while y != '':
    b.add(y)
    y = str(input())
intersection = a        & b
if len(intersection) == 0:
    print('EMPTY')
else:
    while intersection:
        for i in intersection:
            print(i)