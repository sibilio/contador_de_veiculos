import cv2
import funcoes.constantes as ct

class C1(object):
    def __init__(self):
        self.nome = "NoNoNo"

if __name__ == "__main__":
    c = [C1(), C1(), C1()]
    c[0].nome = "Marcos"
    c[1].nome = "Cruz"
    c[2].nome = "Sibilio"

    for index, a in enumerate(c):
        if index == 0:
            a.nome = "Elaine"
        elif index == 1:
            a.nome = "Duarte"
        elif index == 2:
            a.nome = "SIBILIO"

    print(c[0].nome)
    print(c[1].nome)
    print(c[2].nome)