#!/usr/bin/python3

import random
import subprocess as sp

# data una stringa
# restituisce la stessa stringa con gli spazi tra ogni caratteri
def spaziatore(s):
    tmp = "".join(s[i] + " " for i in range(len(s)-1))
    return tmp + s[len(s)-1]


# dato un numero intero decimale
# restituisce la codifica binaria in modulo a 8 bit
def dec_to_bin_m(n):
    s = ""
    while n != 0:
        s = str(n % 2) + s
        n = int(n / 2)
    while len(s) != 8:
        s = "0" + s
    return s


# dato un numero intero decimale
# restituisce la codifica binaria in fixed point 4.4 bit
def dec_to_bin_fp(n):
    s = ""
    i = int(n)
    d = n - i
    while i > 0:
        s = str(i % 2) + s
        i //= 2
    while len(s) != 4:
        s = "0" + s
    while d not in [1, 0]:
        s += str(int(d * 2))
        d *= 2
        if d > 1.0:
            d -= 1
    while len(s) != 8:
        s += "0"
    return s


# dato un numero binario in fixed point 4.4 bit
# restituisce il corrispondente binario
def bin_to_dec(s):
    n = 0
    e = 3
    for i in range(8):
        n += int(s[i]) * pow(2, e)
        e -= 1
    return n


# funzione che rappresenta lo stato di erogazione della soluzione acida e le sue transizioni
def eroga_acido():
    global state, rst, start, ph, nclk, eo
    # se rst è alzato si torna allo stato iniziale con tutti gli output a 0
    if rst == "1":
        state = "ph_iniziale"
        eo.write("0 " * 19 + "0\n")
    # altrimenti si alcalinizza la soluzione di partenza di 0.5 e si aumenta il contatore
    else:
        ph -= 0.5
        nclk += 1
        # se il ph è neutro si passa allo stato di fine alzando il corrispettivo bit
        if ph <= 8:
            state = "fine"
            eo.write(f"1 0 0 0 {spaziatore(dec_to_bin_fp(ph))} {spaziatore(dec_to_bin_m(nclk))}\n")
        # altrimenti rimane nello stesso stato con il corrispettivo bit alzato
        else:
            eo.write(f"0 0 1 0 {spaziatore(dec_to_bin_fp(ph))} {spaziatore(dec_to_bin_m(nclk))}\n")
        # in entrambi i casi si stampano gli attuali ph e nclk


# funzione che rappresenta lo stato di erogazione della soluzione basica e le sue transizioni
def eroga_base():
    global state, rst, start, ph, nclk, eo
    # se rst è alzato si torna allo stato iniziale con tutti gli output a 0
    if rst == "1":
        state = "ph_iniziale"
        eo.write("0 " * 19 + "0\n")
    # altrimenti si acidifica la soluzione di partenza di 0.25 e si aumenta il contatore
    else:
        ph += 0.25
        nclk += 1
        # se il ph è neutro si passa allo stato di fine alzando il corrispettivo bit
        if ph >= 7:
            state = "fine"
            eo.write(f"1 0 0 0 {spaziatore(dec_to_bin_fp(ph))} {spaziatore(dec_to_bin_m(nclk))}\n")
        # altrimenti rimane nello stesso stato con il corrispettivo bit alzato
        else:
            eo.write(f"0 0 0 1 {spaziatore(dec_to_bin_fp(ph))} {spaziatore(dec_to_bin_m(nclk))}\n")
        # in entrambi i casi si stampano gli attuali ph e nclk


# funzione che rappresenta lo stato finale e le sue transizioni 
def fine():
    global state, rst, start, ph, nclk, eo
    # se rst è alzato si torna allo stato iniziale con tutti gli output a 0
    if rst == "1":
        state = "ph_iniziale"
        eo.write("0 " * 19 + "0\n")
    # altrimenti in uscita si mantiene alto il bit di fine e si stampano ph e nclk finali 
    else:
        eo.write(f"1 0 0 0 {spaziatore(dec_to_bin_fp(ph))} {spaziatore(dec_to_bin_m(nclk))}\n")


