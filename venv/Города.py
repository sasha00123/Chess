N = int(input())
a = set()
for i in range(N):
    a.add(input())
    x = input()
if x in a:
    print('TRY ANOTHER')
else:
    print('OK')