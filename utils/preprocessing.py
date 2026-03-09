import cv2
import numpy as np

def normalize(img):
    return img.astype("float32") / 255.

def resize(img, size=(64, 64)):
    return cv2.resize(img, size)

def prepare(img):
    img = resize(img)
    img = normalize(img)
    img = np.expand_dims(img, axis=0)
    return img
