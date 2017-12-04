import random as rnd
import socket as skt
from threading import Thread

class Alice(Thread):
    def __init__(self, x):
        Thread.__init__(self)
        self.x = x

    def run(self):
        
        s = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
        try:
            s.setsockopt(skt.SOL_SOCKET, skt.SO_REUSEADDR, 1)
            s.bind(('localhost', 3212))
        except:
            print("Erro ao escutar na porta 3212")
            sys.exit(0)

        s.listen(1)
        con, client = s.accept()
        # recebe a pensagem no formato p#alpha#beta
        msg = str(con.recv(1024), "utf-8")
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
            y = int(self.x * km % p)
            print("[Alice] Criptografei x = {} e obtive y = {}".format(self.x, y))
            # envia (ke, y) no formato ke#y
            con.sendto(bytearray("{}#{}".format(ke, y), encoding="utf-8"), client)
            print("[Alice] Enviando (Ke, y) = ({}, {})".format(ke, y))

        con.close()
        s.close()