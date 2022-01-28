import random


def spaziatore(s):
    tmp = ""
    for i in range(7):
        tmp += s[i] + " "
    return tmp + s[7]


def dec_to_bin_m(n):
    s = ""
    while n != 0:
        s = str(n % 2) + s
        n = int(n / 2)
    while len(s) != 8:
        s = "0" + s
    return s


def dec_to_bin_fp(n):
    s = ""
    i = int(n)
    d = n - i
    while i > 0:
        s = str(i % 2) + s
        i = int(i / 2)
    while len(s) != 4:
        s = "0" + s
    while d != 1 and d != 0:
        s += str(int(d * 2))
        d *= 2
        if d > 1.0:
            d -= 1
    while len(s) != 8:
        s += "0"
    return s


def bin_to_dec(s):
    n = 0
    e = 3
    for i in range(8):
        n += int(s[i]) * pow(2, e)
        e -= 1
    return n


def eroga_acido():
    global state, rst, start, ph, nclk
    if rst == "1":
        state = "ph_iniziale"
        print("0 " * 19 + "0")
    else:
        ph -= 0.5
        nclk += 1
        if ph <= 8:
            state = "fine"
            print(f"1 0 0 0 {spaziatore(dec_to_bin_fp(ph))} {spaziatore(dec_to_bin_m(nclk))}")
        else:
            print(f"0 0 1 0 {spaziatore(dec_to_bin_fp(ph))} {spaziatore(dec_to_bin_m(nclk))}")


def eroga_base():
    global state, rst, start, ph, nclk
    if rst == "1":
        state = "ph_iniziale"
        print("0 " * 19 + "0")
    else:
        ph += 0.25
        nclk += 1
        if ph >= 7:
            state = "fine"
            print(f"1 0 0 0 {spaziatore(dec_to_bin_fp(ph))} {spaziatore(dec_to_bin_m(nclk))}")
        else:
            print(f"0 0 0 1 {spaziatore(dec_to_bin_fp(ph))} {spaziatore(dec_to_bin_m(nclk))}")


def fine():
    global state, rst, start, ph, nclk
    if rst == "1":
        state = "ph_iniziale"
        print("0 " * 19 + "0")
    else:
        print(f"1 0 0 0 {spaziatore(dec_to_bin_fp(ph))} {spaziatore(dec_to_bin_m(nclk))}")


def errore():
    global state, rst, start, ph, nclk
    if rst == "1":
        state = "ph_iniziale"
        print("0 " * 19 + "0")
    else:
        print(f"0 1 0 0 {spaziatore(dec_to_bin_fp(ph))} {spaziatore(dec_to_bin_m(nclk))}")


def ph_iniziale():
    global state, rst, start, ph, nclk
    nclk = 0
    if rst == "1":
        print("0 " * 19 + "0")
    else:
        if start == "0":
            print(f"0 0 0 0 {spaziatore(dec_to_bin_fp(ph))} {spaziatore(dec_to_bin_m(nclk))}")
        else:
            if ph > 14:
                state = "errore"
                print(f"0 1 0 0 {spaziatore(dec_to_bin_fp(ph))} {spaziatore(dec_to_bin_m(nclk))}")
            else:
                if 7 <= ph <= 8:
                    state = "fine"
                    print(f"1 0 0 0 {spaziatore(dec_to_bin_fp(ph))} {spaziatore(dec_to_bin_m(nclk))}")
                else:
                    if ph < 7:
                        state = "eroga_base"
                        print(f"0 0 0 1 {spaziatore(dec_to_bin_fp(ph))} {spaziatore(dec_to_bin_m(nclk))}")
                    else:
                        state = "eroga_acido"
                        print(f"0 0 1 0 {spaziatore(dec_to_bin_fp(ph))} {spaziatore(dec_to_bin_m(nclk))}")


def genera_input():
    s = ""
    for _ in range(10):
        s += str(random.randrange(2))
    return s


def loop():
    global state, rst, start, ph, nclk, user_input
    print("\n" + state + " " + user_input)
    rst = user_input[0]
    start = user_input[1]
    if state == "ph_iniziale":
        ph = bin_to_dec(user_input[2:])
    eval(state + "()")
    user_input = genera_input()


if __name__ == "__main__":
    ph = 0
    nclk = 0
    state = "ph_iniziale"
    user_input = genera_input()
    while state != "fine":
        loop()
    loop()
