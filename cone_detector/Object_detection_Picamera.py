######## Video Object Detection Using Tensorflow-trained Classifier #########
#
# Second Author: Arthur Telles
# Date: 04/06/18 (DD/MM/YYYY)
# Description: 
# This code was adapted to perform the activity of identifying a traffic cone in a raspberry pi 3.
# Also the angle between the center of the object and the center of the camera is returned.
# Everything was wrapped up in a class to be called by the main control function.
# 
# First Author: Evan Juras
# Date: 1/16/18
# Description: 
# This program uses a TensorFlow-trained classifier to perform object detection.
# It loads the classifier uses it to perform object detection on a video.
# It draws boxes and scores around the objects of interest in each frame
# of the video.

## Some of the code is copied from Google's example at
## https://github.com/tensorflow/models/blob/master/research/object_detection/object_detection_tutorial.ipynb

## and some is copied from Dat Tran's example at
## https://github.com/datitran/object_detector_app/blob/master/object_detection_app.py

import os
import cv2
import picamera
#from picamera import PiCamera, Color
import numpy as np
import tensorflow as tf
import sys
from picamera.array import PiRGBArray

class object_detector():
	def __init__(self,print_results=True, show_image=True):

		# Grab path to tensorflow repository's object detection folder
		TF_OBJ_DET_PATH = os.path.abspath("E:\\models\\research\\object_detection")

		# Appending it to the current folder to import necessary modules
		sys.path.append(TF_OBJ_DET_PATH)

		# Import utilites
		from utils import label_map_util
		from utils import visualization_utils as vis_util

		# current directory path
		CWD = os.getcwd()

		# Grab path to files necessary for object_detection
		DETECTION_FILES_FOLDER = "detection_files"

		# Path to frozen detection graph .pb file, which contains the model that is used
		# for object detection.
		PATH_TO_CKPT = os.path.join(CWD,DETECTION_FILES_FOLDER,'primeira_rede.pb')

		# Path to label map file
		PATH_TO_LABELS = os.path.join(CWD,DETECTION_FILES_FOLDER,'object-detection.pbtxt')

		# Indicate 1 class for traffic cone detection
		NUM_CLASSES = 1

		# Load the label map.
		# Label maps map indices to category names, '1' relates to traffic cone
		# Here we use internal utility functions, but anything that returns a
		# dictionary mapping integers to appropriate string labels would be fine
		label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
		categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
		category_index = label_map_util.create_category_index(categories)

		# Load the Tensorflow model into memory.
		detection_graph = tf.Graph()
		with detection_graph.as_default():
			od_graph_def = tf.GraphDef()
			with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
				serialized_graph = fid.read()
				od_graph_def.ParseFromString(serialized_graph)
				tf.import_graph_def(od_graph_def, name='')

			sess = tf.Session(graph=detection_graph)

		# Define input and output tensors (i.e. data) for the object detection classifier

		# Input tensor is the image
		image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

		# Output tensors are the detection boxes, scores, and classes
		# Each box represents a part of the image where a particular object was detected
		detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

		# Each score represents level of confidence for each of the objects.
		# The score is shown on the result image, together with the class label.
		detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
		detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

		# Number of objects detected
		num_detections = detection_graph.get_tensor_by_name('num_detections:0')

		try:
			camera = picamera.PiCamera(resolution=(640, 480),framerate=10)
			rawCapture=PiRGBArray(camera, size=(640,480))
			#rawCapture = io.BytesIO()
			#camera.start_preview()
			#time.sleep(2)

			for frame in camera.capture_continuous(rawCapture , format='bgr' , use_video_port=True):
				frame2 = frame.array
				image = frame2.copy()
				# Acquire frame and expand frame dimensions to have shape: [1, None, None, 3]
				# i.e. a single-column array, where each item in the column has the pixel RGB value
				frame_expanded = np.expand_dims(image, axis=0)

				# Perform the actual detection by running the model with the image as input
				(boxes, scores, classes, num) = sess.run(
					[detection_boxes, detection_scores, detection_classes, num_detections],
					feed_dict={image_tensor: frame_expanded})

				# Draw the results of the detection (aka 'visulaize the results')
				vis_util.visualize_boxes_and_labels_on_image_array(
					image,
					np.squeeze(boxes),
					np.squeeze(classes).astype(np.int32),
					np.squeeze(scores),
					category_index,
					use_normalized_coordinates=True,
					line_thickness=8,
					min_score_thresh=0.80)
				
				for i in range(0,1):#np.shape(boxes)[1]):
					cv2.rectangle(image, (int(boxes[0,i,1] * np.shape(image)[1]), int(boxes[0,i,0] * np.shape(image)[0])), (int(boxes[0,i,3] * np.shape(image)[1]), int(boxes[0,i,2] * np.shape(image)[0])), (255,0,0), 2)

				width = ((int(boxes[0,i,3] * np.shape(image)[1]) - int(boxes[0,i,1] * np.shape(image)[1]))/2)
				height = ((int(boxes[0,i,2] * np.shape(image)[0]) - int(boxes[0,i,0] * np.shape(image)[0]))/2)

				posX = int(boxes[0,i,1] * np.shape(image)[1] + width)
				posY = int(boxes[0,i,0] * np.shape(image)[0] + height)
				
				# considering the camera has a 140 degress field of view
				angle = ((posX-(image.shape[1]/2))/(image.shape[1]/2))*70
				
				if print_results:
					
					print((int(boxes[0,1,1] * np.shape(image)[1]), int(boxes[0,1,0] * np.shape(image)[0])),\
					(int(boxes[0,1,3] * np.shape(image)[1]), int(boxes[0,1,2] * np.shape(image)[0])))
					
					print("Object Center - X: " + str(posX) + \
										" Y: " + str(posY))

					print("Object Size - Width(Largura): " + str(width) + " pixels" + \
										" Height(Altura): " + str(height) + " pixels")

					print("Angle: " + str(angle) + " degrees")

				if show_image:
				
					# All the results have been drawn on the frame, so it's time to display it.
					cv2.imshow('Object detector', image)
					
					# Press 'q' to quit
					if cv2.waitKey(1) == ord('q'):
						break
					rawCapture.truncate(0)
		finally:
			cv2.destroyAllWindows()
		
		return angle