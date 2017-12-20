# -*- coding: UTF-8 -*-
import cv2
import numpy as np
import sys
from matplotlib import pyplot as plt
from PIL import Image


if '__main__' == __name__:
    watermark_image_path = 'resources/AdobeStock/watermark/W.png'
    watermark_alpha_path = 'resources/AdobeStock/watermark/alpha.png'

    source_image_path = 'resources/images/tumblr_lxz9uzIE451r3rsfmo1_1280.jpg'

    watermark_position = (0, 0)

    watermark_image = cv2.imread(watermark_image_path)
    alpah_image = cv2.imread(watermark_alpha_path) / 255.0
    source_image = cv2.imread(source_image_path)
    source_image_roi = source_image[
        watermark_position[0]:watermark_position[0] +
        watermark_image.shape[0],
        watermark_position[1]:watermark_position[1] +
        watermark_image.shape[1],
     :]

    print 'watermark size is: ', watermark_image.shape
    print 'alpha size is: ', alpah_image.shape
    print 'source image size is:', source_image.shape
    print 'source image roi size is: ', source_image_roi.shape

    watermarked_image = watermark_image * alpah_image + (
        np.ones(alpah_image.shape) - alpah_image) * source_image_roi
    source_image[watermark_position[0]:watermark_position[0] + watermark_image.shape[0], watermark_position[1]:watermark_position[1] + watermark_image.shape[1], :] = watermarked_image
    cv2.imwrite("./test.jpg", source_image)
    plt.imshow(source_image)
    plt.show()
