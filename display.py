from PySide6.QtWidgets import QLineEdit
from paths import BIG_FONT_SIZE,TEXT_MARGIN,MINIMUM_WIDTH
from PySide6.QtCore import Qt

class Display(QLineEdit):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        
        self.configStyle()

    def configStyle(self):
        #Display style
        self.setStyleSheet(f'font-size: {BIG_FONT_SIZE}px;') #setting font-size
        self.setMinimumHeight(BIG_FONT_SIZE*2) #Textbox minimum height
        self.setMinimumWidth(MINIMUM_WIDTH)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(TEXT_MARGIN,TEXT_MARGIN,TEXT_MARGIN,TEXT_MARGIN) #setting the margin inside the text box