import cv2
import numpy as np
import Image_Prepare as imgprep
import predict_2 as digit_predictor
import os,sys
import shutil
import re
from natsort import natsorted, ns
import Excel_Program as excel
from operator import itemgetter

temp_counter = 0

answer_coordinates = []
def everything(path_to_linear_image, path_to_color_image,path_to_unprepared_images,path_to_prepared_images,path_to_answer_sheets,sheet_number):
    black_linear_img = cv2.imread(path_to_linear_image,0)
    colored_linear_img = cv2.imread(path_to_linear_image)  #For Drawing Contours
    colored_final_img = cv2.imread(path_to_color_image)

    #The black and white scanned image is used to find the location of the digits
    #in the image. Once found, this location is cropped from the colored
    #scanned copy
    ret,thresh = cv2.threshold(black_linear_img,1,255,cv2.THRESH_BINARY_INV)
    kernel = np.ones((10,10),np.uint8)
    dilated = cv2.dilate(thresh,kernel,iterations = 1)
    im2, contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    max_area = 0
    if len(contours)>10:
        ADM_NO = False
        for t in range(len(contours)):
            cnt = contours[t]
            area = cv2.contourArea(cnt)
            x,y,w,h = cv2.boundingRect(cnt)
            ####################Change accordind to final paper########################
            if area>max_area and x+w<black_linear_img.shape[1]/3:
            ###########################################################################
                ci = t
                max_area = area
    else:
        ADM_NO = True
        for t in range(len(contours)):
            cnt = contours[t]
            area = cv2.contourArea(cnt)
            x,y,w,h = cv2.boundingRect(cnt)
            ####################Change accordind to final paper########################
            if area>max_area and x+w>black_linear_img.shape[1]/3:
            ###########################################################################
                ci = t
                max_area = area
    cnt = contours[ci]
    x,y,w,h = cv2.boundingRect(cnt)
    #cv2.drawContours(colored_linear_img, contours, ci, (0,255,0), 3)
    cv2.rectangle(colored_linear_img,(x,y),(x+w,y+h),(0,255,0),2)
