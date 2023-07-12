from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt

from paths import SMALL_FONT_SIZE

class info(QLabel):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.configInfoStyle()

    def configInfoStyle(self):
        self.setStyleSheet(f'font-size:{SMALL_FONT_SIZE}px;')
        self.setAlignment(Qt.AlignmentFlag.AlignRight)