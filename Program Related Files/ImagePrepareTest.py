import cv2
import numpy as np
import os
for filename in os.listdir('Digits/'):
	black_img = cv2.imread('Digits/' + filename,0)
	color_img = cv2.imread('Digits/' + filename)
	ret,thresh_inv = cv2.threshold(black_img,200,255,cv2.THRESH_BINARY_INV)
	im2, contours, hierarchy = cv2.findContours(thresh_inv,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	_=cv2.drawContours(color_img, contours, -1, (0,255,0), 1)
	for t in range(len(contours)):
		cnt=contours[t]
		M = cv2.moments(cnt)
		if M['m00']!=0:
			cx = int(M['m10']/M['m00'])
			cy = int(M['m01']/M['m00'])
			cv2.circle(color_img,(cx,cy), 2, (0,0,255), -1)
	_=cv2.putText(color_img, str(len(contours)), (color_img.shape[1]-20, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255,2)
	cv2.imwrite('Digits_Prepared/' + filename,color_img)
