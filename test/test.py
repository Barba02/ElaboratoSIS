#!/usr/lib/python3

import random
import subprocess as sp


# data una stringa
# restituisce la stessa stringa con gli spazi tra ogni caratteri
def spaziatore(string):
    tmp = "".join(string[i] + " " for i in range(len(string)-1))
    return tmp + string[len(string)-1]


# dato un numero intero decimale
# restituisce la codifica binaria in modulo a 8 bit
def dec_to_bin_m(n):
    string = ""
    while n != 0:
        string = str(n % 2) + string
        n = int(n / 2)
    while len(string) != 8:
        string = "0" + string
    return string


# dato un numero intero decimale
# restituisce la codifica binaria in fixed point 4.4 bit
def dec_to_bin_fp(n):
    string = ""
    i = int(n)
    d = n - i
    while i > 0:
        string = str(i % 2) + string
        i = int(i / 2)
    while len(string) != 4:
        string = "0" + string
    while d not in [1, 0]:
        string += str(int(d * 2))
        d *= 2
        if d > 1.0:
            d -= 1
    while len(string) != 8:
        string += "0"
    return string


# dato un numero binario in fixed point 4.4 bit
# restituisce il corrispondente binario
def bin_to_dec(string):
    n = 0
    esp = 3
    for i in range(8):
        n += int(string[i]) * pow(2, esp)
        esp -= 1
    return n


def file_print(f, p, n):
    global eo
    eo.write(f"{f} {spaziatore(dec_to_bin_fp(p))} {spaziatore(dec_to_bin_m(n))}\n")


# funzione che rappresenta lo stato di erogazione della soluzione acida e le sue transizioni
def eroga_acido():
    global ph, registro_ph, registro_nclk, rst, start, state
    # se rst è alzato si torna allo stato iniziale con tutti gli output a 0
    if rst == "1":
        state = "reset"
        registro_ph = ph
        file_print("0 0 0 0", 0, 0)
    # altrimenti si acidifica la soluzione di partenza di 0.5 e si aumenta il contatore
    else:
        registro_ph -= 0.5
        registro_nclk += 1
        # se il ph è neutro si passa allo stato di fine
        if registro_ph <= 8:
            state = "fine"
            file_print("1 0 0 0", registro_ph, registro_nclk)
        else:
            file_print("0 0 1 0", registro_ph, registro_nclk)


# funzione che rappresenta lo stato di erogazione della soluzione basica e le sue transizioni
def eroga_base():
    global ph, registro_ph, registro_nclk, rst, start, state
    # se rst è alzato si torna allo stato iniziale con tutti gli output a 0
    if rst == "1":
        state = "reset"
        registro_ph = ph
        file_print("0 0 0 0", 0, 0)
    # altrimenti si alcalinizza la soluzione di partenza di 0.25 e si aumenta il contatore
    else:
        registro_ph += 0.25
        registro_nclk += 1
        # se il ph è neutro si passa allo stato di fine
        if registro_ph >= 7:
            state = "fine"
            file_print("1 0 0 0", registro_ph, registro_nclk)
        else:
            file_print("0 0 0 1", registro_ph, registro_nclk)


# funzione che rappresenta lo stato finale e le sue transizioni 
def fine():
    global ph, registro_ph, registro_nclk, rst, start, state
    # se rst è alzato si torna allo stato iniziale con tutti gli output a 0
    if rst == "1":
        state = "reset"
        registro_ph = ph
        file_print("0 0 0 0", 0, 0)
    # altrimenti in uscita si mantiene alto il bit di fine e si stampano ph e nclk finali 
    else:
        file_print("1 0 0 0", registro_ph, registro_nclk)


# funzione che rappresenta lo stato di input errato e le sue transizioni 
def errore():
    global ph, registro_ph, registro_nclk, rst, start, state
    # se rst è alzato si torna allo stato iniziale con tutti gli output a 0
    if rst == "1":
        state = "reset"
        file_print("0 0 0 0", 0, 0)
    # altrimenti in uscita si mantiene alto il bit di errore e si stampano ph e nclk
    else:
        file_print("0 1 0 0", ph, 0)
    registro_ph = ph


