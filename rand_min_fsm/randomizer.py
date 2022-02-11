import sys
import random
import subprocess as sp
from os.path import exists


# statistiche riferimento min_datapath.blif
min_nodes = 9
min_lits = 52
# lista dei comandi di sis per la sintesi
commands = ["source script.rugged", "eliminate -1", "sweep", "fx", "resub", "simplify", "full_simplify", "collapse",
            "reduce_depth", "espresso"]
# lettura/creazione e aggiornamento dell'indice del test
if exists("auto_increment.txt"):
    with open("auto_increment.txt", "r") as ai:
        pk = int(ai.readline())
else:
    pk = 0
with open("auto_increment.txt", "w") as ai:
    ai.write(str(pk+1))
# inizio sottoprocesso
assign_algo = str(sys.argv[1])
process = sp.Popen(["sis"], stdin=sp.PIPE, stdout=sp.PIPE, text=True)
with open(str(pk) + "_comandi.txt", "w") as comandi:
    comandi.write("state_assign " + assign_algo + "\n")
    process.stdin.write("read_blif fsm.blif\n")
    process.stdin.write("state_minimize\n")
    process.stdin.write("state_assign " + assign_algo + "\n")
    process.stdin.write("stg_to_network\n")
    process.stdin.write("print_stats\n")
    # esecuzione di n comandi con relativa scrittura, n parametro da terminale
    for _ in range(int(sys.argv[2])):
        cmd = commands[random.randrange(10)]
        comandi.write(cmd + "\n")
        process.stdin.write(cmd + "\n")
        process.stdin.write("print_stats\n")
    process.stdin.write("quit\n")
# recupero output sottoprocesso
lines = str(process.communicate()[0]).split("sis> sis> ")
lines.pop(0)
lines.pop(0)
# stampa delle statistiche
with open(str(pk) + "_stats.txt", "w") as stats:
    for line in lines:
        nodes = int(line[line.find("nodes")+6:line.find("latches")])
        lits = int(line[line.find("lits")+10:line.find("#states")])
        stats.write(str(nodes) + " " + str(lits))
        # evidenziazione di statitistiche valide
        if nodes <= min_nodes:
            min_nodes = nodes
            stats.write("\t\t\tless nodes")
        if lits <= min_lits:
            min_lits = lits
            stats.write("   less lits")
        stats.write("\n")
