count1 = int(input())

count2 = int(input())

list1 = []

for i in range(count1):

    list1.append(input())

list2 = []

for i in range(count2):

    list2.append(input())

result = ()

result = list(set(list1) - set(list2))

result = result + list(set(list2) - set(list1))

if len(result) == 0:

    print('NO')

else:

    print(len(result))