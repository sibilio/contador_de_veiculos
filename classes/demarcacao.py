import cv2
from funcoes import matematica as mt
import funcoes.constantes as const

class Demarcacao(object):
    #coordenada1, 2, 3 ou 4: são os postos do retângulo a ser traçado para área de contagem
    #distancia_retas_contagem: é a distância entre as duas retas que serão desejadas dentro da área de
    #                          análise que a contagem deve ser feita
    #coordenadas_reta_contagem1 e 2: é a demarcação que vai dizer se o objeto deve ser contado, pois a
    #                               contagem acontece após o objeto cruzar as duas retas na área
    #                               demarcada para a contagem. Formato [(x1, y1), (x2, y2)]
    def __init__(self,
                 coordenada1,
                 coordenada2,
                 coordenada3,
                 coordenada4,
                 coordenadas_reta_contagem1, #Formato [(x1, y1), (x2, y2)]
                 coordenadas_reta_contagem2,
                 eixo = const.EIXO['x'],
                 direcao = const.DIRECAO['esquerda_direita']):
        self._coordenada1 = coordenada1     #coordenada usada para traçar o retângulo
        self._coordenada2 = coordenada2
        self._coordenada3 = coordenada3     #coordenada usada para traçar o retângulo
        self._coordenada4 = coordenada4

        self._reta1 = mt.egr(coordenada1, coordenada4)
        self._reta2 = mt.egr(coordenada1, coordenada2)
        self._reta3 = mt.egr(coordenada3, coordenada2)
        self._reta4 = mt.egr(coordenada3, coordenada4)

        self._pontos_reta_contagem1 = coordenadas_reta_contagem1
        self._pontos_reta_contagem2 = coordenadas_reta_contagem2

        self._reta_contagem1 = mt.egr(self._pontos_reta_contagem1[0], self._pontos_reta_contagem1[1])
        self._reta_contagem2 = mt.egr(self._pontos_reta_contagem2[0], self._pontos_reta_contagem2[1])

        self._largura_linha = int(1)

        self._eixo = eixo
        self._direcao = direcao

        self.mostrar_linhas = True

        self.cor_marcador = const.COR['azul']
        self.cor_reta_contagem1 = const.COR['branco']
        self.cor_reta_contagem2 = const.COR['vermelho']

    def coordenada_esta_dentro(self, coordenada):
        x = coordenada[0]
        y = coordenada[1]

        egr_inter1 = mt.egr_perpendicular(coordenada, self._reta1)
        egr_inter2 = mt.egr_perpendicular(coordenada, self._reta2)
        egr_inter3 = mt.egr_perpendicular(coordenada, self._reta3)
        egr_inter4 = mt.egr_perpendicular(coordenada, self._reta4)

        p_inter1 = mt.ponto_interseccao(egr_inter1, self._reta1)
        p_inter2 = mt.ponto_interseccao(egr_inter2, self._reta2)
        p_inter3 = mt.ponto_interseccao(egr_inter3, self._reta3)
        p_inter4 = mt.ponto_interseccao(egr_inter4, self._reta4)

        if  x > p_inter1[0] and \
            x < p_inter2[0] and \
            x < p_inter3[0] and \
            x > p_inter4[0] and \
            y > p_inter1[1] and \
            y < p_inter2[1] and \
            y < p_inter3[1] and \
            y > p_inter4[1]:
            return True
        else:
            return False

    @property
    def largura_linha(self):
        return self._largura_linha

    @largura_linha.setter
    def largura_linha(self, value):
        self._largura_linha = int(1) if value < 1 else int(value)

    def desenhar(self, frame):
        #linhas da área de contagem
        if self.mostrar_linhas == True:
            cv2.line(frame, self._coordenada1, self._coordenada2, self.cor_marcador, self._largura_linha)
            cv2.line(frame, self._coordenada2, self._coordenada3, self.cor_marcador, self._largura_linha)
            cv2.line(frame, self._coordenada3, self._coordenada4, self.cor_marcador, self._largura_linha)
            cv2.line(frame, self._coordenada1, self._coordenada4, self.cor_marcador, self._largura_linha)

            cv2.line(frame,
                     self._pontos_reta_contagem1[0],
                     self._pontos_reta_contagem1[1],
                     self.cor_reta_contagem1,
                     self._largura_linha)

            cv2.line(frame,
                     self._pontos_reta_contagem2[0],
                     self._pontos_reta_contagem2[1],
                     self.cor_reta_contagem2,
                     self._largura_linha)

    def passou_reta(self, coordenada, qual_reta=1):

        if qual_reta == 1:
            egr_inter1 = mt.egr_perpendicular(coordenada, self._reta_contagem1)
            p_inter1 = mt.ponto_interseccao(egr_inter1, self._reta_contagem1)
        else:
            egr_inter1 = mt.egr_perpendicular(coordenada, self._reta_contagem2)
            p_inter1 = mt.ponto_interseccao(egr_inter1, self._reta_contagem2)

        if self._eixo == const.EIXO['x'] and self._direcao == const.DIRECAO['esquerda_direita']:
            if coordenada[0] < p_inter1[0]:
                return False
            else:
                return True
        elif self._eixo == const.EIXO['x'] and self._direcao == const.DIRECAO['direita_esquerda']:
            if coordenada[0] < p_inter1[0]:
                return True
            else:
                return False
        elif self._eixo == const.EIXO['y'] and self._direcao == const.DIRECAO['cima_baixo']:
            if coordenada[1] < p_inter1[1]:
                return False
            else:
                return True
        elif self._eixo == const.EIXO['y'] and self._direcao == const.DIRECAO['baixo_cima']:
            if coordenada[1] < p_inter1[1]:
                return False
            else:
                return True
