import sys
from PyQt5.QtWidgets import QWidget , QApplication, QGraphicsSceneMouseEvent, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QMainWindow, QBoxLayout, QGraphicsItem, QGraphicsRectItem
from PyQt5.QtGui import QPixmap, QImage, QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QRectF, QPointF, QPoint, pyqtSignal, QObject
import numpy as np

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

MAX_XY = 540
MIN_XY = -15 


d_f = {
    1:'p',
    2:'r',
    3:'n',
    4:'b',
    5:'q',
    6:'k'
}

d_s = {
    0:'a',
    1:'b',
    2:'c',
    3:'d',
    4:'e',
    5:'f',
    6:'g',
    7:'h',
}

d_n = {
    0:'8',
    1:'7',
    2:'6',
    3:'5',
    4:'4',
    5:'3',
    6:'2',
    7:'1',
}

#Main class
class ChessPiece(QGraphicsRectItem):
    my_signal = pyqtSignal(str)
    def __init__(self, x, y, color, image_path, scene,emitter): 
        super().__init__(0, 0, 75, 75)
        
        self.move_signal = emitter
        
        self.type = 0
        self.color = color
        self.setPos(QPointF(x, y))
        self.parent = scene
        
        

        
        #Loading image 
        self.setPen(QColor(Qt.transparent))
        pixmap = QPixmap(image_path[color])
        pixmap = pixmap.scaled(self.rect().size().toSize(), aspectRatioMode=Qt.IgnoreAspectRatio, transformMode=Qt.SmoothTransformation)
        brush = QBrush(pixmap)
        self.setBrush(brush)
        
        self.posx = self.x()
        self.posy = self.y()
        
        #Setting flags
        #self.setFlag(self.ItemIsMovable)                     
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
        self.setScale(self.original_scale)
        new_x = round(self.x() / 75) * 75
        new_y = round(self.y() / 75) * 75
        
        nx = int(new_x/75)      #new position x (possible)
        ny = int(new_y/75)      #new position y (possible)
        ox = int(self.posx/75)  # old position x
        oy = int(self.posy/75)  # old position y
        
        if not (self.is_move_legal(nx,ny,ox,oy,self.parent.board) and self.parent.whos_turn==self.color and np.abs(self.parent.board[ny,nx])!=6 ):
            self.setPos(self.posx, self.posy)
            
            
        else:
            if self.parent.board[ny,nx]!=0:
                self.parent.remove_piece(nx*75,ny*75)
            
            
            
            self.setPos(new_x, new_y)
            self.parent.board[ny,nx]=self.type

            self.parent.board[oy,ox]=0
            self.posx = self.x()
            self.posy = self.y()
            self.parent.upp_time(self.color)
            self.parent.check_check(self.parent.board)
            msg = self.move_to_string(ox,oy,nx,ny)
            self.send_move_online(msg)
            self.move_signal.sgnl.emit(f"Move:{self.color} {self.__class__.__name__} from position {ox}, {oy} to position {nx}, {ny}.")
            self.parent.change_turns()
            #print("------------------------------------")
        super().mouseReleaseEvent(event)
        
    def mousePressEvent(self, event):
        if self.parent.game_started and self.color == self.parent.whos_turn:
            self.original_scale = self.scale()  
            self.setScale(self.original_scale * 1.1)
        return super().mousePressEvent(event)
    
    def send_move_online(self,message):
        if self.parent.player_option>=2:
            self.parent.send(message)
    
            
    def are_you_being_checked(self):
        color_num = {"black": -1, "white": 1}[self.color]
        if self.parent.check==color_num*-1:
            return True
        return False
    
    def change_board_state(self,ox,oy,nx,ny,board_var):
        board_var[ny,nx]=board_var[oy,ox]
        board_var[oy,ox]=0
        return board_var
    
    def move_to_string(self,ox,oy,nx,ny):
        
        type_f = d_f[np.abs(self.type)]
        s_ox = d_s[ox]
        s_oy = d_n[oy]
        s_nx = d_s[nx]
        s_ny = d_n[ny]
        word = type_f + s_ox + s_oy + s_nx + s_ny
        self.parent.add_move(word)
        return word
        

class Pawn(ChessPiece):
    def __init__(self, x, y, color, scene, emitter):
        super().__init__(x, y, color, {"black": BLACK_PAWN, "white": WHITE_PAWN}, scene, emitter)
        self.type = {"black": -1, "white": 1}[color]
        self.double_move = True
    def is_move_legal(self,nx,ny,ox,oy, board):
        
        
        color_num = {"black": -1, "white": 1}[self.color]
        diff = np.abs(ny-oy)
        
    
        
        if board[ny,nx]*color_num>0:
            return False
        if diff>2:
                return False
        #move without beating
        if board[ny,nx]==0:
            if (ny-oy)*color_num>0:
                return False  
            if nx!=ox:
                return False
            if self.color=="black":
                if diff==2:
                    if oy==1:
                        if board[ny-1,nx]!=0:
                            return False
                    else:
                        return False
            if self.color=="white":
                if diff==2:
                    if oy==6:
                        if board[ny+1,nx]!=0:
                            return False
                    else:
                        return False
                    
        else:
            
            if diff!=1:
                return False
            if np.abs(nx-ox)!=1:
                return False
            if (ny-oy)*color_num!=-1:
                return False   
        
        return True       
    
        
        