##    if x+w>black_linear_img.shape[1]/3: #This implies its the admission number
##        ADM_NO = True
##        global temp_counter
##        cv2.imwrite(str(temp_counter) + '.png',colored_linear_img)
##        temp_counter = temp_counter + 1
##    else:
##        ADM_NO = False
    x,y,w,h = cv2.boundingRect(cnt)
    crop_color_img = colored_final_img[y:y+h, x:x+w]   #For Table
    
    print 'x:',x,' x+w:',x+w,' y:',y,' y+h:',y+h,'        width:',colored_final_img.shape[1],' height:',colored_final_img.shape[0]
    
    crop_black_img = black_linear_img[y:y+h, x:x+w]    #For Table
    
    global temp_counter
    cv2.imwrite(str(temp_counter) + '.png',crop_black_img)
    temp_counter = temp_counter + 1
    
    crop_color_answers_img = colored_final_img[y:y+h, x+w:colored_final_img.shape[1]]   #For cropping answer photos
    cv2.imwrite('cropped_color.jpg',crop_color_img)
    cv2.imwrite('cropped_black.jpg',crop_black_img)
    cv2.imwrite(path_to_answer_sheets + 'cropped_answers.jpg',colored_final_img)
    #Now the part of the image containing the digits has been cropped

    final_black = crop_black_img.copy()
    final_color = crop_color_img.copy()
    final_answers = crop_color_answers_img.copy()
    temp = crop_color_img.copy()
    kernel = np.ones((2,2),np.uint8)
    closing = cv2.morphologyEx(final_black, cv2.MORPH_CLOSE, kernel)  #This removes the light traces of the digits present in the image
    ret,thresh = cv2.threshold(closing,127,255,cv2.THRESH_BINARY)
    im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    ########This parameter needs to be modified according finally decided print############
    max_height_of_digit_box = 200
    min_height_of_digit_box = 10
    max_width_of_digit_box = 200
    ################################################################################

    #Saving the image with boxed digits fot debugging
    for t in range(len(contours)):
        cnt = contours[t]
        x,y,w,h = cv2.boundingRect(cnt)
        if h<max_height_of_digit_box and h>min_height_of_digit_box and w<max_width_of_digit_box:
            cv2.rectangle(temp,(x+4,y),(x+w-4,y+h-7),(0,255,0),1)  #Addition and Subtractions have been made so that the boxes fit the digits 
    #cv2.drawContours(final_color, contours, -1, (0,255,0), 3)

    #Making a list of the contours that contain digits
    contour_list = []
    for t in range(len(contours)):
        cnt = contours[t]
        x,y,w,h = cv2.boundingRect(cnt)
        if h<max_height_of_digit_box and h>min_height_of_digit_box and w<max_width_of_digit_box:
            contour_list.append(t)

    #Grouping contours that have nearly same y value
    error = 10
    already_listed = []
    grouped_contour_list = []
    for a in range(len(contour_list)):
        if a in already_listed:
            continue
        cnt1 = contours[contour_list[a]]
        M = cv2.moments(cnt1)
        if M['m00']!=0:
            cy1 = int(M['m01']/M['m00'])
            for b in range(a+1,len(contour_list)):
                cnt2 = contours[contour_list[b]]
                M = cv2.moments(cnt2)
                if M['m00']!=0:
                    cy2 = int(M['m01']/M['m00'])
                    if abs(cy2-cy1)<error:
                        already_listed.append(a)
                        already_listed.append(b)
                        grouped_contour_list.append([contour_list[a],contour_list[b]])
                        
    #Merging equired elements of grouped_contour_list
    # Example : [1,2] and [1,3] is merged to [1,2,3]
    for a in range(len(grouped_contour_list)):
        if grouped_contour_list[a][0] == -1:
            continue
        for b in range(a+1,len(grouped_contour_list)):
            t1 = grouped_contour_list[a][0]
            t2 = grouped_contour_list[b][0]
            if t1 == t2:
                for c in grouped_contour_list[b]:
                    if c in grouped_contour_list[a]:
                        continue
                    else:
                        grouped_contour_list[a].append(c)
                grouped_contour_list[b][0] = -1

    temp = []
    for a in grouped_contour_list:
        if a[0] == -1:
            continue
        else:
            temp.append(a)
    grouped_contour_list = temp

    #Arranging contours in the list so that the leftmost contours is the first
    #element in each array in the list (ascending value of x for more than 2)
    for a in range(len(grouped_contour_list)):
        for b in range(len(grouped_contour_list[a])):
            for c in range(b+1,len(grouped_contour_list[a])):
                cnt1 = contours[grouped_contour_list[a][b]]
                cnt2 = contours[grouped_contour_list[a][c]]
                x1,y,w,h = cv2.boundingRect(cnt1)
                x2,y,w,h = cv2.boundingRect(cnt2)
                if x2<x1:
                    grouped_contour_list[a][b],grouped_contour_list[a][c] = grouped_contour_list[a][c],grouped_contour_list[a][b]
                    
    
    #Cropping the digits images and storing them
    if ADM_NO == False:   #If page is not the adm no page save in question and marks format
        counter_marks = 1
        counter_questions = 1
        question_filename_vs_y_cood = []  #This is meant for cropping answers from the image in the next section
                                       #it stores the name of the filename of each question box (leftmost incase there are 2 of them) and the y coordinate of
                                       #of the top left corner of that box
        #path_to_unprepared_images = 'Digits/'   Now passes as parameter
        grouped_digit_filename = []  #This stores the image filename for the question
                                     #number and the marks for that question in the
                                     #form of arrays. Example :
        #grouped_digit_filename = [['M_1.png','Q_1A.png','Q_1B.png'],['M_2.png','Q_2A.png']]
        for a in grouped_contour_list:
            counter_question_part = 'A' #Example : Quesion 12 has two digits '1' and '2'. These are stored as Q_12A and Q_12B
            elem = []
            for b in a:
                cnt = contours[b]
                x,y,w,h = cv2.boundingRect(cnt)
                digit_image = final_color[y+7:y+h-7, x+4:x+w-4]
                #digit_image = final_color[y:y+h, x:x+w]
                if b == a[0]:
                    image_name = 'M_' + str(counter_marks) + '.png'
                    cv2.imwrite(path_to_unprepared_images + 'M_' + str(counter_marks) + '.png', digit_image)
                else:
                    image_name = 'Q_' + str(counter_questions) + counter_question_part + '.png'
                    cv2.imwrite(path_to_unprepared_images + 'Q_' + str(counter_questions) + counter_question_part + '.png', digit_image)
                    if counter_question_part == 'A':
                        question_filename_vs_y_cood.append([image_name, y])
                    counter_question_part = chr(ord(counter_question_part)+1)
                elem.append(image_name)
            grouped_digit_filename.append(elem)
            counter_marks = counter_marks + 1
            counter_questions = counter_questions + 1
    elif ADM_NO == True:  #If it is ADM_NO page save images as 1.png, 2.png and so on
        counter_adm = 1
        for a in grouped_contour_list:
            for b in a:
                cnt = contours[b]
                x,y,w,h = cv2.boundingRect(cnt)
                #digit_image = final_color[y:y+h-7, x+4:x+w-4]
                #digit_image = final_color[y:y+h, x:x+w]
                digit_image = final_color[y+7:y+h-7, x+4:x+w-4]
                image_name = str(counter_adm) + '.png'
                cv2.imwrite(path_to_unprepared_images + image_name, digit_image)
                counter_adm = counter_adm + 1

    #Preparing the images to be feeded into MNIST. The images cropped out in
    #the previous step had alot of extra area that was not needed. This part
    #of the program removes the unnecessary area to get better results from
    #MNIST
    #path_to_prepared_images = 'Digits_Prepared/'  Now passed as parameter
    imgprep.image_prepare(path_to_unprepared_images, path_to_prepared_images) #Calls function from the Image_Prepare.py file

    global answer_coordinates #Stores the y coorinates of the starting point of all
                              #answers and also the sheet in which they are present
