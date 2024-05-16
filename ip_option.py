from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QLabel

class InputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Wprowadź dane")

        layout = QFormLayout()
        self.label1 = QLabel("IP address:")
        self.entry1 = QLineEdit()
        layout.addRow(self.label1, self.entry1)

        self.label2 = QLabel("Port:")
        self.entry2 = QLineEdit()
        layout.addRow(self.label2, self.entry2)

        self.okButton = QPushButton("OK")
        self.okButton.clicked.connect(self.accept)
        layout.addWidget(self.okButton)

        self.setLayout(layout)

    def accept(self):
       
        value1 = self.entry1.text()
        value2 = self.entry2.text()

        super().accept()


class InputDialogShort(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Enter data")
        layout = QFormLayout()


        self.label2 = QLabel("Port:")
        self.entry2 = QLineEdit()
        layout.addRow(self.label2, self.entry2)

        self.okButton = QPushButton("OK")
        self.okButton.clicked.connect(self.accept)
        layout.addWidget(self.okButton)

        self.setLayout(layout)

    def accept(self):
       

        value2 = self.entry2.text()

        super().accept()





