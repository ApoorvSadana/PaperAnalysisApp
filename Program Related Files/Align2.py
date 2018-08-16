import cv2
import numpy as np
black_img = cv2.imread('out.jpeg',0)
ret,thresh = cv2.threshold(black_img,1,255,cv2.THRESH_BINARY_INV)
blur = cv2.GaussianBlur(thresh, (5, 5), 0)
#edged = cv2.Canny(blur, 75, 200)
kernel = np.ones((10,10),np.uint8)
dilated = cv2.dilate(blur,kernel,iterations = 1)
#cv2.imwrite('dilated.jpg',dilated)
im2, contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
colored_img = cv2.imread('out.jpeg')
max_area = 0
for t in range(len(contours)):
    cnt = contours[t]
    area = cv2.contourArea(cnt)
    x,y,w,h = cv2.boundingRect(cnt)
    if area>max_area and w<black_img.shape[1]/2:
        ci = t
        max_area = area

cnt = contours[ci]
angle = cv2.minAreaRect(cnt)[-1]
angle = angle
(h, w) = colored_img.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, angle, 1.0)
rotated = cv2.warpAffine(colored_img, M, (w, h),
	flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
cv2.imwrite('test1.jpg',rotated)

black_img = cv2.imread('test1.jpg',0)
colored_img = cv2.imread('test1.jpg')
ret,thresh = cv2.threshold(black_img,1,255,cv2.THRESH_BINARY_INV)
blur = cv2.GaussianBlur(thresh, (5, 5), 0)
#edged = cv2.Canny(blur, 75, 200)
dilated = cv2.dilate(blur,kernel,iterations = 1)
im2, contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
max_area = 0
for t in range(len(contours)):
    cnt = contours[t]
    area = cv2.contourArea(cnt)
    x,y,w,h = cv2.boundingRect(cnt)
    if area>max_area and w<black_img.shape[1]/2:
        ci = t
        max_area = area
cnt = contours[ci]
x,y,w,h = cv2.boundingRect(cnt)
h = colored_img.shape[0]
crop_img = colored_img[y:y+h, x:x+w]
cv2.imwrite('cropped.jpg',crop_img)
