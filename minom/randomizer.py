import sys
import random
import subprocess as sp
from os.path import exists


blif = str(sys.argv[1])
# statistiche riferimento
if blif == "datapath":
    min_nodes = 44
    min_lits = 201
elif blif == "fsm":
    min_nodes = 11
    min_lits = 51
elif blif == "fsmd":
    min_nodes = 61
    min_lits = 245
else:
    exit(0)
# lista dei comandi di sis per la sintesi
commands = ["source script.rugged", "eliminate x", "sweep", "fx", "resub", "simplify", "full_simplify", "collapse",
            "reduce_depth", "espresso", "decomp", "invert", "invert_io"]
# lettura/creazione e aggiornamento dell'indice del test
if exists("auto_increment.txt"):
    with open("auto_increment.txt", "r") as ai:
        pk = int(ai.readline())
else:
    pk = 0
with open("auto_increment.txt", "w") as ai:
    ai.write(str(pk+1))
# inizio sottoprocesso
assign_algo = "jedi" if (random.random() % 2 == 0) else "nova"
process = sp.Popen(["sis"], stdin=sp.PIPE, stdout=sp.PIPE, text=True)
with open(blif + "_" + str(pk) + "_comandi.txt", "w") as comandi:
    process.stdin.write("read_blif full_" + blif + ".blif\n")
    if blif == "fsm":
        comandi.write("state_assign " + assign_algo + "\n")
        process.stdin.write("state_minimize\n")
        process.stdin.write("state_assign " + assign_algo + "\n")
        process.stdin.write("stg_to_network\n")
        process.stdin.write("print_stats\n")
    # esecuzione di n comandi con relativa scrittura, n parametro da terminale
    for _ in range(int(sys.argv[2])):
        cmd = commands[random.randrange(10)]
        # parametro di eliminate
        if cmd == "eliminate x":
            cmd = cmd.replace("x", str(random.randrange(-5, 6)))
        comandi.write(cmd + "\n")
        process.stdin.write(cmd + "\n")
        process.stdin.write("print_stats\n")
        # esecuzione di espresso dopo reduce_depth
        if cmd == "reduce_depth":
            cmd = "espresso"
            comandi.write(cmd + "\n")
            process.stdin.write(cmd + "\n")
            process.stdin.write("print_stats\n")
    process.stdin.write("quit\n")
# recupero output sottoprocesso
lines = str(process.communicate()[0]).split("sis> sis> ")
lines.pop(0)
if blif == "fsm":
    lines.pop(0)
# stampa delle statistiche
with open(blif + "_" + str(pk) + "_stats.txt", "w") as stats:
    for line in lines:
        nodes = int(line[line.find("nodes")+6:line.find("latches")])
        if blif == "fsm":
            lits = int(line[line.find("lits") + 10:line.find("#states")])
        else:
            lits = int(line[line.find("lits")+10:])
        stats.write(str(nodes) + " " + str(lits))
        # evidenziazione di statitistiche valide
        if nodes <= min_nodes:
            min_nodes = nodes
            stats.write("\t\t\tless nodes")
        if lits <= min_lits:
            min_lits = lits
            stats.write("   less lits")
        stats.write("\n")
