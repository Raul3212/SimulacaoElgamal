import socket as skt
import random as rnd
import math as mt
from euclides import *
from threading import Thread

# Seguind o esquema apresentado no livro, onde Bob inicia o procedimento.
class Bob(Thread):
    def __init__(self, p, alpha):
        Thread.__init__(self)
        self.p = p
        self.alpha = alpha
    
    def run(self):
        # seleciona kpr em {2, ..., p-2}
        kpr = rnd.choice(list(range(2, self.p-1)))
        print("[Bob] Selecionei Kpr = {}".format(kpr))
        # computa kpub = alpha^kpr mod p
        kpub = int(mt.pow(self.alpha, kpr) % self.p)
        print("[Bob] Calculei Kpub = {}".format(kpub))
        # enviando (p, alpha, kpub) no formato p#alpha#kpub
        s = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
        s.connect(("localhost", 3212))
        while True:
            s.send(bytearray("{}#{}#{}".format(self.p, self.alpha, kpub), encoding="utf-8"))
            print("[Bob] Enviando (p, alpha, Kpub) = ({}, {}, {})".format(self.p, self.alpha, kpub))
            # recebe (ke, y) no formato ke#y
            msg = str(s.recv(1024), "utf-8")
            msgList = msg.split("#")
            # converte ke e y para inteiros
            (ke, y) = int(msgList[0]), int(msgList[1])
            print("[Bob] Recebi Ke = {} e y = {}".format(ke, y))
            # calcula km
            km = int(mt.pow(ke, kpub) % self.p)
            print("[Bob] Calculei Km = {}".format(km))
            # calcula o inverso modular de km
            (r, s, t) = euclides_extendido(self.p, km)
            if t < 0: t += self.p
            print("[Bob] Calculei o Km^-1 = {}".format(t))
            # descriptografa y e obtém x
            x = int(y * t % self.p)
            print("[Bob] Calculei x = {}".format(x))
            break
            
        



