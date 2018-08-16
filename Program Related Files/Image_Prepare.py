import cv2
import numpy as np
import os

def image_prepare(path_to_unprepared_images, path_to_prepared_images):
    for filename in os.listdir(path_to_unprepared_images):
        black_img = cv2.imread(path_to_unprepared_images + filename,0)
        color_img = cv2.imread(path_to_unprepared_images + filename) #Only for drawing contours
        ret,thresh_inv = cv2.threshold(black_img,200,255,cv2.THRESH_BINARY_INV)
        im2, contours, hierarchy = cv2.findContours(thresh_inv,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(color_img, contours, -1, (0,255,0), 3)

        #Eliminating boxes with no digits
        if len(contours) == 0:
            continue

##        #To check if all the contours have at least one point which is
##        #somewhere in middle of image. If not then the contour is probabaly the edge of the table that has come into the image (false contour)
##        #All false contour found are removed from the list of contours
##        temp_contours_list = []
##        for t in range(len(contours)):
##            cnt = contours[t]
##            false_contour = True
##            for [[x,y]] in cnt:
##                ##################Change this according to finally designed sheet##################################################
##                if x>0.2*black_img.shape[1] and x<0.8*black_img.shape[1] and y>0.2*black_img.shape[0] and y<0.8*black_img.shape[0]:
##                ###################################################################################################################
##                    false_contour = False
##                    break
##            if false_contour == True:
##                pass
##            else:
##                temp_contours_list.append(cnt)
##
##        contours = list(temp_contours_list)  #To ensure that the list is copied and not referenced
                    
        #Finding contours with maximum area
        max_area = 0
        for t in range(len(contours)):
            cnt = contours[t]
            x,y,w,h = cv2.boundingRect(cnt)
            area = cv2.contourArea(cnt)
            if area>=max_area:
                max_area = area
                ci = t
        cnt = contours[ci]

        #If height of contour is less than 5 than the contour is just a noise and not digit
        x,y,w,h1 = cv2.boundingRect(cnt)
        if h1<5:
            continue

        #Once the contour with the maximum area has been found the program looks
        #for contours having height similar to the contour with max area
        h_difference = 7  #Maximum Difference in the heights of contour of
                          #max area and the other contours (which are digits
                          #but dont have the maximum area)
        contour_list = [] #List having the indices of contours which
                          #are digits
        contour_list.append(ci) #The contour with max area (which has to be a
                                #digit is added to the list
        #####The above value might change when the final paper is designed######
        for t in range(len(contours)):
            if t == ci:
                continue
            cnt = contours[t]
            x,y,w,h2 = cv2.boundingRect(cnt)
            if abs(h2-h1)<h_difference:
                contour_list.append(t)

        #Arranging contours in the list so that the leftmost contours is the first
        #element in each array in the list (ascending value of x for more than 2)
        for a in range(len(contour_list)):
            for b in range(a+1,len(contour_list)):
                cnt1 = contours[contour_list[a]]
                cnt2 = contours[contour_list[b]]
                x1,y,w,h = cv2.boundingRect(cnt1)
                x2,y,w,h = cv2.boundingRect(cnt2)
                if x2<x1:
                    contour_list[a],contour_list[b] = contour_list[b],contour_list[a]

        #Finding out where the decimal point exists (if any) by looking for
        #a contour in between any two digits. If there is a decimal point
        #and -1 is added between the indices of those two contours in
        #contour_list
        contour_list_after_decimal_check = contour_list[:]
        for a in range(len(contour_list)-1):
            cnt1 = contours[contour_list[a]]
            M = cv2.moments(cnt1)
            cx1 = int(M['m10']/M['m00'])
            cy1 = int(M['m01']/M['m00'])
            cnt2 = contours[contour_list[a+1]]
            M = cv2.moments(cnt2)
            cx2 = int(M['m10']/M['m00'])
            cy2 = int(M['m01']/M['m00'])
            for b in range(len(contours)):
                cnt3 = contours[b]
                M = cv2.moments(cnt3)
                if M['m00']!= 0:
                    cx3 = int(M['m10']/M['m00'])
                    cy3 = int(M['m01']/M['m00'])
                    if cx3>cx1 and cx3<cx2:
                        for c in range(len(contour_list_after_decimal_check)):
                            if contour_list_after_decimal_check[c] == contour_list[a+1]:
                                contour_list_after_decimal_check.insert(c,-1)
                                break               
        #Cropping the smallest vertical rectangle around each digit and saving
        #the image in path_to_prepared_images
        digit_counter = 1 #counts the number of digits in a box
        decimal_counter = 0 #counts the number of decimal points in a box
                            #there can be two or more decimal points
                            #if a question has sub sub parts. Eg : 5.1.2
        for t in contour_list_after_decimal_check:
            if t == -1:
                decimal_counter = decimal_counter + 1
                continue
            cnt = contours[t]
            x,y,w,h = cv2.boundingRect(cnt)
            digit_image_resized = black_img[y:y+h, x:x+w]
            filename_without_png = filename.replace('.png','')
            #Image storing format :
            # (Letter)_(Box Index)_(Digit Index)_(Decimal Index)
            # Letter : 'Q' stands for question and 'M' stands for Marks
            # Box Index : This is the number of the box in the image of the answer script. Both 'Q' and 'M' have there
            #             own  list starting from 0. For Q each number is followed by an alphabet with 'A' referring
            #             to the first box after marks box, 'B' for the second and so on.
            # Digit Index : In each box there can be multiple digits. The left most digit is indexed 0. The second
            #               leftmost 2 and so on
            # Decimal Index : As there can be multiple decimals (eg. when there are sub sub parts of question like
            #                 5.1.2), decimal index refers to the number of decimal places before each digit in a
            #                 box
            cv2.imwrite(path_to_prepared_images + filename_without_png + '_' + str(digit_counter) + '_' + str(decimal_counter) + '.png',digit_image_resized)
            digit_counter = digit_counter + 1
