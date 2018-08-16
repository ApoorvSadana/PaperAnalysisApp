import cv2
import numpy as np
import xlsxwriter
import re
import os
import pandas
import math
import sys

#######Change this value if required#########################
path_to_unprepared_folders = 'Digits/'
#############################################################

def increment_char(c):
	return chr(ord(c) + 1) if c != 'Z' else 'A'

def increment_str(s):
	    lpart = s.rstrip('Z')
	    num_replacements = len(s) - len(lpart)
	    new_s = lpart[:-1] + increment_char(lpart[-1]) if lpart else 'A'
	    new_s += 'A' * num_replacements
	    return new_s

def create_checking_sheet(spreadsheet):
    sheets = [] #Stores the name of the sheet folders
    for filename in os.listdir(path_to_unprepared_folders):
        sheets.append(filename)
    sheets.sort()
    if len(spreadsheet) != len(sheets):   #If the number of folders (each folder contains the images of boxes in one paper) is not equal to records
                                          #exit the program
        sys.exit()
    workbook = xlsxwriter.Workbook('CheckSheet.xlsx',)
    worksheet = workbook.add_worksheet()
    worksheet.set_column(0, 4, 10)
    worksheet.set_default_row(50)
    worksheet.set_row(0, 100)
    format_normalcell = workbook.add_format()
    format_heading = workbook.add_format()
    format_normalcell.set_text_wrap()
    format_heading.set_text_wrap()
    format_ignore_column = workbook.add_format()
    format_ignore_column.set_bg_color('#08d700')
    format_ignore_column.set_text_wrap()
    worksheet.write(0, 0, "Computer Generated Question", format_heading)
    worksheet.write(0, 1, "Computer Generated Marks", format_heading)
    worksheet.write(0, 2, "Actual Question", format_heading)
    worksheet.write(0, 3, "Actual Marks", format_heading)
    worksheet.write(0, 5, "Ignore After This", format_heading)
    worksheet.set_column(5,5, 20, format_ignore_column)
    worksheet.write(0, 6, "Type", format_heading)
    worksheet.write(0, 7, "Sheet Number", format_heading)
    worksheet.write(0, 8, "Y-COOD", format_heading)
    row_counter = 1
    for a in range(len(sheets)):
        filename = sheets[a]
        path_to_unprepared_images = path_to_unprepared_folders + filename + '/'
        record = spreadsheet[a]
        if isinstance(record[0],list):   #The record is not that of an adm no as first element of adm record is 'D' which is a string
            files_q = []
            files_m = []
            for filename in os.listdir(path_to_unprepared_images):
                if 'Q' in filename:
                    files_q.append(filename)
                elif 'M' in filename:
                    files_m.append(filename)
            counter_q = 0
            counter_m = 0
            for b in range(len(record)):
                nested_list = record[b]
                if nested_list[0] == 'UNMARKED_QUESTIONS':
                        #worksheet.write(row_counter, 0, 'UNMARKED QUESTIONS', format_normalcell)
                        row_counter = row_counter + 1
                        for c in range(len(nested_list)):
                                if isinstance(nested_list[c],list):  #Unmarked questions are stored like ['UNMARKED_QUESTION',['1','4'],['10','3']]
                                                                #wherein [a,b] a refers to box number and b refers to computer predicted question
                                                                #this if is just to skip first elements of nested_list i.e. 'UNMARKED_QUESTION'
                                        worksheet.write(row_counter, 0, nested_list[c][1], format_normalcell)
                                        for filename in files_q:
                                                digits_in_filename = re.findall("\d+", filename)
                                                if nested_list[c][0] == digits_in_filename[0]:
                                                        worksheet.insert_image(row_counter,1, path_to_unprepared_images + filename)
                                        worksheet.write(row_counter, 6, 'UQ', format_normalcell)
                                        worksheet.write(row_counter, 7, str(a+1), format_normalcell)
                                        worksheet.write(row_counter, 8, nested_list[c][2], format_normalcell)
                                        row_counter = row_counter + 1
                        continue
                worksheet.write(row_counter, 0, nested_list[1], format_normalcell)
                worksheet.write(row_counter, 1, nested_list[2], format_normalcell)
                worksheet.write(row_counter, 7, str(a+1), format_normalcell)
                worksheet.write(row_counter, 6, 'QvM', format_normalcell)
                worksheet.write(row_counter, 8, nested_list[3], format_normalcell)
                for filename in files_q:
                    digits_in_filename = re.findall("\d+", filename)
                    if nested_list[0] == digits_in_filename[0]:
                        worksheet.insert_image(row_counter,2, path_to_unprepared_images + filename)
                for filename in files_m:
                    digits_in_filename = re.findall("\d+", filename)
                    if nested_list[0] == digits_in_filename[0]:
                        worksheet.insert_image(row_counter,3, path_to_unprepared_images + filename)
                
                row_counter = row_counter + 1
        elif isinstance(record[0],str):   #The record is an adm no. This indicates start of a new paper
            worksheet.write(row_counter, 6, "END", format_normalcell)
            row_counter = row_counter + 2
            worksheet.set_row(row_counter, 100)
            worksheet.write(row_counter, 0, record[1], format_normalcell)
            files_adm = []
            for filename in os.listdir(path_to_unprepared_images):
                files_adm.append(filename)
            files_adm.sort()
            column_counter = 1
            for filename in files_adm:
                worksheet.insert_image(row_counter,column_counter, path_to_unprepared_images + filename)
                column_counter = column_counter + 1
            worksheet.write(row_counter, 6, 'ADM Number', format_normalcell)
            row_counter = row_counter + 1         
    workbook.close()

