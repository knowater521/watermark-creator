# -*- coding: UTF-8 -*-
import cv2
import numpy as np
import argparse
import os
from matplotlib import pyplot as plt


if '__main__' == __name__:
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument(
        '-W',
        '--watermark',
        help='watermark image',
     required=True)
    args_parser.add_argument(
        '-a',
        '--alpha',
        help='watermark alpha image',
     required=True)
    args_parser.add_argument(
        '-s',
        '--source',
        help='source image dir or path',
     required=True)
    args_parser.add_argument(
        '-p',
        '--position',
        help='watermark position file path',
     required=True)
    args_parser.add_argument(
        '-r',
        '--result',
        help='dir for watermarked images',
     required=True)
    args = args_parser.parse_args()

    watermark_image_path = args.watermark
    #watermark_image_path = 'resources/AdobeStock/watermark/W.png'
    watermark_alpha_path = args.alpha
    #watermark_alpha_path = 'resources/AdobeStock/watermark/alpha.png'

    source_image_dir = args.source
    watermark_position_path = args.position

    #source_image_path = 'resources/images/tumblr_lxz9uzIE451r3rsfmo1_1280.jpg'

    #watermark_position = (0, 0)

    watermark_position_list = None
    with open(watermark_position_path, 'r') as _position_f:
        lines = _position_f.readlines()
        assert len(lines) > 0, 'Position format error...'
        watermark_position_list = dict()
        for line in lines:
            line = line.strip('\n')
            words = line.split(',')
            watermark_position_list[words[0]] = (int(words[1]), int(words[2]))

    watermark_image = cv2.imread(watermark_image_path)
    alpah_image = cv2.imread(watermark_alpha_path) / 255.0


    for img_name in watermark_position_list.keys():
        source_image = cv2.imread(os.path.join(source_image_dir, img_name))
        watermark_position = watermark_position_list[img_name]
        source_image_roi = source_image[
            watermark_position[0]:watermark_position[0] +
            watermark_image.shape[0],
            watermark_position[1]:watermark_position[1] +
            watermark_image.shape[1],
        :]

        print 'watermark size is: ', watermark_image.shape
        print 'alpha size is: ', alpah_image.shape
        print 'source image: ', os.path.join(source_image_dir, img_name)
        print 'source image size is:', source_image.shape
        print 'source image roi size is: ', source_image_roi.shape

        watermarked_image = watermark_image * alpah_image + (
            np.ones(alpah_image.shape) - alpah_image) * source_image_roi
        source_image[
            watermark_position[0]:watermark_position[0] +
            watermark_image.shape[0],
            watermark_position[1]:watermark_position[1] +
            watermark_image.shape[1],
        :] = watermarked_image

        cv2.imwrite(os.path.join(args.result, img_name), source_image)
