import cv2
import numpy as np
import os

def image_prepare(path_to_unprepared_images, path_to_prepared_images):
    for filename in os.listdir(path_to_unprepared_images):
        black_img = cv2.imread(path_to_unprepared_images + filename,0)
        color_img = cv2.imread(path_to_unprepared_images + filename) #Only for drawing contours
        ret,thresh_inv = cv2.threshold(black_img,200,255,cv2.THRESH_BINARY_INV)
        im2, contours, hierarchy = cv2.findContours(thresh_inv,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(color_img, contours, -1, (0,255,0), 3)
        new_contours_list = contours
        ######################These values will change when paper is designed############
        min_x_cood_of_digit = 5
        max_x_cood_of_digit = black_img.shape[1]-5
        for t in range(len(contours)):
            cnt = contours[t]
            x,y,w,h = cv2.boundingRect(cnt)
            if x<min_x_cood_of_digit or x>max_x_cood_of_digit:
                for b in range(len(new_contours_list)):
                    if contours[t] == new_contours_list[b]:
                        new_contours_list = np.delete(new_contours_list,b,0)
                        break
        contours = new_contours_list
        if len(contours) == 0:
            continue
        max_area = 0
        for t in range(len(contours)):
            cnt = contours[t]
            area = cv2.contourArea(cnt)
            if area>max_area:
                max_area = area
                ci = t
        cnt = contours[ci]
        x,y,w,h = cv2.boundingRect(cnt)
        if h<5:
            continue    #If height of contour is less than 5 than the contour
                        #is just a noise and not digit
        x,y,w,h = cv2.boundingRect(cnt)
        digit_image_resized = black_img[y:y+h, x:x+w]
        cv2.imwrite(path_to_prepared_images + filename,digit_image_resized)
