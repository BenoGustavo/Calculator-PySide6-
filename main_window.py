from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTextEdit, QPushButton, QScrollArea, QDialog

from paths import SMALL_FONT_SIZE,MINIMUM_WIDTH,TEXT_MARGIN

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

class CustomMessageBox(QDialog):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Equation History")
        self.setWindowModality(Qt.ApplicationModal)

        # Create a QVBoxLayout to arrange the contents of the dialog
        layout = QVBoxLayout(self)

        # Create a QTextEdit widget to display the text
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(text)
        self.text_edit.setReadOnly(True)
        self.setStyleSheet(f'font-size: {SMALL_FONT_SIZE}px;') #setting font-size
        self.setMinimumHeight(SMALL_FONT_SIZE*2) #Textbox minimum height
        self.setMinimumWidth(MINIMUM_WIDTH)
        self.setContentsMargins(TEXT_MARGIN,TEXT_MARGIN,TEXT_MARGIN,TEXT_MARGIN)

        # Create a QScrollArea to add scroll functionality to the text
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setWidget(self.text_edit)

        # Add the QScrollArea to the layout
        layout.addWidget(scroll_area)

        # Add OK button
        exitButton = QPushButton("Exit", self)
        exitButton.clicked.connect(self.accept)
        layout.addWidget(exitButton)