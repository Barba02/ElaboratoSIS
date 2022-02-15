import os

list = []
for i in range(1, 116):
    with open(str(i) + "_stats.txt", "r") as file:
        if file.read().find("lits") != -1:
            print(i)
        else:
            list.append(i)
for x in list:
    os.remove(str(x) + "_stats.txt")
    os.remove(str(x) + "_comandi.txt")
