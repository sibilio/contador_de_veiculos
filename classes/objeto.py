import config
import funcoes.constantes as ct
import cv2
from funcoes.tensor_util import converte_tensorflow_box
from funcoes.tensor_util import mediatriz_tensorflow_box
from funcoes.matematica import egr

class Objeto(object):
    #coordenada_inicial = mediatriz do box encontrado pelo tensorflow
    #coordenada_atual = mediatriz do último box encontrado pelo tensorflow
    def __init__(self, tensorflow_box, classe):
        self._coordenada_inicial = mediatriz_tensorflow_box(tensorflow_box)
        self._coordenada_atual = []
        self._tensorflow_box = tensorflow_box
        self._classe = classe
        self._cor_box = str(int(classe))
        self._entrou = False
        self._saiu = False
        self._direcao = 0
        self._num_checagens = 5
        # Se em num_checagens checagem a coordenada não for achada o objeto é fechado
        self._checagem = self._num_checagens
        self._fechado = False

    @property
    def entrou(self):
        return self._entrou

    @entrou.setter
    def entrou(self, value):
        if self._entrou == False and value == True:
            self._entrou = True

    @property
    def saiu(self):
        return self._saiu

    @saiu.setter
    def saiu(self, value):
        if self._saiu == False and value == True:
            self._saiu = True

    @property
    def direcao(self):
        return self._direcao

    @direcao.setter
    def direcao(self, value):
        if (self._direcao == 0) and (value in ct.DIRECAO.values()):
            self._direcao = value

    @property
    def coordenada_atual(self):
        if len(self._coordenada_atual) == 0:
            return self._coordenada_inicial
        else:
            return self._coordenada_atual

    @property
    def fechado(self):
        return self._fechado

    @fechado.setter
    def fechado(self, value):
        if (not self._fechado) and (value == True):
            self._fechado = True

    def egr(self):
        return egr(self._coordenada_inicial, self._coordenada_atual)

    def desenha_quadro(self, frame):
        box = converte_tensorflow_box(self._tensorflow_box)
        x_centro = int((box[0][0] + box[1][0]) / 2)
        y_centro = int((box[0][1] + box[1][1]) / 2)
        cv2.rectangle(frame, box[0], box[1], config.COR_CLASSE[self._cor_box])
        cv2.circle(frame, (x_centro, y_centro), 2, ct.COR['verde'], thickness=2)


    def atualiza_coordenada(self, tensorflow_box):
        achei_objeto = False

        nova_coordenada = mediatriz_tensorflow_box(tensorflow_box)

        p1, p2 = converte_tensorflow_box(tensorflow_box)
        diferenca_x = int((p1[0] - p2[0]) / 2)
        diferenca_x = diferenca_x if diferenca_x > 0 else diferenca_x * -1
        diferenca_y = int((p1[1] - p2[1]) / 2)
        diferenca_y = diferenca_y if diferenca_y > 0 else diferenca_y * -1

        if len(self._coordenada_atual) == 0:
            if  (nova_coordenada[0] <= self._coordenada_inicial[0] + diferenca_x and \
                 nova_coordenada[0] >= self._coordenada_inicial[0] - diferenca_x) and \
                (nova_coordenada[1] <= self._coordenada_inicial[1] + diferenca_y and \
                 nova_coordenada[1] >= self._coordenada_inicial[1] - diferenca_y):
                achei_objeto = True
        else:
            if (nova_coordenada[0] <= self._coordenada_atual[0] + diferenca_x  and \
                nova_coordenada[0] >= self._coordenada_atual[0] - diferenca_x ) and \
               (nova_coordenada[1] <= self._coordenada_atual[1] + diferenca_y and \
                nova_coordenada[1] >= self._coordenada_atual[1] - diferenca_y ):
                achei_objeto = True

        if achei_objeto == True:
            self._coordenada_atual = nova_coordenada
            self._tensorflow_box = tensorflow_box
            self._checagem = self._num_checagens
        else:
            self._checagem -= 1
            if self._checagem == 0:
                self._fechado = True

        return achei_objeto