def create_master_sheet(text, path_to_save):
    #Collecting data from CheckSheet
    df = pandas.read_excel('CheckSheet.xlsx')
    row_type = df['Type'].values
    questions = df['Computer Generated Question'].values
    marks = df['Computer Generated Marks'].values
    sheet_no = df['Sheet Number'].values
    y_cood = df['Y-COOD'].values
    questions = questions.tolist()
    marks = marks.tolist()
    row_type = row_type.tolist()
    sheet_no = sheet_no.tolist()
    y_cood = y_cood.tolist()
    record_started = False
    record = []
    final_spreadsheet = []
    unmarked_questions = []
    unmarked_questions.append('UNMARKED QUESTIONS')
    for a in range(len(row_type)):
        if row_type[a] == 'ADM Number':
            record.append(int(questions[a]))   #This is actually the ADM number
            record_started = True
        elif row_type[a] == 'QvM':
            record.append([questions[a],marks[a],sheet_no[a],y_cood[a]])
        elif row_type[a] == 'UQ':
            unmarked_questions.append([questions[a],sheet_no[a],y_cood[a]])
        elif row_type[a] == 'END' and record_started == True:
            record_started = False
            if len(unmarked_questions)>1:
                record.append(unmarked_questions)
            final_spreadsheet.append(record)
            unmarked_questions = []
            unmarked_questions.append('UNMARKED QUESTIONS')
            record = []
            
    if len(unmarked_questions)>1:
            record.append(unmarked_questions)
    final_spreadsheet.append(record)  #To append last record
    print final_spreadsheet
    #Buidling new excel file
    workbook = xlsxwriter.Workbook(path_to_save)
    worksheet = workbook.add_worksheet('Master')
    answer_sheet = workbook.add_worksheet('Answer Sheets')
    format_normalcell = workbook.add_format()
    format_normalcell.set_text_wrap()
    format_normalcell.set_align('center')
    format_heading = workbook.add_format({
    'bold':     True,
    'border':   6,
    'align':    'center',
    'valign':   'vcenter',
    'fg_color': '#C0C0C0',
    })
    worksheet.write(0, 0, "ADM NO", format_heading)
    text = text.split('\n')
    text = [t.encode('utf-8') for t in text]
    questions_mastersheet = []
    for a in text:
        if '-' not in a:
            questions_mastersheet.append(a)
        elif '-' in a:
            question_vs_subpart = a.split('-')   #Creates array ['A','B'] where A is question number and B is number of subparts
            questions_extracted = [question_vs_subpart[0] + '.' + str(t+1) for t in range(int(question_vs_subpart[1]))]
            #questions extracted is an array of the question numbers (sub parts included). Eg. the [A,B] above is converted to ['A.1','A.2',...'A.B']
            for t in questions_extracted:
                questions_mastersheet.append(t)
    qustions_last_cell_alphabet_for_merging = 'B'
    for a in range(len(questions_mastersheet)-1): 
        qustions_last_cell_alphabet_for_merging = increment_str(qustions_last_cell_alphabet_for_merging)
    qustions_last_cell_for_merging = qustions_last_cell_alphabet_for_merging + '1'
    worksheet.merge_range('B1:' + qustions_last_cell_for_merging, "Questions",format_heading)
    total_cell_alphabet = increment_str(qustions_last_cell_alphabet_for_merging)
    total_cell = total_cell_alphabet + '1'
    worksheet.write(total_cell, "Total", format_heading)
    #Writing questions on excel sheet
    questions_mastersheet = map(float,questions_mastersheet)
    questions_mastersheet_with_column_no = []
    for a in range(len(questions_mastersheet)):
        worksheet.write(1, a+1, str(questions_mastersheet[a]), format_normalcell)
        questions_mastersheet_with_column_no.append([questions_mastersheet[a],a+1])
    
    #Entering the records
    url_format = workbook.add_format({
    'font_color': 'blue',
    'underline':  1
    })
    row_counter_master = 2
    row_counter_ans_sheet = 2
    sheets_already_added = []
    sheet_no_vs_cell = []
    for record in final_spreadsheet:
        total = 0
        attempted_questions = []
        for a in record:
            if isinstance(a,int):  #Adm no
                worksheet.write(row_counter_master, 0, record[0], format_normalcell)
            else:
                went_in_unmarked_loop = False
                if a[0] == 'UNMARKED QUESTIONS':
                        went_in_unmarked_loop = True
                        for c in a:
                            if isinstance(c, list):  # Format is ['UNMARKED QUESTIONS',[question,sheet_no,y_cood],... n records]
                                question = c[0]
                                sheet_no_for_ans = int(c[1])
                                y_cood_for_ans = c[2]
                                for b in questions_mastersheet_with_column_no:
                                    if b[0] == question:
                                        attempted_questions.append(b[0])
                                        print attempted_questions
                                        if sheet_no_for_ans not in sheets_already_added:
                                                cell_to_insert_image = 'B' + str(row_counter_ans_sheet)
                                                answer_sheet.insert_image(cell_to_insert_image,'Answer_Sheets/Sheet_'+ str(sheet_no_for_ans)+ '/cropped_answers.jpg', {'x_scale': 0.5,'y_scale': 0.5})
                                                sheet_no_vs_cell.append([sheet_no_for_ans,cell_to_insert_image])
                                                cell_to_be_linked = 'D' + str(row_counter_ans_sheet+ 11)  # It is different from cell_to_insert_image to ensure that the linked

                                                                                               # cell is at centre of image. So when the teacher click on the marks to
                                                                                               # view the answer the entire image is seen. If the top left cell
                                                                                               # of image is linked (cell_to_insert_image) then teacher needs to scroll
                                                                                               # a little bit

                                                sheets_already_added.append(sheet_no_for_ans)
                                                row_counter_ans_sheet = row_counter_ans_sheet + 32
                                        else:
                                                for d in sheet_no_vs_cell:
                                                        if d[0] == sheet_no_for_ans:
                                                                cell_to_be_linked = d[1]
                                        worksheet.write_url(row_counter_master, b[1],"internal:'Answer Sheets'!"+ cell_to_be_linked, url_format,'UNMARKED')
                                        break
                if went_in_unmarked_loop == True:
                        continue
                question = a[0]
                mark_for_question = a[1] #marks variable is already used hence this name
                sheet_no_for_ans = int(a[2])
                y_cood_for_ans = a[3]
                found = False
                total = total + mark_for_question
                for b in questions_mastersheet_with_column_no:
                    if b[0] == question:
                        attempted_questions.append(b[0])
                        #worksheet.write(row_counter, b[1], mark_for_question, format_normalcell)
                        if sheet_no_for_ans not in sheets_already_added:
                            cell_to_insert_image = "B" + str(row_counter_ans_sheet)
                            answer_sheet.insert_image(cell_to_insert_image, 'Answer_Sheets/Sheet_' + str(sheet_no_for_ans) + '/cropped_answers.jpg', {'x_scale': 0.5, 'y_scale': 0.5})
                            sheet_no_vs_cell.append([sheet_no_for_ans,cell_to_insert_image])
                            cell_to_be_linked = "D" + str(row_counter_ans_sheet + 11)  #It is different from cell_to_insert_image to ensure that the linked
                                                                                       #cell is at centre of image. So when the teacher click on the marks to
                                                                                       #view the answer the entire image is seen. If the top left cell
                                                                                       #of image is linked (cell_to_insert_image) then teacher needs to scroll
                                                                                       #a little bit
                            sheets_already_added.append(sheet_no_for_ans)
                            row_counter_ans_sheet = row_counter_ans_sheet + 32
                        worksheet.write_url(row_counter_master, b[1], "internal:'Answer Sheets'!" + cell_to_be_linked,url_format, str(mark_for_question))
                        found = True
                        break
        worksheet.write(total_cell_alphabet + str(row_counter_master + 1),str(total), format_normalcell)
        for b in questions_mastersheet_with_column_no:
                if b[0] not in attempted_questions:
                        worksheet.write(row_counter_master, b[1], 'NA')
        row_counter_master = row_counter_master + 1
        
    workbook.close()
