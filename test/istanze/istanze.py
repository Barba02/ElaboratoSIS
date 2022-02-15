import os
import subprocess as sp

test_success = []
os.mkdir("output")
for i in range(1, 8):
    # lettura degli input
    ss = ["read_blif \"../../min_fsmd.blif\""]
    with open(f"input/{i}.txt", "r") as inputs:
        for s in inputs.read().split("\n"):
            ss.append("sim " + s)
    ss.append("quit")
    # esecuzione sis
    process = sp.Popen(["sis"], stdin=sp.PIPE, stdout=sp.PIPE, text=True)
    for line in ss:
        line += "\n"
        process.stdin.write(line)
    # recupero, parsing e scrittura output
    out = str(process.communicate()[0])
    with open(f"output/{i}.txt", "w") as outputs:
        # parsing e scrittura di tutti gli output di sis
        while "Outputs" in out:
            s = out[out.find("Outputs")+9:out.find("Outputs")+48] + "\n"
            out = out[out.find("Outputs")+48:]
            outputs.write(s)
    # confronto output aspettati con attuali
    with open(f"output/{i}.txt", "r") as actual, open(f"expected_output/{i}.txt", "r") as expected:
        a = actual.read().split("\n")
        e = expected.read().split("\n")
    passed = 0
    for j in range(len(e)):
        if a[j] == e[j]:
            passed += 1
    test_success.append(passed * 100 / len(e))
    print(f"Test {i}: ", end="")
    print("{:.2f}%".format(test_success[i-1]))
# stampa condizioni rispettate
print("PH ACIDO\t", end="")
if test_success[0] == 100 or test_success[1] == 100:
    print("OK")
else:
    print("-")
print("PH BASICO\t", end="")
if test_success[2] == 100 or test_success[3] == 100:
    print("OK")
else:
    print("-")
print("PH NEUTRO\t", end="")
if test_success[5] == 100 or test_success[6] == 100:
    print("OK")
else:
    print("-")
print("ERRORE\t\t", end="")
if test_success[4] == 100:
    print("OK")
else:
    print("-")
