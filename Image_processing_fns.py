'''
Simple set of image processing utilities. Functionality includes
    - Converting between standard image formats and numpy arrays
    - Options for displaying images using PIL and inline 
        in a jupyter notebook using IPython.display
    - Image resizing
    - Converting to grayscale

Author: Laura Graesser
Version: 1.0
Date: September 2017
'''

import os
import io
from io import BytesIO
import PIL
from PIL import Image as PImage
import numpy as np
from IPython.display import Image, display

def resizeImage(image, size):
    image.thumbnail(size, PIL.Image.ANTIALIAS)
    return image

def resizeImageAlt(image, size):
    newim = image.resize(size, resample=PIL.Image.LANCZOS)
    return newim

def getImage(filename, path):
    fullname = os.path.join(path, filename)
    im = PImage.open(fullname)
    im.load()
    return im

def showImage(filename, path):
    fullname = os.path.join(path, filename)
    display(Image(filename=fullname))

def convertImageToArray(image):
    im_array = np.asarray(image, dtype="float64")
    return im_array

def checkImagePIL(array):
    array = np.asarray(array, dtype="uint8")
    im = PImage.fromarray(array, 'RGB')
    im.show()
    
def displayImageInline(array):
    array = np.asarray(array, dtype="uint8")
    if array.ndim >= 3:
        im = PImage.fromarray(array, 'RGB')
    else:
        im = PImage.fromarray(array)
    bio = BytesIO()
    im.save(bio, format='png')
    display(Image(bio.getvalue(), format='png', embed=True))

def convertToGrayscale(array):
    array_gray = np.dot(array[..., :3], [0.299, 0.587, 0.114])
    return array_gray

def getAndReformatImage(filename, path, scale=0.25, grayscale=False):
    im = getImage(filename, "")
    im_small = resizeImageAlt(im, (int(im.size[0] * scale), int(im.size[1] * scale)))
    arr = convertImageToArray(im_small)
    if grayscale:
        arr = convertToGrayscale(arr)
    arr = arr.astype(int)
    print("Original image dims: {} New dims: {}".format(im.size, arr.shape))
    print("Displaying new image...")
    displayImageInline(arr)
    return arr