**Using machine learning and image processing to effectively analyze scanned answer scripts after an examination**

**Apoorv Sadana**



**ABSTRACT**

The growth of artificial intelligence over the years has managed to solve some of the most difficult problems in the field of technology. The applications of machine learning are vast. This paper attempts to propose a way to use artificial intelligence to increase the efficiency of paper analysis. The aim of the paper is to use machine learning and image processing for the effective digital transformation of answer papers after a test. In a large portion of schools in India, after every test correction there are  certain procedures that need to be followed. These procedures make the task cumbersome, time consuming and prone to errors. In order to tackle the problem, a program was developed to work on the scanned copies of answer scripts for generating an excel file consisting of the analyzed data.

First, the answer script was redesign to increase the efficiency of the OpenCV algorithms. Secondly, the various functions of the OpenCV library were used to collect data from papers. Finally, the collected data was then passed through the MNIST dataset for recognition of handwritten digits and generation of excel file.

The program is able to identify the location of all the handwritten data within the answer script (100%) and is able to predict the handwritten digits upto an accuracy of 92%. In order to eliminate errors, an easy checking algorithm is also made. The application of artificial intelligence in paper analysis has many advantages ranging from reduced effort to time saving.

**Keywords: analysis of scanned answer scripts, artificial intelligence, digit prediction using MNIST dataset, image processing (OpenCV), using excel via python**

**1. Problem**

In many schools in India,after evaluating all the answers scripts, the teacher has to perform the following tasks

1. Totaling the paper
2. Writing down the marks secured by the student in each question on the first sheet of the answer script
3. Creating an excel file from the first sheet of all answer scripts
4. Storing the papers for security purposes

These procedures make the task cumbersome, time consuming and prone to errors.

**2. Algorithm and Solution**

**2.1 Redesigning the answer script**

In order to tackle the problem the answer script was first redesigned. Fig 1 is a sample of the old answer script and Fig 2 is a sample of the redesigned answer script.

In the old answer script, the question numbers were written in the left margin and the marks were written along with the answers. This made the data unorganized and difficult for the computer to extract all information within a sheet.

In order to collect all the relevant data in one place, a new column was added to the redesigned answer script. It was made dark black so that it could be easily thresholded. The right column was used by the students to write down the question number and the left column was used by the teachers to write down the marks secured by the student in each question. The marks for each question were written in the box just to the left of the box containing the question number

**Old answer script**

