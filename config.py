import os
from funcoes.constantes import COR
from funcoes.constantes import DIRECAO as DIR
from time import localtime, strftime

#Resolução do vídeo analisado
RESOLUTION = {
    'width': int(640),      #Largura da resolução do vídeo
    'height': int(480),     #Altura da resolução do vídeo
}

#VIDEO_NAME = "/home/marcos/Vídeos/janela_19-01-2018_10:52:52.avi" #nome do vídeo analisado
VIDEO_NAME = "/home/marcos/Vídeos/janela_04-02-2018_01:16:37.avi" #nome do vídeo analisado
#VIDEO_NAME = "http://192.168.100.43:81/videostream.cgi?loginuse=admin&loginpas=" #nome do vídeo analisado

SHOW_TRACES = True          #Se True desenha todas as linhas e quadrados de reconhecimento na tela

FRAME_CHECK = 1             #Reconhece os objetos da tela a cada 10 (padrão) frames

RECORDING = False           #mudar para true se deseja gravar as imagens do teste

MIN_SCORE = 0.4             #Score mínimo para seleção

CLASSES = {                 #Classes que serão reconhecidas pelo modelo
    'carro': 1.0,
}

COR_CLASSE = {
    '1': COR['azul'],
}

MODEL_NAME = "modelo_marcos" #Modelo que será usado para a análise
#MODEL_NAME = "ssd_mobilenet_v1_coco_2017_11_17" #Modelo que será usado para a análise
#MODEL_NAME = "faster_rcnn_inception_resnet_v2_atrous_coco_2017_11_08"

#Não modificar os valores da variáveis abaixo pois são somente seu valor é
#formado à partir do valor das variáveis acima que podem ser modificadas
#segundo a necessidade do programador
FULL_RESOLUTION = (RESOLUTION['width'], RESOLUTION['height'])

EXECUTION_PATH = os.getcwd()

#Retorna um nome diferente para os arquivos de saída considerando
#data e horário em que iniciou-se a gravação
def name_video_out():
    prefix = EXECUTION_PATH + "/video_out/out_"
    str_date = strftime("%d-%m-%Y_%H:%M:%S", localtime())
    name_video = prefix + str_date + ".avi"
    return name_video