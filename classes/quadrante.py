import funcoes.matematica as mt
import funcoes.constantes as ct
import funcoes.tensor_util as tu
import config
import cv2
"""
Exemplo de quadrante:
                      R2
      p2  +----------------------------+ p3
         /                            /
        /                            /
    R1 /                            / R3
      /                            /
     /                            /
 p1 +----------------------------+ p4
                 R4

p1, p2, p3, p4 = pontos das retas segundo exemplo acima no formato (x, y)
"""
class Quadrande(object):
    def __init__(self, p1, p2, p3, p4):
        self._p1 = p1
        self._p2 = p2
        self._p3 = p3
        self._p4 = p4
        self._r1 = mt.egr(p1, p2)
        self._r2 = mt.egr(p2, p3)
        self._r3 = mt.egr(p4, p3)
        self._r4 = mt.egr(p1, p4)
        self._cor = config.COR['azul']
        self._largura_linha = 1
        self._mostrar_linhas = False

    @property
    def mostrar_linhas(self):
        return self._mostrar_linhas

    @mostrar_linhas.setter
    def mostrar_linhas(self, value):
        if value == True or value == False:
            self._mostrar_linhas = value
        else:
            self._mostrar_linhas = False

    @property
    def cor(self):
        return self._cor

    @cor.setter
    def cor(self, value):
        if value in ct.COR.values:
            self._cor = value
        else:
            self.cor = ct.COR['branco']

    @property
    def largura_linha(self):
        return self._largura_lina

    @largura_linha.setter
    def largura_linha(self, value):
        if value <= 1:
            self._largura_linha = 1
        elif value >= 5:
            self._largura_linha = 5
        else:
            self._largura_linha = value

#Desenha as linhas do quadrante na tela
    def desenhar(self, frame):
        if self._mostrar_linhas == True:
            cv2.line(frame, self._p1, self._p2, self._cor, self._largura_linha)
            cv2.line(frame, self._p2, self._p3, self._cor, self._largura_linha)
            cv2.line(frame, self._p4, self._p3, self._cor, self._largura_linha)
            cv2.line(frame, self._p1, self._p4, self._cor, self._largura_linha)


#retorna True se a coordenada estiver dentro da área de contagem
    def coordenada_dentro(self, coordenada):
        x = coordenada[0]
        y = coordenada[1]

        egr_inter1 = mt.egr_perpendicular(coordenada, self._r1)
        egr_inter2 = mt.egr_perpendicular(coordenada, self._r2)
        egr_inter3 = mt.egr_perpendicular(coordenada, self._r3)
        egr_inter4 = mt.egr_perpendicular(coordenada, self._r4)

        p_inter1 = mt.ponto_interseccao(egr_inter1, self._r1)
        p_inter2 = mt.ponto_interseccao(egr_inter2, self._r2)
        p_inter3 = mt.ponto_interseccao(egr_inter3, self._r3)
        p_inter4 = mt.ponto_interseccao(egr_inter4, self._r4)

        if  x > p_inter1[0] and \
            x < p_inter3[0] and \
            y > p_inter2[1] and \
            y < p_inter4[1]:
            return True
        else:
            return False

#Verifica o posicao do ponto em relação ao direcionamento do quadrante
#Para ter uma avaliação real da direção do objeto devemos testar o ponto
#antes de entrar na área de contagem do quadrante
    def direcao(self, ponto, direcao=ct.DIRECAO['esquerda_direita']):
        if direcao != ct.DIRECAO['esquerda_direita']:
            direcao = ct.DIRECAO['baixo_cima']

        x = ponto[0]
        y = ponto[1]

        if direcao == ct.DIRECAO['esquerda_direita']:
            egr_inter1 = mt.egr_perpendicular(ponto, self._r1)
            egr_inter3 = mt.egr_perpendicular(ponto, self._r3)
            p_inter1 = mt.ponto_interseccao(egr_inter1, self._r1)
            p_inter3 = mt.ponto_interseccao(egr_inter3, self._r3)
            if (x < p_inter1[0]) and (x < p_inter3[0]):
                return ct.DIRECAO['esquerda_direita']
            else:
                return ct.DIRECAO['direita_esquerda']
        else:
            egr_inter2 = mt.egr_perpendicular(ponto, self._r2)
            egr_inter4 = mt.egr_perpendicular(ponto, self._r4)
            p_inter2 = mt.ponto_interseccao(egr_inter2, self._r2)
            p_inter4 = mt.ponto_interseccao(egr_inter4, self._r4)
            if (y < p_inter2[1]) and (y < p_inter4[1]):
                return ct.DIRECAO['baixo_cima']
            else:
                return ct.DIRECAO['cima_baixo']