spreadsheet = [['D', '1119'], [['11', '1', '5', 89], ['9', '2.1', '1', 237], ['6', '2.2', '6', 458], ['4', '3', '3.5', 609]], [['10', '5', '1', 102], ['8', '7', '1', 257], ['6', '8.1', '2', 411], ['5', '8.2', '2', 489], ['4', '9', '0.5', 567], ['3', '10', '1', 645], ['UNMARKED_QUESTIONS', ['1', '11', 803]]], ['D', '8775'], [['9', '6', '0', 103], ['6', '1', '1.5', 351], ['4', '8.1', '025', 517], ['2', '8.2', '1.25', 682]], [['10', '1', '2.5', 108], ['9', '2.1', '3.5', 192], ['8', '2.2', '1.5', 266], ['6', '3', '0', 435], ['5', '4', '0', 510], ['4', '5', '1', 588], ['2', '9', '2', 736], ['1', '10', '2', 802]]]
#record = [['1', '1', '7'], ['2', '5', '3.4'], ['3', '6.2', '9.1'], ['4', '6.1.3', '2.2.1'], ['5', '6', '7'], ['6', '1', '93'], ['7', '72', '5.6'], ['8', '3.4', '2.9'], ['9', '2.1', '13'], ['10', '9', '96'], ['11', '14', '12'], ['12', '5.6', '3.1'], ['13', '7.2', '4.6'], ['14', '2.3', '1.5']]
path_to_save = '/home/apoorv/Desktop/Record.xlsx'
text = '1\n2-2\n3\n4\n5\n6\n7\n8-2\n9\n10\n11'
#create_checking_sheet(spreadsheet)
#create_master_sheet(text, path_to_save)