# funzione che rappresenta lo stato iniziale e le sue transizioni
def reset():
    global ph, registro_ph, registro_nclk, rst, start, state
    # si azzera il conteggio dei cicli di clock
    registro_nclk = 0
    # se rst è alzato si torna allo stato iniziale con tutti gli output a 0
    if rst == "1":
        file_print("0 0 0 0", 0, 0)
    # nel caso rst sia abbassato
    else:
        # se start è basso rimango nello stato e stampo il ph dato in input e nclk
        if start == "0":
            file_print("0 0 0 0", ph, 0)
        # se start è alto inizia il calcolo
        else:
            # se il ph in input è maggiore di 14 si va nello stato di errore con il relativo bit alzato e stampo il
            # ph dato in input e nclk
            if ph > 14:
                state = "errore"
                file_print("0 1 0 0", ph, 0)
            # se il ph è valido
            else:
                # nel caso sia già neutro passo allo stato di fine alzando corrispettivo bit e mettendo in output il
                # ph dato con nclk
                if 7 <= ph <= 8:
                    state = "fine"
                    file_print("1 0 0 0", ph, registro_nclk)
                # altrimenti
                else:
                    # se la soluzione è acida, inizio ad erogare soluzione basica e alzo il bit della corrispondente
                    # valvola, stampando ph e nclk
                    if ph < 7:
                        state = "eroga_base"
                        file_print("0 0 0 1", ph, registro_nclk)
                    # se la soluzione è basica, inizio ad erogare soluzione acida e alzo il bit della corrispondente
                    # valvola, stampando ph e nclk
                    else:
                        state = "eroga_acido"
                        file_print("0 0 1 0", ph, registro_nclk)
    registro_ph = ph


# funzione che genera una stringa di 10 bit casuali per l'input
def genera_input():
    tmp = ""
    for _ in range(10):
        tmp += str(random.randrange(2))
    return tmp


# funzione che svolge la routine stampare gli input sul file e richiamare le funzioni dello stato attuale
def loop():
    global ph, registro_ph, registro_nclk, rst, start, state, user_input, eo, inputs
    inputs.write("sim " + spaziatore(user_input) + "\n")
    rst = user_input[0]
    start = user_input[1]
    ph = bin_to_dec(user_input[2:])
    eval(state + "()")
    user_input = genera_input()


if __name__ == "__main__":
    tot = 0
    for _ in range(64):
        # inizializzazione del datapath
        ph = 0
        registro_ph = 0
        registro_nclk = 0
        # inizializzazione della fsm
        rst = 0
        start = 0
        state = "reset"
        with open("expected_outputs.txt", "w") as eo, open("inputs.txt", "w") as inputs:
            inputs.write("read_blif \"../min_fsmd.blif\"\n")
            # inizio della routine
            user_input = genera_input()
            for _ in range(1024):
                loop()
            loop()
            # chiusura routine e chiusura del file con i comandi per sis
            inputs.write("quit\n")
        # lettura degli input da dare a sis
        with open("inputs.txt", "r") as inputs:
            ss = inputs.read().split("\n")
        # creazione sottoprocesso di sis
        process = sp.Popen(["sis"], stdin=sp.PIPE, stdout=sp.PIPE, text=True)
        # esecuzione di ogni riga
        for line in ss:
            line += "\n"
            process.stdin.write(line)
        # recupero dell'output del sottoprocesso una volta terminato
        out = str(process.communicate()[0])
        with open("outputs.txt", "w") as outputs:
            # parsing e scrittura di tutti gli output di sis
            while "Outputs" in out:
                s = out[out.find("Outputs")+9:out.find("Outputs")+48] + "\n"
                out = out[out.find("Outputs")+48:]
                outputs.write(s)
        # lettura degli output di sis e di quelli aspettati
        with open("outputs.txt", "r") as actual, open("expected_outputs.txt", "r") as expected:
            # creazione degli array con gli output
            a = actual.read().split("\n")
            e = expected.read().split("\n")
        # conteggio dei test superati
        passed = 0
        for i in range(len(a)-1):
            if a[i] == e[i]:
                passed += 1
            else:
                print("row", i+1)
        # stampa percentuale di test superati
        passed = passed * 100 / (len(a) - 1)
        tot += passed
        print("{:.2f}%".format(passed))
    tot /= 64
    print("Media: {:.2f}%".format(tot))
