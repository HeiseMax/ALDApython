import time

def ca_step(ca, rule):
    ca2 = ""
    i = 0
    while (i < len(ca)):

        if  i == 0 and ca[0:3] == "#o-": #für ping_pong
            ca2 = "#-o"
            i = 2

        elif i == (len(ca) -2) and ca[len(ca)-3:len(ca)] == "-o#": #für ping_pong
            ca2 = ca2[:-1] + "o-#"
            i = i +2

        elif i == 0:
            ca2 = ca2 + rule[" " + ca[i:i + 2]]

        elif i == len(ca) -1:
            ca2 = ca2 + rule[ca[i-1: i +1] + " "]

        else:
            ca2 = ca2 + rule[ca[i-1:i+2]]
        i = i +1

    return ca2

rule1 = {
    "   ": "*",
    "***": " ",
    "*  ": " ",
    " * ": "*",
    "  *": " ",
    "** ": "*",
    " **": "*",
    "* *": " "
}
rule2 = {
    "   ": " ",
    "***": "*",
    "*  ": "*",
    " * ": " ",
    "  *": " ",
    "** ": "*",
    " **": " ",
    "* *": " "
}
rule3 = {
    "   ": "*",
    "***": " ",
    "*  ": "*",
    " * ": "*",
    "  *": "*",
    "** ": " ",
    " **": " ",
    "* *": " "
}
rule4 = {
    "   ": "*",
    "***": "*",
    "*  ": "*",
    " * ": "*",
    "  *": "*",
    "** ": " ",
    " **": " ",
    "* *": "*"
}

def create_ca(): #erstellt den String im Anfangszustand
    ca = ""
    for n in range(0, 71):
        if n == 35:
            ca = ca + "*"
        else:
            ca = ca + " "
    return ca

def elementary1():
    ca = create_ca()
    print ("elementary1:")
    for t in range(0, 31):
        print("T", t, ":'{}'".format(ca))
        ca2 = ca_step(ca, rule1)
        ca = ca2

def elementary2():
    ca = create_ca()
    print("elementary2:")
    for t in range(0, 31):
        print("T", t, ":'{}'".format(ca))
        ca2 = ca_step(ca, rule2)
        ca = ca2

def elementary3():
    ca = create_ca()
    print("elementary3:")
    for t in range(0, 31):
        print("T", t, ":'{}'".format(ca))
        ca2 = ca_step(ca, rule3)
        ca = ca2

def elementary4():
    ca = create_ca()
    print("elementary4:")
    for t in range(0, 31):
        print("T", t, ":'{}'".format(ca))
        ca2 = ca_step(ca, rule4)
        ca = ca2

def run_all():
    elementary1()
    elementary2()
    elementary3()
    elementary4()

run_all() #Fuehrt alle Funktionen aus 2b aus!


'''
Aufgabe 2b
Wie viele verschiedene Regeln kann man daraus aufbauen?
    Es gibt 8 verschiedene Zustände von 3 nebeneinanderliegenden Zellen, jedem dieser Zustände kann man entweder " " oder "*" zuweisen.
    => 16 versschiedene Regeln möglich und 2^8 mögliche Regelsätze
'''

rule_ping_pong = {
    "o- ": " ",
    " o-": "-",
    "-o ": "-",
    " -o": " ",
    "-  ": " ",
    "  -": " ",
    "o  ": "o",
    "  o": "o",
    "#o-": "-",
    " #o": "#",
    "# o": "o",
    " #-": "#",
    "#-o": " ",
    "# -": " ",
    "-o#": "-",
    "o# ": "#",
    "o #": "o",
    "-# ": "#",
    "o-#": " ",
    "- #": " ",
    " # ": "#",
    "#  ": " ",
    "  #": " ",
    "   ": " ",
}

def ping_pong():
    ca = "#         o- #"
    print("Ping Pong:")
    t = 0
    while True:
        print("T", t, ":'{}'".format(ca))
        ca2 = ca_step(ca, rule_ping_pong)
        ca = ca2
        t = t +1
        time.sleep(0.1)

#ping_pong()