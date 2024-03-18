import sys
from PyQt5.QtWidgets import QApplication, QGraphicsSceneMouseEvent, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QMainWindow, QBoxLayout, QGraphicsItem, QGraphicsRectItem
from PyQt5.QtGui import QPixmap, QImage, QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QRectF, QPointF, QPoint


WHITE_PAWN = 'images/pawn.png'
BLACK_PAWN = 'images/pawn1.png'

WHITE_BISHOP = 'images/bishop.png'
BLACK_BISHOP = 'images/bishop1.png'

WHITE_KNIGHT = 'images/knight.png'
BLACK_KNIGHT = 'images/knight1.png'

WHITE_ROOK = 'images/rook.png'
BLACK_ROOK = 'images/rook1.png'

WHITE_QUEEN = 'images/queen.png'
BLACK_QUEEN = 'images/queen1.png'

WHITE_KING = 'images/king.png'
BLACK_KING = 'images/king1.png'

MAX_XY = 525
MIN_XY = 0 

#Main class
class ChessPiece(QGraphicsRectItem):
    def __init__(self, x, y, color, image_path):
        super().__init__(0, 0, 75, 75)
        self.setPos(QPointF(x, y))
        
        #Loading image 
        self.setPen(QColor(Qt.transparent))
        pixmap = QPixmap(image_path[color])
        pixmap = pixmap.scaled(self.rect().size().toSize(), aspectRatioMode=Qt.IgnoreAspectRatio, transformMode=Qt.SmoothTransformation)
        brush = QBrush(pixmap)
        self.setBrush(brush)
        
        
        #Setting flags
        self.setFlag(self.ItemIsMovable)                     
        self.setFlag(self.ItemSendsScenePositionChanges)     

        
        #Collision settings
        self.max_xy = MAX_XY    
        self.min_xy = MIN_XY
        
        #Mouse event settings
        self.original_scale = 1.0
        
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            if value.x() > self.max_xy:
                value.setX(self.max_xy)
            if value.x() < self.min_xy:
                value.setX(self.min_xy)
            if value.y() > self.max_xy:
                value.setY(self.max_xy)
            if value.y() < self.min_xy:
                value.setY(self.min_xy)
            return value
        return super().itemChange(change, value)

    def mouseReleaseEvent(self, event):
        new_x = round(self.x() / 75) * 75
        new_y = round(self.y() / 75) * 75
        self.setPos(new_x, new_y)
        self.setScale(self.original_scale)
        super().mouseReleaseEvent(event)
        
    def mousePressEvent(self, event):
        self.original_scale = self.scale()  # Zapisanie pierwotnej skali
        self.setScale(self.original_scale * 1.1)
        return super().mousePressEvent(event)


class Pawn(ChessPiece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, {"black": BLACK_PAWN, "white": WHITE_PAWN})
        
        
        #Colision adjustment
    #    self.max_xy += 15
    #    self.min_xy -= 15
        
        
        
class Bishop(ChessPiece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, {"black": BLACK_BISHOP, "white": WHITE_BISHOP})


class Knight(ChessPiece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, {"black": BLACK_KNIGHT, "white": WHITE_KNIGHT})


class Rook(ChessPiece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, {"black": BLACK_ROOK, "white": WHITE_ROOK})


class Queen(ChessPiece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, {"black": BLACK_QUEEN, "white": WHITE_QUEEN})


class King(ChessPiece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, {"black": BLACK_KING, "white": WHITE_KING})