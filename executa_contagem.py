import cv2
import config
import funcoes.constantes as const
from classes.modelo import Modelo
from classes.video import Video
from classes.contador import Contador
from classes.quadrante import Quadrande
from funcoes.tensor_util import seleciona_objetos_desejados as sod

def totalizar(t1, t2):
    print("A contagem de objetos foi:")
    print("Objetos que passaram da esquerda para a direita: {}".format(t1))
    print("Objetos que passaram da direita para a esquerda: {}".format(t2))

#from classes.contagem import Contador
import os
import time
import numpy as np
from PIL import Image
from skimage.measure import structural_similarity as ssim

#Configuração###########################################################################################

inicio = time.time()        #contador simples
m = Modelo()

#Objeto responsável pela demarcação das áreas de contagem na imagem
p1 = (255, 344)
p2 = (271, 242)
p3 = (349, 253)
p4 = (334, 354)
quadrante = Quadrande(p1, p2, p3, p4)
quadrante.mostrar_linhas = True

#Objeto responsável pela contagem de objetos
limite = 437    #ponto limite para considerar um objeto
direcao = const.DIRECAO['esquerda_direita']
contador = Contador(quadrante, direcao)

#########################################################################################################

m.inicializar()
with m.graph():
    with m.session() as sess:
        m.inicializar_tensores()
        video = Video(config.VIDEO_NAME,
                      definicao=config.FULL_RESOLUTION,
                      realizar_gravacao=config.RECORDING)
        video.iniciar_gravacao(config.name_video_out(), config.FULL_RESOLUTION)
        video.processar()

        count = 0
        contador_foto = 1
        while True:
            if count == 0:
                m.inicializar_tensores()
                (boxes, scores, classes, num) = m.run(sess, video.np_expande())
                boxes_limpos, scores_limpos, classes_limpas = sod(boxes,
                                                                  scores,
                                                                  classes)
                contador.atualizar(video.frame,
                                   boxes_limpos,
                                   scores_limpos,
                                   classes_limpas)
            count += 1
            if count == config.FRAME_CHECK:
                count = 0

            t1, t2 = contador.totalizar()
            #totalizar(t1, t2)
            contador.desenhar(video.frame)
            legenda1 = "Carros da esquerda para direita: {}".format(t1)
            legenda2 = "Carros da direita para esquerda: {}".format(t2)
            video.reset_legenda()
            video.frase_legenda(legenda1)
            video.frase_legenda(legenda2)
            video.legendar(video.frame)
            video.show()
            video.gravar_frame()
            video.processar()

            if video.waitKey():
                break

        video.finalizar()
#print(inicio)
#print(time.time())
#print(time.time()-inicio)