#Others
import os
import sys

#Pyside imports
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

#My imports
from styles import setupTheme
from display import Display
from info import info
from paths import WINDOW_ICON_PATH
from main_window import MainWindow
from buttons import ButtonGrid
from save import SaveHistory

####################################
#######START#OF#THE#CODE############
####################################

if __name__ == "__main__":

    #History Instance
    saveData = SaveHistory()

    #If there is a save file, load it
    if os.path.exists(saveData._filename):
        saveData.loadData()
    else:
        print('no data to read')

    #Creating the app
    app = QApplication(sys.argv)
    setupTheme()
    window = MainWindow()

    #Adding an icon to the app
    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    #last calculus
    infowedget = info('...')
    window.addWidgetToVLayout(infowedget)

    #Setting up the display
    display = Display()
    display.setPlaceholderText("Press H to open history") #Setting a place holder text into the textbox
    window.addWidgetToVLayout(display) #Adding the text box to the layout

    #grid
    buttonsGrid = ButtonGrid(window,display,saveData,infowedget)
    window.vLayout.addLayout(buttonsGrid)

    #Setting up the buttons
    buttonsGrid._makeGrid()#Adding the buttons to the layout


    #Remove the permission to resize the window
    window.AdjustFixedSize()
    window.show()
    app.exec()