import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QMainWindow, QBoxLayout, QGraphicsItem, QGraphicsRectItem
from PyQt5.QtGui import QPixmap, QImage, QBrush, QPen
from PyQt5.QtCore import Qt
from figures import Pawn, Bishop, Rook, Queen, King, Knight

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setWindowTitle("Szachy")
        self.setGeometry(100, 100, 1000, 600)
        self.create_ui()
        
        

    def create_ui(self):
        self.scene = QGraphicsScene(self)
        self.size_x = 600
        self.size_y = 600
        self.scene.setSceneRect(0,0,self.size_x,self.size_y)
        
        self.view = QGraphicsView(self.scene,self)
        self.view.setGeometry(0,0,self.size_x,self.size_y)
        image = QImage('images/chessboard.png')
        self.scene.setBackgroundBrush(QBrush(image))
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        
        self.show()
        self.addContent()
        
    def addContent(self):

        for i in range(8):
            self.scene.addItem(Pawn(0+75*i,75,"black"))
        for i in range(8):
            self.scene.addItem(Pawn(0+75*i,450,"white"))       

        self.scene.addItem(Rook(0,525,"white"))
        self.scene.addItem(Rook(525,525,"white"))
        
        self.scene.addItem(Rook(0,0,"black"))
        self.scene.addItem(Rook(525,0,"black"))
        
        self.scene.addItem(Knight(75,525,"white"))
        self.scene.addItem(Knight(450,525,"white"))
        
        self.scene.addItem(Knight(75,0,"black"))
        self.scene.addItem(Knight(450,0,"black"))
        
        self.scene.addItem(Bishop(150,0,"black"))
        self.scene.addItem(Bishop(375,0,"black"))

        self.scene.addItem(Bishop(150,525,"white"))
        self.scene.addItem(Bishop(375,525,"white"))
        
        self.scene.addItem(Queen(225,0,"black"))

        self.scene.addItem(Queen(225,525,"white"))
        
        self.scene.addItem(King(300,0,"black"))
        
        self.scene.addItem(King(300,525,"white"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    
    chessboard = MainWindow()


    sys.exit(app.exec_())