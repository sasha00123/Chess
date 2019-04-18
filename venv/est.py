def addFriends(name, frend):
    if name in dict_frend:
        dict_frend[name] = dict_frend[name] + frend
    else:
        dict_frend[name] = frend


def isFriends(name1, name2):
    print(name2 in dict_frend[name1])


def printFriends(name):
    print(*sorted(dict_frend[name]))


dict_frend = {}