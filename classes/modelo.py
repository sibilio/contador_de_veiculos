import tensorflow as tf
import numpy as np
import os
import cv2
from utils import label_map_util
import config

#from utils import visualization_utils as vis_util

class Modelo(object):
    def __init__(self, cam=1):
        self._MODEL_NAME = config.EXECUTION_PATH + "/modelos/" + config.MODEL_NAME
        self._PATH_TO_CKPT = self._MODEL_NAME + '/frozen_inference_graph.pb'
        self._PATH_TO_LABELS = os.path.join(config.EXECUTION_PATH, 'modelos/mscoco_label_map.pbtxt')
        self._image_tensor = ""
        self._detection_boxes = ""
        self._detection_scores = ""
        self._detection_classes =""
        self._num_detections = ""

        self._NUM_CLASSES = 90
        self._cam = cam

    def carrega_modelo(self):
        self._detection_graph = tf.Graph()
        with self._detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self._PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

    def carrega_labels(self):
        label_map = label_map_util.load_labelmap(self._PATH_TO_LABELS)
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=self._NUM_CLASSES,
                                                                    use_display_name=True)
        category_index = label_map_util.create_category_index(categories)

    def inicializar(self):
        self.carrega_modelo()
        self.carrega_labels()

    def graph(self):
        return self._detection_graph.as_default()

    def session(self):
        return tf.Session(graph=self._detection_graph)

    def inicializar_tensores(self):
        self._image_tensor = self._detection_graph.get_tensor_by_name('image_tensor:0')
        self._detection_boxes = self._detection_graph.get_tensor_by_name('detection_boxes:0')
        self._detection_scores = self._detection_graph.get_tensor_by_name('detection_scores:0')
        self._detection_classes = self._detection_graph.get_tensor_by_name('detection_classes:0')
        self._num_detections = self._detection_graph.get_tensor_by_name('num_detections:0')

    def run(self, sess, image):
        return sess.run(
            [self._detection_boxes, self._detection_scores,
             self._detection_classes, self._num_detections],
            feed_dict={self._image_tensor: image})
