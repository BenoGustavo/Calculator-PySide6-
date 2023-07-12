from typing import Optional
import PySide6.QtCore
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel

class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        #Window Tittle
        self.setWindowTitle('Calculator')

        #Basic Layout
        self.central_widget = QWidget()
        self.vLayout = QVBoxLayout()
        self.central_widget.setLayout(self.vLayout)
        self.setCentralWidget(self.central_widget)

    def AdjustFixedSize(self):
        #NEEDS TO BE THE LAST THING SETTED 
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    def addWidgetToVLayout(self,widget: QWidget):
        self.vLayout.addWidget(widget)