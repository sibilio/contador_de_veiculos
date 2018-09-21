#Biblioteca com funções para manipulação dos dados recebidos
#das predições do TensorFlow
import config
import funcoes.constantes as const
import numpy as np

def converte_tensorflow_box(tensorflow_box):
    ymin, xmin, ymax, xmax = tensorflow_box

    ymin = int(ymin * config.RESOLUTION['height'])
    xmin = int(xmin * config.RESOLUTION['width'])
    ymax = int(ymax * config.RESOLUTION['height'])
    xmax = int(xmax * config.RESOLUTION['width'])

    coordenadas = ((xmin, ymax), (xmax, ymin))

    return coordenadas

def mediatriz_tensorflow_box(tensorflow_box):
    p1, p2 = converte_tensorflow_box(tensorflow_box)

    mediatriz_x = (p1[0] + p2[0]) / 2
    mediatriz_y = (p1[1] + p2[1]) / 2

    return (mediatriz_x, mediatriz_y)

#Remove os dados de objetos que não são da classe desejada
def seleciona_objetos_desejados(boxes, scores, classes):
    boxes_limpos, scores_limpos, classes_limpas = _remove_objeto_score_menor(boxes, scores, classes)
    boxes_limpos, scores_limpos, classes_limpas = _remove_objeto_classe_nao_desejada(boxes_limpos,
                                                                                     scores_limpos,
                                                                                     classes_limpas)
    """
    boxes_limpos, scores_limpos, classes_limpas = _remove_objeto_fora_do_limite(boxes_limpos,
                                                                                scores_limpos,
                                                                                classes_limpas,
                                                                                limite,
                                                                                eixo,
                                                                                direcao)
    """
    return boxes_limpos, scores_limpos, classes_limpas

# remove dados com score menor que o score mínimo
def _remove_objeto_score_menor(boxes, scores, classes):
    indices = []
    for index, score in enumerate(scores[0]):
        if (score <= config.MIN_SCORE):
            indices.append(index)
    if len(indices) > 0:
        boxes_limpos = np.delete(boxes[0], indices, axis=0)
        scores_limpos = np.delete(scores[0], indices, axis=0)
        classes_limpas = np.delete(classes[0], indices, axis=0)
        return boxes_limpos, scores_limpos, classes_limpas

    return boxes, scores, classes

def _remove_objeto_classe_nao_desejada(boxes, scores, classes):
    indices = []
    for index, classe in enumerate(classes):
        if(classe not in config.CLASSES.values()):
            indices.append(index)
    if len(indices) > 0:
        boxes_limpos = np.delete(boxes, indices, axis=0)
        scores_limpos = np.delete(scores, indices, axis=0)
        classes_limpas = np.delete(classes, indices, axis=0)
        return boxes_limpos, scores_limpos, classes_limpas

    return boxes, scores, classes

# remove boxes fora do limite
def _remove_objeto_fora_do_limite(boxes, scores, classes, limite, eixo, direcao):
    indices = []
    for index, classe in enumerate(classes):
        mediatriz = mediatriz_tensorflow_box(boxes[index])

        if eixo == const.EIXO['x'] and direcao == const.DIRECAO['esquerda_direita']:
            if mediatriz >= limite:
                indices.append(index)
        elif eixo == const.EIXO['x'] and direcao == const.DIRECAO['direita_esquerda']:
            if mediatriz <= limite:
                indices.append(index)
        elif eixo == const.EIXO['y'] and direcao == const.DIRECAO['baixo_cima']:
            if mediatriz >= limite:
                indices.append(index)
        elif eixo == const.EIXO['y'] and direcao == const.DIRECAO['cima_baixo']:
            if mediatriz <= limite:
                indices.append(index)

    if len(indices) > 0:
        boxes_limpos = np.delete(boxes, indices, axis=0)
        scores_limpos = np.delete(scores, indices, axis=0)
        classes_limpas = np.delete(classes, indices, axis=0)
        return boxes_limpos, scores_limpos, classes_limpas

    return boxes, scores, classes