class Bishop(ChessPiece):
    def __init__(self, x, y, color, scene, emitter):
        super().__init__(x, y, color, {"black": BLACK_BISHOP, "white": WHITE_BISHOP}, scene, emitter)
        self.type = {"black": -4, "white": 4}[color]
    def is_move_legal(self,nx,ny,ox,oy, board):
        
        x_diff = np.abs(nx-ox)
        y_diff = np.abs(ny-oy)
        
        color_num = {"black": -1, "white": 1}[self.color]
        
        if board[ny,nx]*color_num>0:
            return False
        
        if y_diff!=x_diff:
            return False
        
        if nx>ox:
            if ny>oy:
                for i in range(1,x_diff):
                    if board[ny-i,nx-i]!=0:
                        return False
            else:
                for i in range(1,x_diff):
                    if board[ny+i,nx-i]!=0:
                        return False
        if nx<ox:
            if ny>oy:
                for i in range(1,x_diff):
                    if board[ny-i,nx+i]!=0:
                        return False
            else:
                for i in range(1,x_diff):
                    if board[ny+i,nx+i]!=0:
                        return False
        return True
    
class Knight(ChessPiece):
    def __init__(self, x, y, color, scene, emitter):
        super().__init__(x, y, color, {"black": BLACK_KNIGHT, "white": WHITE_KNIGHT}, scene, emitter)
        self.type = {"black": -3, "white": 3}[color]
    def is_move_legal(self,nx,ny,ox,oy,board):

        x_diff = np.abs(nx-ox)
        y_diff = np.abs(ny-oy)
        color_num = {"black": -1, "white": 1}[self.color]
        
        if board[ny,nx]*color_num>0:
            return False

        if x_diff==2 and y_diff==1:
            return True
        if x_diff==1 and y_diff==2:
            return True 
        
        return False
    
class Rook(ChessPiece):
    def __init__(self, x, y, color, scene, emitter):
        super().__init__(x, y, color, {"black": BLACK_ROOK, "white": WHITE_ROOK}, scene, emitter)
        self.type = {"black": -2, "white": 2}[color]
        self.first_move = True
    def is_move_legal(self,nx,ny,ox,oy,board):
        
        itr = 0
        
        
        color_num = {"black": -1, "white": 1}[self.color]
        
        if board[ny,nx]*color_num>0:
            return False
        
            
        if nx!=ox and ny!=oy:
            return False
        
        if nx!=ox:
            itr = np.abs(nx-ox)
            if nx>ox:
                for i in range(1,itr):
                    if board[ny,nx-i]!=0:
                        return False
            if nx<ox:
                for i in range(1,itr):
                    if board[ny,nx+i]!=0:
                        return False 
        else:
            itr = np.abs(ny-oy)
            if ny>oy:
                for i in range(1,itr):
                    if board[ny-i,nx]!=0:
                        return False
            if ny<oy:
                for i in range(1,itr):
                    if board[ny+i,nx]!=0:
                        return False        
        self.first_move = False                
        return True

class Queen(ChessPiece):
    def __init__(self, x, y, color, scene, emitter):
        super().__init__(x, y, color, {"black": BLACK_QUEEN, "white": WHITE_QUEEN}, scene, emitter)
        self.type = {"black": -5, "white": 5}[color]
        self.signal_emitter = emitter
    def is_move_legal(self,nx,ny,ox,oy,board):
       
        
        color_num = {"black": -1, "white": 1}[self.color]
        
        if board[ny,nx]*color_num>0:
            return False
        
            
        if nx==ox or ny==oy:
            #pasted from rook
            if nx!=ox:
                itr = np.abs(nx-ox)
                if nx>ox:
                    for i in range(1,itr):
                        if board[ny,nx-i]!=0:
                            return False
                if nx<ox:
                    for i in range(1,itr):
                        if board[ny,nx+i]!=0:
                            return False 
            else:
                itr = np.abs(ny-oy)
                if ny>oy:
                    for i in range(1,itr):
                        if board[ny-i,nx]!=0:
                            return False
                if ny<oy:
                    for i in range(1,itr):
                        if board[ny+i,nx]!=0:
                            return False            
        else:
            #pasted from bishop
            x_diff = np.abs(nx-ox)
            y_diff = np.abs(ny-oy)
            if y_diff!=x_diff:
                return False
            
            if nx>ox:
                if ny>oy:
                    for i in range(1,x_diff):
                        if board[ny-i,nx-i]!=0:
                            return False
                else:
                    for i in range(1,x_diff):
                        if board[ny+i,nx-i]!=0:
                            return False
            if nx<ox:
                if ny>oy:
                    for i in range(1,x_diff):
                        if board[ny-i,nx+i]!=0:
                            return False
                else:
                    for i in range(1,x_diff):
                        if board[ny+i,nx+i]!=0:
                            return False
                        
        return True
    
class King(ChessPiece):
    def __init__(self, x, y, color, scene, emitter):
        super().__init__(x, y, color, {"black": BLACK_KING, "white": WHITE_KING}, scene, emitter)
        self.type = {"black": -6, "white": 6}[color]
        self.first_move = True       
    def is_move_legal(self,nx,ny,ox,oy,board):
        
        
        x_diff = np.abs(nx-ox) 
        y_diff = np.abs(ny-oy)

        color_num = {"black": -1, "white": 1}[self.color]
        
            
        if board[ny,nx]*color_num>0:
            return False
        if y_diff>1:
            return False
        #if nx-ox==2 and self.first_move==True:
        #    if board[ny,nx-1]!=0:
        #        return False
        #    if self.parent.castle(nx+1,ny)==True:
        #        self.first_move = False
        #        return True
        #if nx-ox==-2 and self.first_move==True:
        #    if not(board[ny,nx+1]==0 and board[ny,nx-1]==0):
        #        return False
        #    if self.parent.castle(nx-2,ny)==True:
        #        self.first_move = False
        #        return True
        if x_diff>1:
            return False 
        
        
        
        self.first_move = False
        return True
      
class Emitter(QObject):
    sgnl = pyqtSignal(str)
