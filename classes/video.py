import cv2
import numpy as np
import string
import random
import funcoes.constantes as ct

#Abstrai o funcionamento do OpenCV para a manipulação do vídeo
#conforme necessidade específica do projeto de reconhecimento
#de objetos
class Video(object):
    #_video_name = caminho completo do vídeo
    #_video = objeto de vídeo do OpenCV
    #_frame = Frame capturado com o procedimento processar
    def __init__(self, video_name, definicao=(int(640), int(480)), name_window="", realizar_gravacao=False):
        self._video_name = video_name
        self._video = cv2.VideoCapture(self._video_name)
        self._frame = ""
        self._out = ""
        self._realizar_gravacao = realizar_gravacao
        self._definicao = definicao
        self._name_window = name_window
        self._nome_arquivo = ""
        self._definicao_gravacao = definicao
        self._legenda = []

    @property
    def video_name(self):
        return self._video_name

    #Lê o próximo frame do vídeo
    def processar(self):
        ok, self._frame = self._video.read()
        return ok

    #Retorna o frame com o comando np.expand_dims
    def np_expande(self):
        return np.expand_dims(self._frame, axis=0)

    @property
    def frame(self):
        return self._frame

    #redimensiona o frame
    def resize_frame(self, dimensao):
        w = int(dimensao[0])
        h = int(dimensao[1])
        self._frame = cv2.resize(self._frame, (w, h));

    #inicia gravação de vídeo em disco
    #nome_arquivo = nome do arquivo com caminho completo e extensão
    #definicao = tupla com largura e altura do vídeo ex.:(640, 360)
    def iniciar_gravacao(self, nome_arquivo, definicao=""):
        if self._realizar_gravacao:
            if definicao != "":
                self._definicao_gravacao = definicao
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self._out = cv2.VideoWriter(nome_arquivo, fourcc, 20.0, self._definicao_gravacao)

    #grava o frame no arquivo
    def gravar_frame(self):
        if self._realizar_gravacao:
            frame = cv2.resize(self._frame, self._definicao_gravacao)
            self._out.write(frame)

    def show(self, name_window=''):
        if name_window == '':
            if self._name_window == '':
                alphabet = string.ascii_letters + string.digits
                self._name_window = ''.join(random.choice(alphabet) for i in range(8))
        else:
            if self._name_window == '':
                self._name_window = name_window

        cv2.imshow(self._name_window, self._frame)

    def finalizar(self):
        self._video.release()
        if self._nome_arquivo != "":
            self._out.release()
        cv2.destroyWindow(self._name_window)

    def waitKey(self, key='q'):
        if cv2.waitKey(25) & 0xFF == ord('q'):
            return True
        else:
            return False

    def reset_legenda(self):
        self._legenda = []

    def frase_legenda(self, frase):
        self._legenda.append(frase)

    def legendar(self, frame):
        y = 400
        cor = ct.COR['branco']
        cv2.rectangle(frame, (55, 370), (560, 450), ct.COR['preto'], thickness=cv2.FILLED)
        for legenda in self._legenda:
            cv2.putText(frame, legenda, (63, y), cv2.FONT_HERSHEY_COMPLEX, 0.8, cor)
            y += 30
            cor = ct.COR['amarelo'] if cor==ct.COR['branco'] else ct.COR['branco']
