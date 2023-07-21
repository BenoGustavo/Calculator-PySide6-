from PySide6.QtWidgets import QPushButton,QGridLayout
from PySide6.QtCore import Slot, Qt
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

        #Makes the button don't get focus when you click it
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

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
            ['←','C','±','(',')'],
            ['7','8','9','x','^'],
            ['4','5','6','÷','π'],
            ['1','2','3','-','%'],
            ['0', '','.','+','='],
        ]

        self.display = display
        self.infoWidget = infoSupDisplay

        #Equation needs to be a ' ' (Space) because i need to check the last char in the string
        self._equation = ' '

        self._makeGrid
    
    #Creating the buttons
    def _makeGrid(self):
        #Making the keyboard work
        self.display.backspaceTrigger.connect(self._specialButtons)
        #Clear the calculator
        self.display.clearTrigger.connect(self._specialButtons)
        #Trigger Equals
        self.display.equationTrigger.connect(self._specialButtons)
        #Nums and dots keyborad
        self.display.numAndDotTrigger.connect(self._insertContentIntoDisplay)
        #Use operator in keyboard
        self.display.operatorTrigger.connect(self._insertContentIntoDisplay)

        for row,text in enumerate(self._gridMask):
            for column,buttonText in enumerate(text):
                
                #Skip empty space
                if buttonText == '':
                    continue
                
                #Get button text
                button = Button(buttonText)
                
                if buttonText == '←':
                   button.setProperty('cssClass','backSpaceButton')

                #Setting up special buttons and operators (/*-+=^C...)
                if not buttonText in '1234567890.←':
                    button.setProperty('cssClass','specialButton')

                #Making 0 ocupy the empty space
                if buttonText == '0':
                    self.addWidget(button,row,column,1,2)

                    buttonSlot = self._makeButtonDisplaySlot(self._insertContentIntoDisplay,buttonText,)
                    button.clicked.connect(buttonSlot)
                    continue
                
                self.addWidget(button,row,column)

                buttonSlot = self._makeButtonDisplaySlot(self._insertContentIntoDisplay,buttonText,)
                button.clicked.connect(buttonSlot)
    
    #Delaying the button function (WAITING TO SOMEONE TO PRESS)
    def _makeButtonDisplaySlot(self,method,*args,**kwargs):
        @Slot(bool)
        def realSlot():
            method(*args,**kwargs)
        return realSlot

    #Adding functions to the special buttons
    @Slot()
    def _specialButtons(self,button_char):

        #Clear button
        if button_char == 'C':
            self.display.clear()
            self.display.setPlaceholderText('...')
            self._equation = ' '
            self.infoWidget.setText(self._equation)

        #add the value of pi to the display
        if button_char == 'π':
            self.display.insert('3.1415')
        
        if button_char == '(':
            self.display.insert('(')

        if button_char == ')':   
            self.display.insert(')')

        #Invert display number
        if button_char == '±' and button_char != '0':
            displayValue = self.display.text()

            #If there is two parenthesis in the display and you try to negative the value
            if '(' in self.display.text() and ')' in self.display.text():
                self._equation += self.display.text() + 'x'
                self.infoWidget.setText(self._equation)
                self.display.setText('(-') #Clean the display
                return

            #try multiply the display value by -1
            try:
                displayValue = float(self.display.text()) * -1
                
                if displayValue.is_integer():
                    displayValue = int(displayValue)

            except ValueError:
                self.display.setPlaceholderText("...")

            self.display.setText(str(displayValue))

        #Backspace button
        if button_char == '←':
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
                #Check if the last char is an operator then remove it
                if isOperator(self._equation[-1]):
                    self._equation = deleteLastChar(self._equation)

                #Changing visual operators to actual python operators
                if '÷' in self._equation:
                    self._equation = self._equation.replace('÷','/')
                if 'x' in self._equation:
                    self._equation = self._equation.replace('x','*')
                if '%' in self._equation:
                    self._equation = self._equation.replace('%','/100')
                if '^' in self._equation:
                    self._equation = self._equation.replace('^','**')

                #Removing operators to check before eval the string
                checkOperation = removeOperators(str(self._equation))
                float(checkOperation)
                
                #Add a comma after the first
                if self._equation[1] == '0':
                    self._equation = addDotAfterZero(self._equation)

                #Checking open parentesis
                checkOpenParentesis = self._equation.rfind('(')
                checkCloseParentesis = self._equation.rfind(')')
                
                #Closing parentesis if not open
                if checkOpenParentesis > checkCloseParentesis:
                    self._equation = self._equation + ')'

                #Eval the string
                result = float(eval(self._equation))
                
                #Check if the result can be an intenger
                if result.is_integer():
                    result = int(result)

                self.display.setText(str(result))

                #Reset the _equation
                self._equation = ' '
                self.infoWidget.setText(self._equation)

            except ValueError and ZeroDivisionError:
                self.display.setPlaceholderText("Division by zero")

                #Clear the calculator
                self._specialButtons('C')
                return

    @Slot()
    def _insertContentIntoDisplay(self,text):
        
        newDisplayValue = self.display.text() + text

        #Verify if the button text is a special button (NOT A NUMBER OR OPERATOR)
        self._specialButtons(text)

        try:
            #Changes the last operator if the display is empty.
            if isOperator(text) and isOperator(self._equation[-1]) and self.display.text() == '' and self._equation[-2] != '%':
                self._equation = self._equation[:-1] + text
                self.infoWidget.setText(self._equation)
                return
            
        except IndexError:
            self._equation = ' '+self._equation

        #If the display is empty don't put an operator
        if isOperator(text) and self.display.text() == '':
            return

        #Setting up the operator after clicked
        if not isValidNumber(newDisplayValue):
            if isOperator(text):
                
                #Avoid double operator
                #If the last char of the equation is a operator and the first char of the display is one too, do NOTHING
                if isOperator(self._equation[-1]) and isOperator(newDisplayValue[0]):
                    return
                
                if text == '%':
                    self._equation += newDisplayValue + 'x'
                    self.infoWidget.setText(self._equation)
                    self.display.setText('') #Clean the display
                    return

                #Picking the display value and putting in the infoWidget
                self._equation += newDisplayValue
                self.infoWidget.setText(self._equation)
                self.display.setText('') #Clean the display
            return

        #prevents that the '(' and ')' will be duplicated on display
        if text == '(' or text == ')':
            return
        
        #Put the button text into display
        self.display.insert(text)
