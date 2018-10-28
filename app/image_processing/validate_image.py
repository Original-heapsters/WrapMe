import dlib
import numpy as np
import os
from PIL import Image


detector = dlib.get_frontal_face_detector()
predictor_dat = os.path.join(os.path.dirname(__file__), 
							 'shape_predictor_68.dat')
predictor = dlib.shape_predictor(predictor_dat)


def has_face(image):
	"""
	Returns the coordinates of the head if a head is detected 
	otherwise returns None
	:params image: file path to an image file
	"""
	if not os.path.exists(image):
		raise IOError('Image: %s does not exist' % os.path.abspath(image))
	
	img = Image.open(image)

	img_gray = np.array(img.convert('L'))

	rects = detector(img_gray, 0)

	if len(rects):
		return rects
	else:
 		return None