# funzione che rappresenta lo stato di input errato e le sue transizioni 
def errore():
    global state, rst, start, ph, nclk, eo
    # se rst è alzato si torna allo stato iniziale con tutti gli output a 0
    if rst == "1":
        state = "ph_iniziale"
        eo.write("0 " * 19 + "0\n")
    # altrimenti in uscita si mantiene alto il bit di errore e si stampano ph e nclk attuali 
    else:
        eo.write(f"0 1 0 0 {spaziatore(dec_to_bin_fp(ph))} {spaziatore(dec_to_bin_m(nclk))}\n")


# funzione che rappresenta lo stato iniziale e le sue transizioni
def ph_iniziale():
    global state, rst, start, ph, nclk, eo
    # se rst è alzato si torna allo stato iniziale con tutti gli output a 0
    if rst == "1":
        eo.write("0 " * 19 + "0\n")
    else:
        # si azzera il conteggio dei cicli di clock
        nclk = 0
        # se start è basso rimango nello stato e stampo il ph dato in input e nclk (0)
        if start == "0":
            eo.write(f"0 0 0 0 {spaziatore(dec_to_bin_fp(ph))} {spaziatore(dec_to_bin_m(nclk))}\n")
        elif ph > 14:
            state = "errore"
            eo.write(f"0 1 0 0 {spaziatore(dec_to_bin_fp(ph))} {spaziatore(dec_to_bin_m(nclk))}\n")
        elif 7 <= ph <= 8:
            state = "fine"
            eo.write(f"1 0 0 0 {spaziatore(dec_to_bin_fp(ph))} {spaziatore(dec_to_bin_m(nclk))}\n")
        elif ph < 7:
            state = "eroga_base"
            eo.write(f"0 0 0 1 {spaziatore(dec_to_bin_fp(ph))} {spaziatore(dec_to_bin_m(nclk))}\n")
        else:
            state = "eroga_acido"
            eo.write(f"0 0 1 0 {spaziatore(dec_to_bin_fp(ph))} {spaziatore(dec_to_bin_m(nclk))}\n")


# funzione che genera una stringa di 10 bit casuali per l'input
def genera_input():
    return "".join(str(random.randrange(2)) for _ in range(10))


# funzione che svolge la routine stampare gli input sul file e richiamare le funzioni dello stato attuale
def loop():
    global state, rst, start, ph, nclk, user_input, inputs
    inputs.write("sim " + spaziatore(user_input) + "\n")
    rst = user_input[0]
    start = user_input[1]
    # il ph viene considerato dalla fsm solo nello stato iniziale
    if state == "ph_iniziale":
        ph = bin_to_dec(user_input[2:])
    eval(state + "()")
    user_input = genera_input()


if __name__ == "__main__":
    # inizializzazione del datapath con i registri a 0
    ph = 0
    nclk = 0
    # inizializzazione della fsm nello stato iniziale
    state = "ph_iniziale"
    with open("expected_outputs.txt", "w") as eo:
        with open("inputs.txt", "w") as inputs:
            inputs.write("read_blif fsmd.blif\n")
            # inizio della routine
            user_input = genera_input()
            while state != "fine":
                loop()
            loop()
            # chiusura routine e chiusura del file con i comandi per sis
            inputs.write("quit\n")
    with open("inputs.txt", "r") as inputs:
        ss = inputs.read().split("\n")
    # creazione sottoprocesso di sis
    process = sp.Popen(["sis"], stdin=sp.PIPE, stdout=sp.PIPE, text=True)
    # esecuzione di ogni riga
    for line in ss:
        line += "\n"
        process.stdin.write(line)
    # recupero dell'output del sottoprocesso una volta terminato
    ss = str(process.communicate()[0])
    with open("outputs.txt", "w") as outputs:
        # parsing e scrittura di tutti gli output di sis
        while "Outputs" in ss:
            s = ss[ss.find("Outputs")+9:ss.find("Outputs")+48] + "\n"
            ss = ss[ss.find("Outputs")+48:]
            outputs.write(s)
    with open("outputs.txt", "r") as actual:
        expected = open("expected_outputs.txt", "r")
        # creazione degli array con gli output
        a = actual.read().split("\n")
        e = expected.read().split("\n")
    expected.close()
    # conteggio dei test
    passed = sum(a[i] == e[i] for i in range(len(a)-1))
    # stampa percentuale di test superati
    passed = passed * 100 / (len(a) - 1)
    print("{:.2f}%".format(passed))
