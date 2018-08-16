import cv2
import numpy as np
from resizeimage import resizeimage
import os
from PIL import Image
import subprocess
from scipy import ndimage


y_cood_list = []
contour_no_list = []
y_cood_list_temp = []

frame = cv2.imread("cropped.jpg")
adapt = cv2.adaptiveThreshold(black_img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)
ret,thresh = cv2.threshold(black_img,127,255,cv2.THRESH_BINARY_INV)
im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
first_time = 1
for t in range(len(contours)):
    appended = 0
    cnt = contours[t]
    area = cv2.contourArea(cnt)
    x,y,w,h = cv2.boundingRect(cnt)
    hull = cv2.convexHull(cnt)
    hull_area = cv2.contourArea(hull)
    if h<50 and w<50 and h>5 and w>5:
        M = cv2.moments(cnt)
        if M['m00']!=0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
        else:
            continue
        if first_time == 1:
            y_cood_list.append(cy)
            contour_no_list.append([t])
            #y_cood_list_temp = y_cood_list
            first_time = 0
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)
            cv2.putText(frame, str(t), (cx+200, cy),cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255,2)
            continue
        for x in range(len(y_cood_list)):
            if abs(cy-y_cood_list[x])<10:
                contour_no_list[x].append(t)
                appended = 1
        if appended == 0:
            contour_no_list.append([t])
            y_cood_list.append(cy)
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),-1)
        cv2.putText(frame, str(hull_area), (cx+200, cy),cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255,2)
cv2.imwrite('inrange.jpg',mask)
cv2.imwrite('image.jpg',frame)

frame = cv2.imread('image.jpg')
inrange = cv2.inRange(frame, lgreen, hgreen)
cv2.imwrite('inrange2.jpg',inrange)
counter=0
check_marks_or_ques=0


contour_no_list_modified = []
for t in range(len(contour_no_list)):
    if len(contour_no_list[t])==2:
	    contour_no_list_modified.append(contour_no_list[t])

for t in range(len(contour_no_list_modified)):
    cnt1=contours[contour_no_list_modified[t][0]]
    cnt2=contours[contour_no_list_modified[t][1]]
    x1,y,w,h = cv2.boundingRect(cnt1)
    x2,y,w,h = cv2.boundingRect(cnt2)
    if x2<x1:
        contour_no_list_modified[t][0],contour_no_list_modified[t][1] = contour_no_list_modified[t][1],contour_no_list_modified[t][0]

counter_temp=0
black_img=np.zeros((28,28), np.uint8)
ret,white_img = cv2.threshold(black_img,127,255,cv2.THRESH_BINARY_INV)
for t in contour_no_list_modified:
    check_marks_or_ques=0
    for u in t:
        cnt=contours[u]
        x,y,w,h = cv2.boundingRect(cnt)
        crop_img = mask[y:y+h,x:x+w]
        cv2.imwrite('Cropped/' + str(counter_temp)+'.jpg',crop_img)
        counter_temp=counter_temp + 1
        #crop_img = cv2.resize(crop_img, (28, 28)) 
        opened = cv2.morphologyEx(crop_img, cv2.MORPH_OPEN, kernel)
        #crop_img = cv2.dilate(crop_img,kernel,iterations = 1)
        ret,inv_img = cv2.threshold(crop_img,127,255,cv2.THRESH_BINARY_INV)
        kernel = np.ones((5,5),np.uint8)
        #inv_img = ndimage.binary_fill_holes(inv_img,structure=np.ones((100,100))).astype(int)
        #inv_img = cv2.dilate(inv_img,kernel,iterations = 1)
        #inv_img = cv2.GaussianBlur(inv_img,(5,5),0)
        if check_marks_or_ques==0: 
            cv2.imwrite('Digits/'+str(counter)+'_marks.png',inv_img)
            check_marks_or_ques=check_marks_or_ques+1
        else:
            cv2.imwrite('Digits/'+str(counter)+'_question.png',inv_img)
    counter=counter+1

result=subprocess.check_output('python Predicting_Digit.py', shell=True)
digits=[]
for t in result:
    if t.isdigit() == True:
        digits.append(int(t))

digits_final=[]
counter=0
no_of_elem=0
for t in digits:
    if counter==0:
        digits_final.append([t])
        counter=1
        continue
    if counter==1:
        digits_final[no_of_elem].append(t)
        no_of_elem=no_of_elem+1
        counter=0
        continue
      
