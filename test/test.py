import sys
import time
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
    global ph, next_state_ph, next_state_nclk, rst, state
    # se rst è alzato si torna allo stato iniziale con tutti gli output a 0
    if rst == "1":
        state = "reset"
        next_state_ph = ph
        file_print("0 0 0 0", 0, 0)
    # altrimenti si acidifica la soluzione di 0.5 e si aumenta il contatore
    else:
        next_state_ph -= 0.5
        next_state_nclk += 1
        # se il ph è neutro si passa allo stato di fine
        if next_state_ph <= 8:
            state = "fine"
        # altrimenti si prosegue l'erogazione
        file_print("0 0 1 0", 0, 0)


# funzione che rappresenta lo stato di erogazione della soluzione basica e le sue transizioni
def eroga_base():
    global ph, next_state_ph, next_state_nclk, rst, state
    # se rst è alzato si torna allo stato iniziale con tutti gli output a 0
    if rst == "1":
        state = "reset"
        next_state_ph = ph
        file_print("0 0 0 0", 0, 0)
    # altrimenti si alcalinizza la soluzione di 0.25 e si aumenta il contatore
    else:
        next_state_ph += 0.25
        next_state_nclk += 1
        # se il ph è neutro si passa allo stato di fine
        if next_state_ph >= 7:
            state = "fine"
        # altrimenti si prosegue l'erogazione
        file_print("0 0 0 1", 0, 0)


# funzione che rappresenta lo stato finale e le sue transizioni 
def fine():
    global ph, next_state_ph, next_state_nclk, rst, state
    # se rst è alzato si torna allo stato iniziale
    if rst == "1":
        state = "reset"
        next_state_ph = ph
        file_print("0 0 0 0", 0, 0)
    # altrimenti in uscita si mantiene alto il bit di fine e si stampano ph e nclk
    else:
        file_print("1 0 0 0", next_state_ph, next_state_nclk)


# funzione che rappresenta lo stato di input errato e le sue transizioni 
def errore():
    global ph, next_state_ph, rst, state
    # se rst è alzato si torna allo stato iniziale
    if rst == "1":
        state = "reset"
        file_print("0 0 0 0", 0, 0)
    # altrimenti in uscita si mantiene alto il bit di errore
    else:
        file_print("0 1 0 0", 0, 0)
    next_state_ph = ph


# funzione che rappresenta lo stato iniziale e le sue transizioni
def reset():
    global ph, next_state_ph, next_state_nclk, rst, start, state
    # si azzera il conteggio dei cicli di clock
    next_state_nclk = 0
    # se rst è alzato si resta nello stato iniziale
    if rst == "1":
        file_print("0 0 0 0", 0, 0)
    # nel caso rst sia abbassato
    else:
        # se start è basso rimango nello stato iniziale
        if start == "0":
            file_print("0 0 0 0", 0, 0)
        # se start è alto inizia il calcolo
        else:
            # se il ph in input è maggiore di 14 si va nello stato di errore con il relativo bit alzato
            if ph > 14:
                state = "errore"
                file_print("0 1 0 0", 0, 0)
            # se il ph è valido
            else:
                # nel caso sia già neutro passo allo stato di fine
                if 7 <= ph <= 8:
                    state = "fine"
                    file_print("0 0 0 0", 0, 0)
                # altrimenti
                else:
                    # se la soluzione è acida passo allo stato di eroga_base
                    if ph < 7:
                        state = "eroga_base"
                        file_print("0 0 0 0", 0, 0)
                    # se la soluzione è acida passo allo stato di eroga_acido
                    else:
                        state = "eroga_acido"
                        file_print("0 0 0 0", 0, 0)
    # faccio entrare il ph nel registro
    next_state_ph = ph


# funzione che genera una stringa di 10 bit casuali per l'input
def genera_input():
    global state
    tmp = ""
    for _ in range(10):
        tmp += str(random.randrange(2))
    # se non si è nello stato di reset, c'è 1/3 di possibilità che reset venga messo a 1
    if state != "reset":
        tmp = str(random.randrange(3) % 2) + tmp[1:]
    return tmp


# funzione che stampa gli input sul file e richiama le funzioni dello stato attuale
def loop():
    global ph, rst, start, state, user_input, inputs
    inputs.write("sim " + spaziatore(user_input) + "\n")
    rst = user_input[0]
    start = user_input[1]
    ph = bin_to_dec(user_input[2:])
    eval(state + "()")
    user_input = genera_input()


if __name__ == "__main__":
    # inizializzazione totale dei risultati
    tot = 0
    # input e controlli test
    test = int(sys.argv[1])
    if test < 1:
        test = 1
        print("Too few tests")
    # input e controlli input per test
    input_x_test = int(sys.argv[2])
    if input_x_test > 3410:
        input_x_test = 3410
        print("Too much inputs")
    elif input_x_test < 1:
        input_x_test = 1
        print("Too few inputs")
    # inizio dei testi
    print(f"Executing {test} tests over {input_x_test} inputs\n")
    duration = time.time()
    for i in range(test):
        # inizializzazione del datapath
        ph = 0
        next_state_ph = 0
        next_state_nclk = 0
        # inizializzazione della fsm
        rst = 0
        start = 0
        state = "reset"
        # apertura dei file con gli input da dare a sis e gli output aspettati
        with open("expected_outputs.txt", "w") as eo, open("inputs.txt", "w") as inputs:
            inputs.write("read_blif \"../min_fsmd.blif\"\n")
            # inizio del ciclo
            user_input = genera_input()
            for _ in range(input_x_test):
                loop()
            loop()
            # chiusura ciclo
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
        for j in range(input_x_test):
            if a[j] == e[j]:
                passed += 1
            else:
                print(f"(Test {i+1}) ERROR in line {j+1}")
        # stampa percentuale di test superati
        passed = passed * 100 / input_x_test
        tot += passed
        print(f"Test {i+1}: ", end="")
        print("{:.2f}%".format(passed))
    tot /= test
    print("\nAverage: {:.2f}%".format(tot))
    duration = time.time() - duration
    print("Duration: {:.2f} seconds".format(duration))
