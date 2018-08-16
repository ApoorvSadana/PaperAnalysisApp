########Clear all previously stored variables before every run###########
import sys
sys.modules[__name__].__dict__.clear()
#########################################################################

from appJar import gui
import Master
import Excel_Program as excel
import time
import os


app = gui("Master","800x600")

def press(btn):
    global text
    global path_to_save
    if btn == "SCAN":
        pass
    elif btn == "Done":
        app.hideSubWindow("After Processing")
        app.openPage("Paper Analysis", 4)
    elif btn == "START":
        app.showSubWindow("During Processing")
        path_to_linear = app.getEntry("path_to_black_white")
        path_to_color = app.getEntry("path_to_color")
        spreadsheet = Master.main(path_to_linear + '/', path_to_color + '/')
        excel.create_checking_sheet(spreadsheet)
        app.hideSubWindow("During Processing")
        app.showSubWindow("After Processing")
    elif btn == "Open File":
        os.system("see CheckSheet.xlsx")
    elif btn == "SAVE":
        path_to_save = app.saveBox(title="Save the Record File", fileName="Record", dirName=None, fileExt=".xlsx", fileTypes=None, asFile=None, parent=None)
        text = app.getTextArea("Details")
        excel.create_master_sheet(text, path_to_save)
        
app.startPagedWindow("Paper Analysis")
#app.setGeometry("800x600")
app.startPage()
app.addLabel("black_white", "Enter path to black and white images")
app.addDirectoryEntry("path_to_black_white")
app.addLabel("color", "Enter path to colored images")
app.addDirectoryEntry("path_to_color")
app.stopPage()

app.startPage()
#app.setGeometry("800x600")
app.addLabel("details_label", " Enter the layout of the of paper. \n Example : \n If there are 5 questions and the 2nd question has three subparts then you will enter \n 1\n 2-3\n 3\n 4\n 5")
app.addTextArea("Details")
app.stopPage()

app.startPage()
app.addLabel("process_initiation", "Click on START button to start processing")
app.addButton("START", press)
app.stopPage()

app.startPage()
app.addLabel("Save_Label", "Click on SAVE button to save the excel file in desired location.\nDon't forget to enter the finelane when the dialog box opens after clicking the button.")
app.addButton("SAVE", press)
app.stopPage()

app.startSubWindow("During Processing", modal = True)
app.setGeometry("500x100")
app.addLabel("message", "Processing...")
app.stopSubWindow()

app.startSubWindow("After Processing", modal = True)
app.addLabel("status", "Done! Click 'Open File' and an excel file will open.\nYou will have to check if the computer generated marks and questions\ntally with the actual marks and questions. If not, make the changes there itself and save the file.\n Once Done click on the 'Done' Button")
app.startLabelFrame("Example", 10, 0)
app.addImage("example", "Example.png")
app.stopLabelFrame()
app.addButton("Open File", press)
app.addButton("Done", press)
app.stopSubWindow()
                          
app.go()

