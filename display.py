from PySide6.QtWidgets import QLineEdit
from paths import BIG_FONT_SIZE,TEXT_MARGIN,MINIMUM_WIDTH
from utils import isEmpty,IsNumOrDot
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeyEvent

class Display(QLineEdit):
    equationTrigger = Signal(str)
    backspaceTrigger = Signal(str)
    clearTrigger = Signal(str)
    numAndDotTrigger = Signal(str)
    operatorTrigger = Signal(str)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        
        self.configStyle()
        self.setReadOnly(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def configStyle(self):
        #Display style
        self.setStyleSheet(f'font-size: {BIG_FONT_SIZE}px;') #setting font-size
        self.setMinimumHeight(BIG_FONT_SIZE*2) #Textbox minimum height
        self.setMinimumWidth(MINIMUM_WIDTH)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(TEXT_MARGIN,TEXT_MARGIN,TEXT_MARGIN,TEXT_MARGIN) #setting the margin inside the text box

    #Setting up the keyboard
    def keyPressEvent(self, event: QKeyEvent) -> None:
        text = event.text().strip()
        key = event.key()
        KEYS = Qt.Key

        #Setting up the key that will trigger somethihng
        isEnter = key in [KEYS.Key_Enter, KEYS.Key_Equal]
        isBackspace = key in [KEYS.Key_Backspace, KEYS.Key_Delete]
        isClear = key in [KEYS.Key_C,KEYS.Key_Escape]
        isOperator = key in [KEYS.Key_Plus, KEYS.Key_Minus, KEYS.Key_Slash, KEYS.Key_Asterisk, KEYS.Key_P]

        #Setting up their signal when pressed
        if isEnter:
            self.equationTrigger.emit('=')
            return event.ignore()

        if isBackspace:
            self.backspaceTrigger.emit(str('←'))
            return event.ignore()

        if isClear:
            self.clearTrigger.emit('C')
            return event.ignore()
        
        if isOperator:
            if text.lower() == 'p':
                text = '^'
            self.operatorTrigger.emit(str(text))
            return event.ignore()
        
        # if the button don't have text don't past by
        if isEmpty(text):
            return event.ignore()
        
        if IsNumOrDot(text):
            self.numAndDotTrigger.emit(text)
            return event.ignore()