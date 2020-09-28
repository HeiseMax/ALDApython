
rule_ping_pong2 = {
    " o-  ": " ",
    "o-   ": " ",
    "  o- ": "-",
    "   o-": "o",
    "-o   ": "o",
    " -o  ": "-",
    "  -o ": " ",
    "   -o": " ",
    "-    ": " ",
    "    -": " ",
    "o    ": " ",
    "    o": " ",
    "#o-  ": "o",
    " #o- ": "-",
    "# o- ": "-",
    "#   o": " ",
    "#   -": " ",
    " #-o ": " ",
    "#-o  ": "-",
    "# -o ": " ",
    " -o# ": "-",
    "-o#  ": "#",
    "-o # ": "o",
    "o-#  ": "#",
    " o-# ": " ",
    "o- # ": " ",
    "  #  ": "#",
    " #   ": " ",
    "#    ": " ",
    "     ": " ",
    "- #  ": "#",
    " # o-": "o",
    "-  # ": " ",
    "   # ": " ",
    " o- #": " ",
    "o-  #": " ",
    "-   #": " ",
    "    #": " ",
    " #  o": " ",
    "#  o-": "o",
    "  # o": "#",
    "  #o-": "#",
    "  #-o": "#",
    "  # -": "#",
    " # -o": " ",
    "o   #": " ",
    "-o  #": "o",
    " -o #": "-",
    "o  # ": " ",
    "o #  ": "#",
    "  -o#": "o",
    "  o-#": "-",
    " #  -": " ",
    "#  -o": " "
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

def ping_pong2():
    ca = "#         o- #"
    print("Ping Pong:")
    t = 0
    while True:
        ca2 = ""
        i = 0
        while (i < len(ca)):

            if i == 0:
                ca2 = ca2 + rule_ping_pong2["  " + ca[i:i + 3]]

            elif i == 1:
                ca2 = ca2 + rule_ping_pong2[ " " + ca[i - 1: i + 3]]

            elif i == len(ca) - 2:
                ca2 = ca2 + rule_ping_pong2[ca[i - 2: i + 2] + " "]

            elif i == len(ca) - 1:
                ca2 = ca2 + rule_ping_pong2[ca[i - 2: i + 2] + "  "]

            else:
                ca2 = ca2 + rule_ping_pong2[ca[i - 2:i + 3]]

            i = i + 1


        print("T", t, ":'{}'".format(ca2))
        t = t +1
        time.sleep(0.1)
        ca = ca2