![alt text](https://github.com/ApoorvSadana/PaperAnalysisApp/blob/master/images/image21.png?raw=true)

_Fig 1. Questions numbers are written in the left margin and the marks are written along with the answers_

**Redesigned answer script**

![alt text](https://github.com/ApoorvSadana/PaperAnalysisApp/blob/master/images/image2.png?raw=true)

_Fig 2. Question numbers in left column of table and marks in tight column of table_

Also, the first page of the answer script was modified to include the admission number of the student enclosed withing the admission box.

**First page of answer script**

![alt text](https://github.com/ApoorvSadana/PaperAnalysisApp/blob/master/images/image7.png?raw=true)

_Fig 3. The first page of answer script consists of the admission number of the student_

**2.2 Collecting Data from answer scripts**

Two scanned copies were taken for each answer script – one colored and one in black and white (not grayscale).(Using image processing to produce the black and white copy did not give the desired results. Hence, a scanned copy was used)

The following algorithm was followed:

_Thresholding, contouring and dilating were performed on the black and white image for accurate results. Cropping was performed on the color image as fine details were lost in the black and white scan._

1. Inverted thresholding to switch black and white colors within the image (this made the table and admission box white in color and thus, it could be contoured)
2. Dilating of the thresholded image with kernel size 10. This filled up the black holes within the image, if any
3. Contouring image with tree retrieval mode to detect all contours within image.
4. Checking if the image is of the first page of answer script (containing the admission number) or of a page containing the answers by checking the number of contours in the image (it was found that the first page of the answer scripts had less than 30 contours whereas other pages had more than 30)
5. Contouring image with external retrieval mode to detect only the outer most contours.
6. Cropping the table or the admission box from the image. This is done by finding the external contour of maximum area. In case of the admission box, the rightmost x coordinate of the admission box must be greater than one third of the width of the image. In case of the table, the x coordinate is less than one third of the width.
7. Cropping digit boxes within the image cropped in step  6. The digit box is the box in which the marks, question number or a digit of the admission number is written. The digit boxes are cropped by contouring again.
8. Saving images of the digit boxes. In case of the admission box, the digit boxes are saved in the left to right manner. In case of the table, digit boxes with approximately same y coordinate value are stored with similar filenames. The left one is saved as marks and the right one as question number.

**2.3 Modifying images of the digit boxes**

Three types of digit boxes are possible in an answer script

1. Those containing only a single digit
2. Those containing more than one digit (may or may not be separated by a decimal point). Example:. question number 12 or marks 3.25
3. Those which are empty

In order to distinguish between the above three types of digit boxes and process them accordingly, the following algorithm is followed:

1. Finding the contour of maximum area within the digit box.
2. If the height of the found contour is less than a specific value (will depend upon the resolution of scanned images), then the digit box is empty and not used in any further processing. Else, the contour consists of one digit at least.

_The steps below are executed only if the digit box consists of one digit box at least._

1. Finding contours of height similar to the largest contour. These contours will also be digits and if found, the digit box would contain more than one digit.
2. Checking for the presence of a small contour between any two consecutive digit contours. If present, it would be a decimal point.
3. Cropping all the digits from the digit box and saving them with appropriate filenames to express the position of digits and decimal point in the actual number.

**2.4 Predicting digits with MNIST dataset**

All the digits which are cropped out are passed into a neural network trained on the MNIST dataset.

**2.5 Creating the check sheet**

There is a very high probability that at least one number in an answer script might be predicted incorrectly by the program. However, while analyzing papers, the accuracy must be 100%. In order to rectify these errors, a check sheet is created in excel. Fig 4. shows a part of this check sheet. It displays the numbers predicted by the neural network as well as an image of the actual number (which was cropped in step 8 of section 2.2). The teacher is expected to compare the actual and the computer generated numbers and in case of any errors, the teacher may rectify them there itself and save the file.

In order to speed up the process, the computer generated  and actual number have been placed side by side. This allows the teacher to quickly skim through the excel sheet and locate the errors.

![alt text](https://github.com/ApoorvSadana/PaperAnalysisApp/blob/master/images/image11.png?raw=true)

**Check sheet**

_Fig 4. Check sheet displaying the computer generated and actual numbers_

**2.6 Generating master sheet**

After the errors in the check sheet have been rectified, a master sheet is created using the data from the check sheet. This ensures that the master sheet is 100% accurate. The master sheet is made based on a layout that is provided by the teacher which includes the number of questions in the paper and number of subparts per question, if any. The master sheet displays

1. The marks secured by the student in each question
2. Total marks secured by the student
3. Questions left unattempted by the student
4. Questions that are not marked by the teacher (but have been attempted by the student)
5. Answer scripts. Clicking on the marks secured by a student in any question, say X, displays that sheet of the answer script on which the student has answered question X.

![alt text](https://github.com/ApoorvSadana/PaperAnalysisApp/blob/master/images/image9.png?raw=true)

**Master Sheet**

_Fig 5. Master sheet displaying answer script analysis. &#39;NA&#39; stands for not attempted_

**2.7 GUI**

In Appendix

**3. Results**

Section 2.2 and 2.3 produce results that are nearly 100% accurate. Prediction of digits using MNIST dataset has an accuracy of 92%(digits and not complete numbers). This may seem ambiguous because neural networks trained on the MNIST dataset have achieved accuracies greater than 99%. But these neural networks were tested on images that were originally 28x28 in dimensions (the MNIST format). However, while cropping out digits from the answer scripts, the dimensions of the digits will vary as the handwritings of different students will vary and no student can accurately make a digit which is exactly 28x28 in dimensions. Hence, the images of cropped digits first need to be converted into the required format and then predicted with the neural network. It is due this conversion that the accuracy is around 92%.

The program can also detect decimal numbers which means that it can detect question subparts and fractional marks.

**4. Future and Scope**

The advantages of an application capable of analyzing answer scripts include:

1. Saves time. All tasks mentioned in section 1 have been reduced to scanning of papers and rectifying of errors in the check sheet.
2. Reduces Errors. No more errors in totaling the paper.  The program also notifies the teacher if any question has been left unmarked.
3. Prevents paper tampering. As the excel sheet has a record of the answers, students cannot modify their answers and ask for marks.
4. Provides easy access. Previously, all papers had to be stored and during paper reopening, teachers had to look for specific papers among thousands of others. Using the program, they can access the paper from the excel sheet as it also contains the answer scripts.
5. Paper Recycling. Papers no longer needs to be stored as the excel file contains all information.

**5. References**

No paper was referenced to as the research actually attempts to apply machine learning and image processing algorithms to a real life problem.

**Appendix**

GUI Demonstration

**1. Input**

![alt text](https://github.com/ApoorvSadana/PaperAnalysisApp/blob/master/images/image7.png?raw=true)

1

![alt text](https://github.com/ApoorvSadana/PaperAnalysisApp/blob/master/images/image2.png?raw=true)

2                                                                              

![alt text](https://github.com/ApoorvSadana/PaperAnalysisApp/blob/master/images/image8.png?raw=true)

3

![alt text](https://github.com/ApoorvSadana/PaperAnalysisApp/blob/master/images/image3.png?raw=true)

4

_Fig 6._

Similarly, a black and white copy of all the above images was also scanned. The images must be scanned in the order as shown above – one paper followed by another.

**2. Starting the GUI – Entering location of scanned pictures**



![alt text](https://github.com/ApoorvSadana/PaperAnalysisApp/blob/master/images/image10.png?raw=true)

![alt text](https://github.com/ApoorvSadana/PaperAnalysisApp/blob/master/images/image13.png?raw=true)

_Fig 7._

**3. Entering question paper layout**

![alt text](https://github.com/ApoorvSadana/PaperAnalysisApp/blob/master/images/image23.png?raw=true)

_Fig 8._


**4. Start Processing**

![alt text](https://github.com/ApoorvSadana/PaperAnalysisApp/blob/master/images/image20.png?raw=true)

_Fig 9._

**5. After Processing**

![alt text](https://github.com/ApoorvSadana/PaperAnalysisApp/blob/master/images/image6.png?raw=true)

![alt text](https://github.com/ApoorvSadana/PaperAnalysisApp/blob/master/images/image11.png?raw=true)

_Fig 10._

**6. Saving master sheet**

![alt text](https://github.com/ApoorvSadana/PaperAnalysisApp/blob/master/images/image13.png?raw=true)

_Fig 11._

**7. Master Sheet**

![alt text](https://github.com/ApoorvSadana/PaperAnalysisApp/blob/master/images/image18.png?raw=true)

_Fig 12._

                                                             
 Clicking on D4 gives  

![alt text](https://github.com/ApoorvSadana/PaperAnalysisApp/blob/master/images/image3.png?raw=true)

Clicking on H6 gives

![alt text](https://github.com/ApoorvSadana/PaperAnalysisApp/blob/master/images/image2.png?raw=true)

_                     Fig 13.                                                        Fig 14._
