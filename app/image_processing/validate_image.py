from PIL import Image
import dlib
import numpy as np


detector = dlib.get_frontal_faclinux e_detector()
predictor = dlib.shape_predictor('shape_predictor_68.dat')


def has_face(image):
	"""
	Returns the coordinates of the head if a head is detected 
	otherwise returns None
	:params image: file path to an image file
	"""
	img = Image.open(image)

	img_gray = np.array(img.convert('L'))

	rects = detector(img_gray, 0)

	if len(rects):
		return rects
	else:
 		return None