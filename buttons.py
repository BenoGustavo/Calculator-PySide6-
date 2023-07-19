from PySide6.QtWidgets import QPushButton,QGridLayout
from PySide6.QtCore import Slot
from paths import MEDIUM_FONT_SIZE
from display import Display
from info import info

#IsNumOrDot and isEmpty don't worked properly =(
from utils import IsNumOrDot, isEmpty, isValidNumber, isOperator, removeOperators, deleteLastChar, addDotAfterZero

#Class to create a button
class Button(QPushButton):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.configStyle()

    #Adding CSS to the button
    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75,75)

class ButtonGrid(QGridLayout):
    def __init__(self,display: Display,infoSupDisplay: info,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self._gridMask = [
            ['C','⌫','^','/'],
            ['7','8','9','*'],
            ['4','5','6','-'],
            ['1','2','3','+'],
            ['0', '','.','='],
        ]

        self.display = display
        self.infoWidget = infoSupDisplay

        #Equation needs to be a ' ' (Space) because i need to check the last char in the string
        self._equation = ' '

        self._makeGrid
    
    #Creating the buttons
    def _makeGrid(self):

        for row,text in enumerate(self._gridMask):
            for column,button_text in enumerate(text):
                
                #Skip empty space
                if button_text == '':
                    continue
                
                #Get button text
                button = Button(button_text)

                #Setting up special buttons and operators (/*-+=^C...)
                if not button_text in '1234567890.':
                    button.setProperty('cssClass','specialButton')

                #Making 0 ocupy the empty space
                if button_text == '0':
                    self.addWidget(button,row,column,1,2)

                    buttonSlot = self._makeButtonDisplaySlot(self._insertContentIntoDisplay,button,)
                    button.clicked.connect(buttonSlot)
                    continue

                self.addWidget(button,row,column)

                buttonSlot = self._makeButtonDisplaySlot(self._insertContentIntoDisplay,button,)
                button.clicked.connect(buttonSlot)
    
    #Delaying the button function (WAITING TO SOMEONE TO PRESS)
    def _makeButtonDisplaySlot(self,method,*args,**kwargs):
        @Slot(bool)
        def realSlot():
            method(*args,**kwargs)
        return realSlot

    #Adding functions to the special buttons
    def _specialButtons(self,button_char):
        #Clear button
        if button_char == 'C':
            self.display.clear()
            self._equation = ' '
            self.infoWidget.setText(self._equation)

        #Backspace button
        if button_char == '⌫':
            if self.display.text() != '':
                self.display.backspace()
            else:
                self._equation = deleteLastChar(self._equation)
                self.infoWidget.setText(self._equation)

        #Equals button
        if button_char == '=':
            self._equation += self.display.text()
            self.display.clear()
            
            #Checking the string before eval
            try:
                if '^' in self._equation:
                    self._equation = self._equation.replace('^','**')
                #Removing operators to check before eval the string
                checkOperation = removeOperators(str(self._equation))
                float(checkOperation)

                #Check if the last char is an operator then remove it
                if isOperator(self._equation[-1]):
                    self._equation = deleteLastChar(self._equation)
                
                #Add a comma after the first zero
                if self._equation[1] == '0':
                    self._equation = addDotAfterZero(self._equation)

                #Eval the string
                self.display.setText(str(eval(self._equation)))

                #Reset the _equation
                self._equation = ' '
                self.infoWidget.setText(self._equation)

            except ValueError and ZeroDivisionError:
                self.display.setPlaceholderText("BAD EQUATION")

                #Clear the calculator
                self._specialButtons('C')
                return


    def _insertContentIntoDisplay(self,button):
        buttonText = button.text()
        newDisplayValue = self.display.text() + buttonText

        #Verify if the button text is a special button (NOT A NUMBER OR OPERATOR)
        self._specialButtons(button.text())

        try:
            #Changes the last operator if the display is empty.
            if isOperator(buttonText) and isOperator(self._equation[-1]) and self.display.text() == '':
                self._equation = self._equation[:-1] + buttonText
                self.infoWidget.setText(self._equation)
                return
        except IndexError:
            self._equation = ' '+self._equation

        #If the display is empty don't put an operator
        if isOperator(buttonText) and self.display.text() == '':
            return

        if not isValidNumber(newDisplayValue):
            if isOperator(buttonText):
                
                #Avoid double operator
                #If the last char of the equation is a operator and the first char of the display is one too, do NOTHING
                if isOperator(self._equation[-1]) and isOperator(newDisplayValue[0]):
                    return
                
                #Picking the display value and putting in the infoWidget
                self._equation += newDisplayValue
                self.infoWidget.setText(self._equation)
                self.display.setText('') #Clean the display
            return

        #Put the button text into display
        self.display.insert(buttonText)