##    if ADM_NO == False:
##        for filename in os.listdir(path_to_prepared_images):
##            digits_in_filename_1 = re.findall("\d+", filename)
##            if 'M' not in filename or 'A' not in filename or digits_in_filename_1[-1] != '0':
##                continue
##            elem = []
##            
##            for a in question_filename_vs_y_cood:
##                digits_in_filename_2 = re.findall("\d+", a[0])
##                if digits_in_filename_1[0] == digits_in_filename_2[0] :     
##                    elem.append(sheet_number)
##                    elem.append(a[1])
##                    answer_coordinates.append(elem)
##                    break
##    elif ADM_NO == True:
##        answer_coordinates.append([-1])
                
    if ADM_NO == False:  #If its not the adm no page look for questions and marks
        #Predicting the digits using the MNIST dataset
        files_q = []
        files_m = []
        for filename in os.listdir(path_to_prepared_images):
            if 'Q' in filename:
                files_q.append(filename)
            elif 'M' in filename:
                files_m.append(filename)
        files_q = natsorted(files_q, key=lambda y: y.lower())  #Natural Sorting the file names for convenience
        files_m = natsorted(files_m, key=lambda y: y.lower())

        #Grouping the filenames in a grouped list so that each element of the list
        #itself is a list of the the filenames of the images of digits that belong
        #to one box
        #Eg. [['2','Q_2A_1_0.png'], ['3','Q_3A_1_0.png', 'Q_3A_2_1.png'], ['4','Q_4A_1_0.png', 'Q_4A_2_1.png', 'Q_4A_3_2.png']]
        #First element of each nested list denotes the box number
        box_number_completed_m = []
        files_m_grouped = []
        for a in range(len(files_m)):
            elem = []
            digits_in_filename = re.findall("\d+", files_m[a])
            box_number = digits_in_filename[0]
            if box_number in box_number_completed_m:
                continue
            else:
                box_number_completed_m.append(box_number)
                elem.append(box_number)
                elem.append(files_m[a])
            for b in range(a+1,len(files_m)):
                digits_in_filename = re.findall("\d+", files_m[b])
                if digits_in_filename[0] == box_number:
                    elem.append(files_m[b])
            files_m_grouped.append(elem)
        box_number_completed_q = []
        files_q_grouped = []
        for a in range(len(files_q)):
            elem = []
            digits_in_filename = re.findall("\d+", files_q[a])
            box_number = digits_in_filename[0]
            if box_number in box_number_completed_q:
                continue
            else:
                box_number_completed_q.append(box_number)
                elem.append(box_number)
                elem.append(files_q[a])
            for b in range(a+1,len(files_q)):
                digits_in_filename = re.findall("\d+", files_q[b])
                if digits_in_filename[0] == box_number:
                    elem.append(files_q[b])
            files_q_grouped.append(elem)

        #In the above created grouped lists, the filenames are replaces by the digits
        #they contain by predicting the image with the MNIST dataset and all digits
        #present in one box and joined together in a string
        #Eg. ['3','Q_3A_1_0.png', 'Q_3A_2_1.png'] will change to
        #    ['3', '25'] if 'Q_3A_1_0.png' is an image of 2 and 'Q_3A_2_1.png'
        #    is an image of 5
        predicted_numbers_grouped_m = []
        for a in files_m_grouped:
            decimal_counter = 0
            elem = []
            elem.append(a[0])
            final_number = ''
            for b in range(1,len(a)):
                filename = a[b]
                digits_in_filename = re.findall("\d+", filename)
                x = digit_predictor.predict(path_to_prepared_images+filename)
                if str(decimal_counter) == digits_in_filename[-1]:
                    final_number = final_number + str(x)
                else:
                    final_number = final_number + str('.') + str(x)
                    decimal_counter = decimal_counter + 1
            elem.append(final_number)
            predicted_numbers_grouped_m.append(elem)
        predicted_numbers_grouped_q = []
        for a in files_q_grouped:
            decimal_counter = 0
            elem = []
            elem.append(a[0])
            final_number = ''
            for b in range(1,len(a)):
                filename = a[b]
                digits_in_filename = re.findall("\d+", filename)
                x = digit_predictor.predict(path_to_prepared_images+filename)
                if str(decimal_counter) == digits_in_filename[-1]:
                    final_number = final_number + str(x)
                else:
                    final_number = final_number + str('.') + str(x)
                    decimal_counter = decimal_counter + 1
            elem.append(final_number)
            predicted_numbers_grouped_q.append(elem)

        #Combining the question number with the marks by comparing the box numbers
        #Eg. ['1','2'] in questions list and ['1','5'] in marks list are combined
        #as ['1','2','5'] (The box number is kept for later use in excel file
        #After combining the question with the marks the y coordinate of that question in the image
        #is also appended so that it can be used later to crop the answer.
        #So if question 2 had a y coordinate of 252 the final element wil be
        #['1','2','5',252]
        record = []
        unamarked_questions = []
        unamarked_questions.append('UNMARKED_QUESTIONS')
        for a in predicted_numbers_grouped_q:
            elem = []
            elem.append(a[0])
            elem.append(a[1])
            found = False
            for b in predicted_numbers_grouped_m:
                if a[0] == b[0]: #Comparing box numbers
                    elem.append(b[1])
                    found = True
                    break
            for [filename,y_cood] in question_filename_vs_y_cood:
                digits_in_filename = re.findall("\d+", filename)
                if digits_in_filename[0] == a[0]:
                    elem.append(y_cood)
                    break
            if found ==  False:  #There are no marks to the question (Unmarked)
                unamarked_questions.append(elem)
            else:  #Question is marked
                record.append(elem)
        #Sorting record elements in increasing y coordinate order
        print record
        record=sorted(record, key=itemgetter(3))
        if len(unamarked_questions)>1:
            record.append(unamarked_questions)
    elif ADM_NO == True:   #If it is the ADM_NO page then return list has specific format
        files_adm = []
        final_number = ''
        for filename in os.listdir(path_to_prepared_images):
            files_adm.append(filename)
        files_adm.sort()
        record = []
        record.append('D')
        for filename in files_adm:
            x = digit_predictor.predict(path_to_prepared_images+filename)
            final_number = final_number + str(x)
        record.append(final_number)

    return record
        


