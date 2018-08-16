import cv2
import numpy as np
black_img = cv2.imread('5.jpg',0)
gray = cv2.GaussianBlur(black_img, (5, 5), 0)
edged = cv2.Canny(gray, 75, 200)
kernel = np.ones((20,20),np.uint8)
edged = cv2.dilate(edged,kernel,iterations = 1)
colored_img = cv2.imread('5.jpg')
im2, contours, hierarchy = cv2.findContours(edged,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
max_area = 0
max_h = 0
img_area = img.shape[0]*img.shape[1]
for t in range(len(contours)):
    cnt = contours[t]
    area = cv2.contourArea(cnt)
    x,y,w,h = cv2.boundingRect(cnt)
    peri = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
    if h>max_h:
        ci = t
        max_h = h

cnt = contours[ci]
angle = cv2.minAreaRect(cnt)[-1]
if angle < -45:
    angle = (90 + angle)
else:
    angle = -angle
(h, w) = colored_img.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, angle, 1.0)
rotated = cv2.warpAffine(colored_img, M, (w, h),
	flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
#cv2.drawContours(colored_img, contours, -1, (0,255,0), 3)
cv2.imwrite('test1.jpg',edged)
