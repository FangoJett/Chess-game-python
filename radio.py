import sys
from PyQt5.QtWidgets import QApplication, QWidget, QRadioButton, QVBoxLayout

class RadioWidget(QWidget):
    def __init__(self,parent):
        self.parent = parent
        super().__init__()

        self.initUI()

    def initUI(self):
        
        self.radioButton1 = QRadioButton('Local game')
        self.radioButton1.setChecked(True)
        self.radioButton1.option = 0
        self.radioButton2 = QRadioButton('Local vs AI')
        self.radioButton2.option = 1
        self.radioButton3 = QRadioButton('Join Onlie Game')
        self.radioButton3.option = 2
        self.radioButton4 = QRadioButton('Host Onlie Game')
        self.radioButton4.option = 3
        
        layout = QVBoxLayout()
        layout.addWidget(self.radioButton1)
        layout.addWidget(self.radioButton2)
        layout.addWidget(self.radioButton3)
        layout.addWidget(self.radioButton4)
        
        self.setLayout(layout)

        
        self.radioButton1.toggled.connect(self.onClicked)
        self.radioButton2.toggled.connect(self.onClicked)
        self.radioButton3.toggled.connect(self.onClicked)
        self.radioButton4.toggled.connect(self.onClicked)
        
        self.show()

    def onClicked(self):
        radioButton = self.sender()

        if radioButton.isChecked():
            self.parent.player_option = radioButton.option
            


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RadioWidget()
    sys.exit(app.exec_())
