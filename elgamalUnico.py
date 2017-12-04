import sys
import socket as skt
import random as rnd
from euclides import *
from threading import Thread

def main():
    bob = False
    p = 0
    alpha = 0
    x = 0

    if len(sys.argv) < 2:
        print("Use:")
        print("python elgamalUnico.py -bob [p] [alpha]")
        print("python elgamalUnico.py -alice [x]")
        sys.exit(0)
    elif sys.argv[1] == '-bob' and len(sys.argv) == 4:
        p = int(sys.argv[2])
        alpha = int(sys.argv[3])
        bob = True
    elif sys.argv[1] == '-alice' and len(sys.argv) == 3:
        x = int(sys.argv[2])
    else:
        sys.exit(0)

    s = skt.socket(skt.AF_INET, skt.SOCK_STREAM)

    if bob == True:
        s.bind(('localhost', 3212))
        # seleciona kpr em {2, ..., p-2}
        kpr = rnd.choice(list(range(2, p-1)))
        print("[Bob] Selecionei Kpr = {}".format(kpr))
        # computa kpub = alpha^kpr mod p
        kpub = int(pow(alpha, kpr, p))
        print("[Bob] Calculei Kpub = {}".format(kpub))
        #esperando alice
        s.listen(1)
        con, client = s.accept()
        # enviando (p, alpha, kpub) no formato p#alpha#kpub
        con.send(bytearray("{}#{}#{}".format(p, alpha, kpub), encoding="utf-8"))
        print("[Bob] Enviando (p, alpha, Kpub) = ({}, {}, {})".format(p, alpha, kpub))
        # recebe (ke, y) no formato ke#y
        msg = str(con.recv(1024), "utf-8")
        msgList = msg.split("#")
        # converte ke e y para inteiros
        (ke, y) = int(msgList[0]), int(msgList[1])
        print("[Bob] Recebi Ke = {} e y = {}".format(ke, y))
        # calcula km
        km = int(pow(ke, kpr, p))
        print("[Bob] Calculei Km = {}".format(km))
        # calcula o inverso modular de km
        (r, s, t) = euclides_extendido(p, km)
        if t < 0: t += p
        print("[Bob] Calculei o Km^-1 = {}".format(t))
        # descriptografa y e obtém x
        x = int(y * t % p)
        print("[Bob] Calculei x = {}".format(x))
    else:
        s.connect(("localhost", 3212))
        # recebe a pensagem no formato p#alpha#beta
        msg = str(s.recv(1024), "utf-8")
        if msg:
            # quebra a mensagem em [p, alpha, kpub]
            strList = msg.split("#")
            # converte p, alpha e kpub para inteiros
            (p, alpha, kpub) = int(strList[0]), int(strList[1]), int(strList[2])
            print("[Alice] Recebi p = {}, alpha = {} e Kpub = {}".format(p, alpha, kpub))
            # seleciona i em {2, ..., p-2}
            i = rnd.choice(list(range(2, p-1)))
            print("[Alice] Selecionei i = {}".format(i))
            # calcula chave efêmera 
            ke = int(pow(alpha, i, p))
            print("[Alice] Calculei Ke = {}".format(ke))
            # calcula chave máscara
            km = int(pow(kpub, i, p))
            print("[Alice] Calculei Km = {}".format(km))
            # criptografa x
            y = int(x * km % p)
            print("[Alice] Criptografei x = {} e obtive y = {}".format(x, y))
            # envia (ke, y) no formato ke#y
            s.send(bytearray("{}#{}".format(ke, y), encoding="utf-8"))
            print("[Alice] Enviando (Ke, y) = ({}, {})".format(ke, y))

if __name__ == '__main__':
    main()        