def main(path_to_linear, path_to_color):
    #path_to_linear = 'AnsLinear3/'
    #path_to_color = 'AnsColor3/'
    files_linear = []
    files_color = []
    spreadsheet = []
    check = os.path.isdir('Digits')
    if check == False:
        os.makedirs('Digits')
    else:
        shutil.rmtree('Digits/')
        os.makedirs('Digits')
    check = os.path.isdir('Digits_Prepared/')
    if check == False:
        os.makedirs('Digits_Prepared/')
    else:
        shutil.rmtree('Digits_Prepared/')
        os.makedirs('Digits_Prepared')
    check = os.path.isdir('Answer_Sheets/')
    if check == False:
        os.makedirs('Answer_Sheets/')
    else:
        shutil.rmtree('Answer_Sheets/')
        os.makedirs('Answer_Sheets')
    for filename in os.listdir(path_to_linear):
        files_linear.append(filename)
    for filename in os.listdir(path_to_color):
        files_color.append(filename)
    files_linear.sort()
    files_color.sort()
    if len(files_linear) != len(files_color):
        print "No. of linear images is not equal to No. of colored images. Exiting..."
        sys.exit()
    for a in range(len(files_linear)):
        sheet_number = a+1
        path_to_unprepared_images = 'Digits/Sheet_' + str(sheet_number) + '/'
        os.makedirs(path_to_unprepared_images)
        path_to_prepared_images = 'Digits_Prepared/Sheet_' + str(sheet_number) + '/'
        os.makedirs(path_to_prepared_images)
        path_to_answer_sheets = 'Answer_Sheets/Sheet_' + str(sheet_number) + '/'
        os.makedirs(path_to_answer_sheets)
        record = everything(path_to_linear + files_linear[a], path_to_color + files_color[a],path_to_unprepared_images,path_to_prepared_images,path_to_answer_sheets,sheet_number)
        spreadsheet.append(record)
    return spreadsheet

path_to_linear = 'AnsLinear7/'
path_to_color = 'AnsColor7/'
spreadsheet = main(path_to_linear, path_to_color)
#excel.create_checking_sheet(spreadsheet)
#excel.create_master_sheet()
