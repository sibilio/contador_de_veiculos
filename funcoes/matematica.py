import numpy as np
import matplotlib.pyplot as plt

#Calcula a equação geral (egr) da reta seguindo a fórmula ax+by+c
#retorna uma tupla com os termos (a, b, c)
def egr(p1, p2):
    a = p1[1] + (p2[1] * -1)
    b = p2[0] + (p1[0] * -1)
    c = (p1[0] * p2[1]) + ((p2[0] * p1[1]) * -1)
    return (int(a), int(b), int(c))

#Equação reduzida da reta (err) segue a fórmula y = -(a/b)x - (c/b)
#Para efeito de cálculo chamaremos -(a/b)x de termo1 e -(c/b) de termo2
#Calculamos a egr de dois pontos onde recebemos a, b, c e podemos calcular a err
#_egr = (a, b, c) -> representa a equação geral da reta
def err(_egr):
    a, b, c = _egr

    termo1 = -1*(a/b)
    termo2 = -1*(c/b)

    return (termo1, termo2)

#Retorna o coeficiente angular da reta que passa por dois pontos
#através da equação reduzida da reta
#_egr = (a, b, c) -> equação geral da reta
def coeficiente_angular(_egr):
    t1, t2 = err(_egr)
    return t1

#Retorna a equação geral da reta r que passa por um ponto p1 e é perpendicular a reta s
#que é representada pela egr1
def egr_perpendicular(p1, egr1):
    ca1 = coeficiente_angular(egr1)

    #levando em conta que uma reta é perpendicular a outra quando mr*ms = -1, onde:
    #r = egr1, s = reta2, m=coeficiente angular; então consideraremos a variável ca1
    #o coeficiente angular da reta r
    #calculo do coeficiente angular da reta s guardado na variável ca2
    ca2 = -1/ca1

    #cálculo da egr que passa pelo ponto p1 é é perpendicular a egr1
    a = int(ca2)
    b = int(-1)
    c = int((-1 * (ca2 * p1[0])) + p1[1])

    return a, b, c

#Retorna o valor de y para o x passado segunda equação gera da reta egr
def get_y(egr, x):
    a, b, c = egr
    y = ((a * x * -1) + (c * -1)) / b
    return int(y)

#Retorna o valor de x para o y passado segunda equação gera da reta egr
def get_x(egr, y):
    a, b, c = egr
    x = ((b * y * -1) + (c * -1)) / a
    return int(x)
    
#Calcula o ponto de intersecção entre duas retas através das suas equações gerais
def ponto_interseccao(egr1, egr2):
    a, c = _reduz(egr1, egr2)
    x = (c * -1)/a

    a, b, c = egr1
    if b == 0:
        a, b, c = egr2
        a, c = _reduz(egr1, egr2)
        x = (c * -1) / a

    y = ((a * x * -1) + (c * -1)) / b

    return (int(x), int(y))

#Calcula a mediatriz (ponto médio) entre duas coordenadas
def mediatriz(p1, p2):
    mx_float = (p1[0] + p2[0]) / 2
    my_float = (p1[1] + p2[1]) / 2
    mx = int(mx_float)
    my = int(my_float)
    return (mx, my)

#Resolve um sistema de equações do tipo:
# (a1x + b1y + c1) + (a2x + b2y + c2)
#Isolando a e c achando o 'x' da equação para substituir e achar os pontos
def _reduz(egr1, egr2):
    fator = (egr1[1] / egr2[1]) * -1
    a = egr1[0] + (egr2[0]*fator)
    c = egr1[2] + (egr2[2]*fator)
    reduzida = (a, c)

    return reduzida

#Retorna True ou False para a comparação de np.array com valores boleanos
#Ex.: [True, True, True, True]
def np_compare(np1, np2):
    comp = np1 == np2
    retorno = True

    if(comp.__class__ == np.array([]).__class__):
        for c in comp:
            if c == False:
                retorno = False
                break
    else:
        if comp == False or comp == True:
            return comp

    return retorno

##########################################################################
#Testes
##########################################################################

#Desenha o gráfico para verificarmos que realmente a reta está perpendicular
def teste_egr_perpendicular():
    p1 = (28, 28)
    egr1 = egr((-5, 25), (20, 5))
    egr_p = egr_perpendicular(p1, egr1)

    r1p1 = (-5, get_y(egr1, -5))
    r1p2 = (25, get_y(egr1, 25))

    r2p1 = (0, get_y(egr_p, 0))
    r2p2 = (28, get_y(egr_p, 28))

    plt.plot([r1p1[0], r1p2[0]], [r1p1[1], r1p2[1]])
    plt.plot([r2p1[0], r2p2[0]], [r2p1[1], r2p2[1]])
    plt.axis([-10, 35, 0, 35])
    plt.show()

def teste_egr(p, egr):
    resultado = (p[0] * egr[0]) + (p[1] * egr[1]) + egr[2]
    print("Teste_egr: {}".format(resultado == 0))

def teste_interseccao():
    p1r1 = (2, 1)
    p2r1 = (3, 3)

    p1r2 = (1, 4)
    p2r2 = (5, 2)

    ponto_interseccao_real = (3, 3)

    egr1 = egr(p1r1, p2r1)
    egr2 = egr(p1r2, p2r2)

    ponto = ponto_interseccao(egr1, egr2)
    print("Testa_ponto_interseccao: {}".format(ponto == ponto_interseccao_real))

def roda_testes():
    p1 = (4, 6)
    p2 = (6, 8)

    termos = egr(p1, p2)

    teste_egr((50, 52), termos)
    teste_interseccao()

if __name__ == "__main__":
    teste_egr_perpendicular()