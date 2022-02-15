import os


toRemove = []
ai = "auto_increment.txt"
n = int(open(ai, "r").readline())
os.remove(ai)
for s in ["datapath", "fsm", "fsmd"]:
    for i in range(0, n):
        st = s + "_" + str(i) + "_stats.txt"
        cmd = s + "_" + str(i) + "_comandi.txt"
        if os.path.exists(st):
            with open(st, "r") as file:
                if file.read().find("lits") == -1:
                    toRemove.append(st)
                    toRemove.append(cmd)
        else:
            if os.path.exists(cmd):
                os.remove(cmd)
    for x in toRemove:
        if os.path.exists(x):
            os.remove(x)
