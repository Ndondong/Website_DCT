import os
import numpy as np
from datetime import datetime

def SlugMaker():
	time = datetime.now()
	time = time.strftime("%Y%m%d%H%M%S")
	return time

def ValidateImage(value):
	ext = os.path.splitext(value.name)[1]
	valid_extensions = ['.png', '.jpg']
	if ext.lower() in valid_extensions:
		return True

def GetExtension(value):
	_, file_extension = value.rsplit('.', 1)
	return str(file_extension.upper())

def GetExtensionImage(value):
	_, file_extension = value.rsplit('.', 1)
	return str(file_extension)
	
def ParameterQuality(image, modf):
	mse = np.mean((image - modf) ** 2)
	if mse == 0:
		return 100, 0
	else:
		max_pixel_value = 255.0
		psnr = 20 * np.log10(max_pixel_value / np.sqrt(mse))
		return psnr, mse