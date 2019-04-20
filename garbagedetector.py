# -*- coding: utf-8 -*-
#https://pysource.com/2018/07/27/check-if-a-set-of-images-match-the-original-one-with-opencv-and-python/
#https://stackoverflow.com/questions/52305578/sift-cv2-xfeatures2d-sift-create-not-working-even-though-have-contrib-instal
# Author - Raghu Prasad K S

import cv2
import numpy as np
import glob
 
import urllib.request

import datetime
import time


url='http://192.168.43.1:8080/shot.jpg'
current_milli_time = lambda: int(round(time.time() * 1000))

print('start ', current_milli_time())


while True:
    time.sleep(10)
# Use urllib to get the image from the IP camera
    imgResponse = urllib.request.urlopen(url)
 
 # Numpy to convert into a array
    imgNp = np.array(bytearray(imgResponse.read()),dtype=np.uint8)
 
 # Decode the array to OpenCV usable format
    img = cv2.imdecode(imgNp,-1)
    date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    print(date)
 
 # put the image on screen
    #cv2.imshow('IPWebcam',img)
    date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    
    write_name = date +'-loc1.jpg'
    print(write_name)
    
    cv2.imwrite(write_name, img)
    original = cv2.imread(write_name)
 
# Sift and Flann
    sift = cv2.xfeatures2d.SIFT_create()
    kp_1, desc_1 = sift.detectAndCompute(original, None)
 
    index_params = dict(algorithm=0, trees=5)
    search_params = dict()
    flann = cv2.FlannBasedMatcher(index_params, search_params)
 
# Load all the images
    all_images_to_compare = []
    titles = []
    for f in glob.iglob("images\*"):
        image = cv2.imread(f)
        titles.append(f)
        all_images_to_compare.append(image)
        print('image to compare', titles)
        print('First loop ', current_milli_time())
 
    for image_to_compare, title in zip(all_images_to_compare, titles):
    # 1) Check if 2 images are equals
        #print('Second loop start', current_milli_time())
        if original.shape == image_to_compare.shape:
            print("The images have same size and channels")
            difference = cv2.subtract(original, image_to_compare)
            b, g, r = cv2.split(difference)
 
            if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                print("Similarity: 100% (equal size and channels)")
                break
        #print('Second loop End', current_milli_time())
    # 2) Check for similarities between the 2 images
        kp_2, desc_2 = sift.detectAndCompute(image_to_compare, None)
 
        matches = flann.knnMatch(desc_1, desc_2, k=2)
 
        good_points = []
        for m, n in matches:
            #print('Thrid loop Start', current_milli_time())
#        if m.distance &amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;lt; 0.6*n.distance:
            if m.distance < 0.6*n.distance:
                good_points.append(m)
 
        number_keypoints = 0
#    if len(kp_1) &amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;lt;= len(kp_2):
        if len(kp_1) <= len(kp_2):
            number_keypoints = len(kp_1)
        else:
            number_keypoints = len(kp_2)
 
 
        print("Title: " + title)
        percentage_similarity = len(good_points) / number_keypoints * 100
        print("Similarity: " + str(int(percentage_similarity)) + "\n")
        