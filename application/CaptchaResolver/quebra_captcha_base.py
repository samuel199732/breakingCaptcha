import cv2
import numpy as np
import os

# run on CPU, to run on GPU comment this line or write '0'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util


class ResolverCapcha:

    def __init__(self, path_to_frozen, path_to_label, num_classes):
        self.path_to_frozen = path_to_frozen
        self.path_to_label = path_to_label
        self.num_classes = num_classes
        label_map = label_map_util.load_labelmap(self.path_to_label)
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=self.num_classes,
                                                                    use_display_name=True)
        self.category_index = label_map_util.create_category_index(categories)

        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.compat.v1.GraphDef()
            with tf.io.gfile.GFile(self.path_to_frozen, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

    def captch_detection(self, image, average_distance_error=3):

        with self.detection_graph.as_default():
            with tf.compat.v1.Session(graph=self.detection_graph) as sess:
                # Open image
                image_np = cv2.imread(image)
                # Resize image if needed
                image_np = cv2.resize(image_np, (0, 0), fx=3, fy=3)
                # To get real color we do this:
                image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
                # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                image_np_expanded = np.expand_dims(image_np, axis=0)
                # Actual detection.
                image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
                boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
                scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
                classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
                num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')
                # Visualization of the results of a detection.
                (boxes, scores, classes, num_detections) = sess.run(
                    [boxes, scores, classes, num_detections],
                    feed_dict={image_tensor: image_np_expanded})
                vis_util.visualize_boxes_and_labels_on_image_array(
                    image_np,
                    np.squeeze(boxes),
                    np.squeeze(classes).astype(np.int32),
                    np.squeeze(scores),
                    self.category_index,
                    use_normalized_coordinates=True,
                    line_thickness=2)

                cv2.imwrite("predic.jpg", cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB))

                # Bellow we do filtering stuff
                captcha_array = []
                # loop our all detection boxes
                for i, b in enumerate(boxes[0]):
                    for Symbol in range(self.num_classes):
                        if classes[0][i] == Symbol:  # check if detected class equal to our symbols
                            if scores[0][i] >= 0.65:  # do something only if detected score more than 0.65
                                # x-left        # x-right
                                mid_x = (boxes[0][i][1] + boxes[0][i][3]) / 2  # find x coordinates center of letter
                                # to captcha_array array save detected Symbol, middle X coordinates and detection percentage
                                captcha_array.append([self.category_index[Symbol].get('name'), mid_x, scores[0][i]])

                # rearange array acording to X coordinates datected
                for number in range(20):
                    for captcha_number in range(len(captcha_array) - 1):
                        if captcha_array[captcha_number][1] > captcha_array[captcha_number + 1][1]:
                            temporary_captcha = captcha_array[captcha_number]
                            captcha_array[captcha_number] = captcha_array[captcha_number + 1]
                            captcha_array[captcha_number + 1] = temporary_captcha

                # Find average distance between detected symbols
                average = 0
                captcha_len = len(captcha_array) - 1
                while captcha_len > 0:
                    average += captcha_array[captcha_len][1] - captcha_array[captcha_len - 1][1]
                    captcha_len -= 1
                # Increase average distance error
                average = average / (len(captcha_array) + average_distance_error)

                captcha_array_filtered = list(captcha_array)
                captcha_len = len(captcha_array) - 1
                while captcha_len > 0:
                    # if average distance is larger than error distance
                    if captcha_array[captcha_len][1] - captcha_array[captcha_len - 1][1] < average:
                        # check which symbol has higher detection percentage
                        if captcha_array[captcha_len][2] > captcha_array[captcha_len - 1][2]:
                            del captcha_array_filtered[captcha_len - 1]
                        else:
                            del captcha_array_filtered[captcha_len]
                    captcha_len -= 1

                # Get final string from filtered CAPTCHA array
                captcha_string = ""
                for captcha_letter in range(len(captcha_array_filtered)):
                    captcha_string += captcha_array_filtered[captcha_letter][0]

                return captcha_string
