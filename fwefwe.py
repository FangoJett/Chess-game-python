from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QMainWindow, QGraphicsItem
from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtCore import Qt, QRectF

class CustomRectItem(QGraphicsRectItem):
    def __init__(self, x, y, width, height, scene):
        super().__init__(x, y, width, height)
        self.scene = scene  # Przechowuje referencję do sceny, aby móc sprawdzić jej rozmiary

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            # Logika ograniczająca, aby element nie wychodził poza scenę
            new_pos = value.toPointF()
            rect = self.scene.sceneRect()
            item_rect = self.rect()
            # Sprawdź, czy nowa pozycja nie wychodzi poza granice sceny i dostosuj, jeśli trzeba
            if not rect.contains(new_pos):
                if new_pos.x() < rect.left():
                    new_pos.setX(rect.left())
                elif new_pos.x() + item_rect.width() > rect.right():
                    new_pos.setX(rect.right() - item_rect.width())
                if new_pos.y() < rect.top():
                    new_pos.setY(rect.top())
                elif new_pos.y() + item_rect.height() > rect.bottom():
                    new_pos.setY(rect.bottom() - item_rect.height())
                return new_pos
        return super().itemChange(change, value)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 1000, 600)
        self.setWindowTitle("Szachy")

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 600, 600)  # Ustawienie rozmiaru sceny

        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(0, 0, 600, 600)

        self.show()
        self.addContent()

    def addContent(self):
        green_brush = QBrush(Qt.green)
        black_pen = QPen(Qt.black)
        black_pen.setWidth(1)

        # Tworzenie i dodawanie niestandardowego prostokąta do sceny
        rect_item = CustomRectItem(0, 0, 100, 100, self.scene)
        rect_item.setBrush(green_brush)
        rect_item.setPen(black_pen)
        rect_item.setFlag(QGraphicsItem.ItemIsMovable)
        self.scene.addItem(rect_item)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec_()
