import funcoes.matematica as mt
import funcoes.constantes as ct
import funcoes.tensor_util as tu
import config
import cv2
from classes.objeto import Objeto

class Contador(object):
    def __init__(self, quadrante, direcao=ct.DIRECAO['esquerda_direita']):
        self._quadrante = quadrante
        self._objetos = []
        self._direcao = direcao
        self._inicio_fim = 0
        self._fim_inicio = 0
        self.limite_frames_sem_boxes = 10
        self._frames_sem_boxes = 0

    def cria_objeto(self, tensorflow_box, classe):
        obj = Objeto(tensorflow_box, classe)
        self._objetos.append(obj)
        return len(self._objetos) - 1 #retorna o indice do último registro add

    def atualizar(self, frame, boxes, scores, classes):
        if len(scores) > 0:
            criar_objetos = self._rastrear_objetos(boxes)
            self._criar_objetos(criar_objetos, boxes, classes)
            self._verificar_passagem()
            self._desenhar_boxes(frame)
            self._frames_sem_boxes = 0
        else:
            self._frames_sem_boxes += 1
            if self._frames_sem_boxes >= self.limite_frames_sem_boxes:
                self._objetos = []
                self._frames_sem_boxes = 0

    def _rastrear_objetos(self, boxes):
        objetos_para_criar = []
        for index, box in enumerate(boxes):
            obj_achado = False
            for obj in self._objetos:
                obj_achado = obj.atualiza_coordenada(box)
                if obj_achado:
                    if obj.direcao == 0:
                        obj.direcao = self._quadrante.direcao(obj.coordenada_atual, self._direcao)
                    break

            if not obj_achado:
                objetos_para_criar.append(index)

        return objetos_para_criar

    def _criar_objetos(self, indices, boxes, classes):
        for i in indices:
            obj = Objeto(boxes[i], classes[i])
            self._objetos.append(obj)

    def _verificar_passagem(self):
        remover = []
        for index, obj in enumerate(self._objetos):
            dentro = self._quadrante.coordenada_dentro(obj.coordenada_atual)
            if dentro:
                obj.entrou = True
            elif obj.entrou and not obj.saiu:
                if obj.direcao == ct.DIRECAO['esquerda_direita'] or \
                        obj.direcao == ct.DIRECAO['cima_baixo']:
                    self._inicio_fim += 1
                else:
                    self._fim_inicio += 1
                obj.saiu = True

            if obj.fechado:
                remover.append(index)

        for i in remover:
            if i < len(self._objetos):
                self._objetos.pop(i)

    def _desenhar_boxes(self, frame):
        for obj in self._objetos:
            if not (obj.entrou and obj.saiu):
                obj.desenha_quadro(frame)
        print(len(self._objetos))

#Totaliza os objetos que passaram pela área de contagem
    def totalizar(self):
        return self._inicio_fim, self._fim_inicio

#Desenha a área de contagem
    def desenhar(self, frame):
        self._quadrante.desenhar(frame)