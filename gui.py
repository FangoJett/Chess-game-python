import sys
from PyQt5.QtWidgets import QGraphicsProxyWidget,QDialog ,QGraphicsTextItem, QWidget, QLabel ,QVBoxLayout, QSlider, QPushButton, QTextEdit, QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QMainWindow, QBoxLayout, QGraphicsItem, QGraphicsRectItem
from PyQt5.QtGui import QPixmap, QImage, QBrush, QPen, QFont, QColor
from PyQt5.QtCore import QTimer, QSize, Qt, pyqtSignal, QRectF, QObject,pyqtSlot
from figures import Pawn, Bishop, Rook, Queen, King, Knight, ChessPiece, Emitter
import numpy as np
from radio import RadioWidget
from ip_option import InputDialog, InputDialogShort
import json
import xml.etree.ElementTree as ET
import sqlite3
import os
import socket
import threading

FORMAT = 'utf-8'

infinity = 99999999999


d_abc = {
    'a': 0,
    'b': 75,
    'c': 150,
    'd': 225,
    'e': 300,
    'f': 375,
    'g': 450,
    'h': 525,
}

d_123 = {
    '8': 0,
    '7': 75,
    '6': 150,
    '5': 225,
    '4': 300,
    '3': 375,
    '2': 450,
    '1': 525,
}


d_fig = {
    'p':1,
    'r':2,
    'n':3,
    'b':4,
    'q':5,
    'k':6
}
d_fig2 = {
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



class TimerItem(QGraphicsTextItem):
    def __init__(self,color,parent, alt: bool):
        super().__init__()
        
        self.alt_mode = alt
        self.parent = parent
        self.color = color
        self.remaining_time = 900  # 15 mins
        self.setFont(QFont("Arial", 24))
        self.setDefaultTextColor(Qt.black)
        self.update_display()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  
        
    def update_time(self):
        if self.color==self.parent.whos_turn and self.parent.game_started:
            self.remaining_time -= 1
        self.update_display()
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.setPlainText(f"{minutes:02}:{seconds:02}")
        
        if self.remaining_time <= 0:
            self.timer.stop()
            #Tutaj przegrana dodac
            
    def update_display(self):
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.setPlainText(f"{minutes:02}:{seconds:02}")

    def add_time(self,color):
        if self.alt_mode and str(self.color)==str(color):
            self.remaining_time+=3

        
 
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.player_color = ""
        self.session_number = 1
        self.game_started: bool = False
        self.timer_on: bool = True
        self.player_option: int = 0
        self.address = "0"
        self.port = 0
        self.scene = QGraphicsScene()
        self.setWindowTitle("Szachy")
        self.setGeometry(100, 100, 1000, 700)
        self.create_ui()
        
        

        
        
        self.info_window = InfoWindow()

        
    def add_timers(self, alt: bool):
        self.white_timer = TimerItem("white",self,alt)
        self.black_timer = TimerItem("black",self,alt)

        self.white_timer.setPos(660, 500)
        self.black_timer.setPos(660, 50)

        self.scene_info.addItem(self.white_timer)
        self.scene_info.addItem(self.black_timer)
        


    def create_ui(self):
        
        
        
        #scene with chessboard
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0,0,600,600)

        self.view = QGraphicsView(self.scene,self)
        self.view.setGeometry(0,0,600,600)
        image = QImage('images/chessboard.png')
        self.scene.setBackgroundBrush(QBrush(image))
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        
        #scene with button and timers
        self.scene_info = QGraphicsScene(self)
        self.scene_info.setSceneRect(650,0,150,600)
        self.view_info = QGraphicsView(self.scene_info,self)

        
        self.scene_info.setBackgroundBrush(QColor('white'))
        self.view_info.setGeometry(650,0,150,600)
        self.view_info.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view_info.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  
             

        #add buttons
        button_start_timers = QPushButton("Start classic")
        button_start_timers.clicked.connect(self.start_with_timers)
        button_blitz_timers = QPushButton("Start blitz")
        button_blitz_timers.clicked.connect(self.start_blitz)
        self.button1 = self.scene_info.addWidget(button_start_timers)
        self.button1.setPos(660,250)
        self.button2 = self.scene_info.addWidget(button_blitz_timers)
        self.button2.setPos(660,300)
        
        
        radio_buttons_var = RadioWidget(self)
        self.radio_buttons = self.scene_info.addWidget(radio_buttons_var)
        self.radio_buttons.setPos(660,50)
        
        
        #add board numeration
        self.scene_y = QGraphicsScene(self)
        self.scene_y.setSceneRect(600,0,50,600)
        self.view_y = QGraphicsView(self.scene_y,self)
        self.scene_y.setBackgroundBrush(QColor('white'))
        self.view_y.setGeometry(600,0,50,600)
        self.view_y.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view_y.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  
        imagey = QImage('images/123.png')
        self.scene_y.setBackgroundBrush(QBrush(imagey))
        
        
        self.scene_x = QGraphicsScene(self)
        self.scene_x.setSceneRect(0,600,600,50)

        self.view_x = QGraphicsView(self.scene_x,self)
        self.scene_x.setBackgroundBrush(QColor('white'))
        self.view_x.setGeometry(0,600,600,50)
        self.view_x.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view_x.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff) 
        imagex = QImage('images/abc.png')
        self.scene_x.setBackgroundBrush(QBrush(imagex))
        
        
        self.show()
        self.addContent()
        
    def addContent(self):
        
        
        self.emitter = Emitter()
        self.emitter.sgnl.connect(self.log_move)
        
        self.online_emitter = Emitter()
        self.online_emitter.sgnl.connect(self.move_to_gui)
        

        for i in range(8):
            self.scene.addItem(Pawn(0+75*i,75,"black", self, self.emitter))
        for i in range(8):
            self.scene.addItem(Pawn(0+75*i,450,"white", self, self.emitter))       

        self.scene.addItem(Rook(0,525,"white", self, self.emitter))   
        self.scene.addItem(Rook(525,525,"white", self, self.emitter))   
        
        self.scene.addItem(Rook(0,0,"black", self, self.emitter))   
        self.scene.addItem(Rook(525,0,"black",self, self.emitter))   
        
        self.scene.addItem(Knight(75,525,"white", self, self.emitter))   
        self.scene.addItem(Knight(450,525,"white", self, self.emitter))   
        
        self.scene.addItem(Knight(75,0,"black", self, self.emitter))   
        self.scene.addItem(Knight(450,0,"black",self, self.emitter))   
        
        self.scene.addItem(Bishop(150,0,"black", self, self.emitter))   
        self.scene.addItem(Bishop(375,0,"black", self, self.emitter))   

        self.scene.addItem(Bishop(150,525,"white",self, self.emitter))   
        self.scene.addItem(Bishop(375,525,"white",self, self.emitter))   
        
        self.scene.addItem(Queen(225,0,"black", self,self.emitter))

        self.scene.addItem(Queen(225,525,"white", self,self.emitter))
        
        self.scene.addItem(King(300,0,"black", self, self.emitter))   
        
        self.scene.addItem(King(300,525,"white", self, self.emitter)) 
        
        
        ############
        self.scene_calc = QGraphicsScene(self)
        self.scene_calc.addItem(Pawn(75,75,"black", self, self.emitter))
        self.scene_calc.addItem(Pawn(75,75,"white", self, self.emitter))
        self.scene_calc.addItem(Knight(75,0,"black", self, self.emitter))   
        self.scene_calc.addItem(Knight(450,0,"black",self, self.emitter))   
        self.scene_calc.addItem(Bishop(150,0,"black", self, self.emitter))   
        self.scene_calc.addItem(Bishop(375,0,"black", self, self.emitter))
        self.scene_calc.addItem(Queen(225,0,"black", self,self.emitter))
        self.scene_calc.addItem(Queen(225,525,"white", self,self.emitter))
        self.scene_calc.addItem(King(300,0,"black", self, self.emitter))   
        self.scene_calc.addItem(King(300,525,"white", self, self.emitter))
        self.scene_calc.addItem(Rook(525,525,"white", self, self.emitter))     
        self.scene_calc.addItem(Rook(0,0,"black", self, self.emitter)) 
        ######
        self.initial_board_state = [
        [ -2, -3, -4, -5, -6, -4, -3, -2],
        [ -1, -1, -1, -1, -1, -1, -1, -1],
        [  0,  0,  0,  0,  0,  0,  0,  0],
        [  0,  0,  0,  0,  0,  0,  0,  0],
        [  0,  0,  0,  0,  0,  0,  0,  0],
        [  0,  0,  0,  0,  0,  0,  0,  0],
        [  1,  1,  1,  1,  1,  1,  1,  1],
        [  2,  3,  4,  5,  6,  4,  3,  2]]
        
        self.whos_turn = "white"
        
        """ 
            0 - nothing
            Black < 0 , White > 0 
            1 - Pawn
            2 - Rook
            3 - Knight
            4 - Bishop
            5 - Queen
            6 - King
        """

            
        self.board = np.array(self.initial_board_state, dtype=int)
        self.check: int = 0 
        """
         0 - no check
         1 - black is being checked
        -1 - white is being checked
        """
    def add_text_gui(self):
        
        
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText("")
        font = QFont("Arial", 20) 
        self.text_edit.setFont(font)
      
        self.text_edit_proxy = QGraphicsProxyWidget()
        self.text_edit_proxy.setWidget(self.text_edit)
        self.text_edit_proxy.setGeometry(QRectF(660, 300, 120, 0))
        
        self.scene_info.addItem(self.text_edit_proxy)
        self.text_edit_proxy.setPos(660, 300)

        
        button_move = QPushButton("Make move")
        button_move.clicked.connect(self.get_text)
        self.button3 = self.scene_info.addWidget(button_move)
        self.button3.setPos(660,270)
  
        
    def upp_time(self,color):
        for item in self.scene_info.items():
            if isinstance(item,TimerItem):
                item.add_time(color) 
    def can_move(self,x,y):
        x = int(x)
        y = int(y)
        if self.blocked[x,y]!=0:
            return False
        return True
    
    def castle(self,var_x,var_y):
        for item in self.scene.items():
            if isinstance(item, Rook) and item.first_move==True and item.posx==var_x*75 and item.posy==var_y*75:
                if var_x==7:
                    nx = 5
                if var_x==0:
                    nx = 3
                item.first_move==False
                if item.color=="white":
                    item.setPos(nx*75, 7*75)
                    self.board[7,nx]=2
                    self.board[7,var_x]=0
                    item.posx = item.x()
                    item.posy = item.y() 
                    return True
                if item.color=="black":
                    item.setPos(nx*75, 0)
                    self.board[0,nx]=2
                    self.board[0,var_x]=0
                    item.posx = item.x()
                    item.posy = item.y()
                    return True  
        return False    
    
    def get_text(self):
        text = self.text_edit.toPlainText()  
        self.text_edit.clear()
        if text[0]=="/":
            self.send(text)
        else:
            self.make_move(text) 
        
    
    def make_move(self,text):
        if len(text)==3:
            fig = d_fig[text[0]] *{"black":-1,"white":1}[self.whos_turn]
            x = d_abc[text[1]]
            y = d_123[text[2]]
 
            xp = int(x/75)
            yp = int(y/75)
           
            for item in self.scene.items():
                if isinstance(item, ChessPiece) and item.type == fig and item.color == self.whos_turn:
                    
                    
                    if item.is_move_legal(xp,yp,int(item.posx/75),int(item.posy/75),self.board):
                        if self.board[yp,xp]!=0:
                            self.remove_piece(xp*75,yp*75)
                        self.add_move(text)
                        item.setPos(x, y)
                        item.parent.board[yp,xp]=item.type
                        ox = int(item.posx/75)
                        oy = int(item.posy/75)
                        self.board[oy,ox]=0
                        item.posx = item.x()
                        item.posy = item.y()
                        item.parent.upp_time(item.color)
                        #self.check_check(self.board)
                        item.move_signal.sgnl.emit(f"Move:{item.color} {item.__class__.__name__} from position {ox}, {oy} to position {xp}, {yp}.")
                        self.change_turns() 
            
        if len(text)==5:
            fig = d_fig[text[0]] *{"black":-1,"white":1}[self.whos_turn]
            x_dem = d_abc[text[1]]
            y_dem = d_123[text[2]]
            x = d_abc[text[3]]
            y = d_123[text[4]]
                        
            xp = int(x/75)
            yp = int(y/75)

            for item in self.scene.items():
                if isinstance(item, ChessPiece) and item.type == fig and item.color == self.whos_turn and item.posx==x_dem and item.posy==y_dem:
                    
                    
                    if item.is_move_legal(xp,yp,int(item.posx/75),int(item.posy/75),self.board):
                        if self.board[yp,xp]!=0:
                            self.remove_piece(xp*75,yp*75)
                        
                        ox = int(item.posx/75)
                        oy = int(item.posy/75)
                        
                        self.add_move(text)
                        item.setPos(x, y)
                        item.parent.board[yp,xp]=item.type
                        
                        item.parent.board[oy,ox]=0
                        item.posx = item.x()
                        item.posy = item.y()
                        item.parent.upp_time(item.color) 
                        #self.check_check(self.board)
                        item.move_signal.sgnl.emit(f"Move:{item.color} {item.__class__.__name__} from position {ox}, {oy} to position {xp}, {yp}.")
                        self.change_turns()
                        
        if len(text)==4:
            fig = d_fig[text[0]] *{"black":-1,"white":1}[self.whos_turn]
            num_bool = False
            if text[1].isdigit():
                dem = d_123[text[1]]
                num_bool = True
            else:
                dem = d_abc[text[1]]
            x = d_abc[text[2]]
            y = d_123[text[3]]
                        
            xp = int(x/75)
            yp = int(y/75)

            for item in self.scene.items():
                if isinstance(item, ChessPiece) and item.type == fig and item.color == self.whos_turn:
                    if num_bool:
                        pos = item.posy
                    else:
                        pos = item.posx
                    if pos==dem:
                        if item.is_move_legal(xp,yp,int(item.posx/75),int(item.posy/75),self.board):
                            if self.board[yp,xp]!=0:
                                self.remove_piece(xp*75,yp*75)
                            
                            self.add_move(text)
                            item.setPos(x, y)
                            item.parent.board[yp,xp]=item.type
                            ox = int(item.posx/75)
                            oy = int(item.posy/75)
                            self.board[oy,ox]=0
                            item.posx = item.x()
                            item.posy = item.y()
                            item.parent.upp_time(item.color)
                            #self.check_check(self.board)
                            item.move_signal.sgnl.emit(f"Move:{item.color} {item.__class__.__name__} from position {ox}, {oy} to position {xp}, {yp}.")
                            self.change_turns()                        
             
    
    
    def log_move(self, message):
        self.info_window.text_edit.append(message)

    def change_turns(self):
        if self.whos_turn =="black":
            self.whos_turn = "white"
            #text = self.minmax(self.board,self.whos_turn,2,True)
            #print(text)
            
        else:
            self.whos_turn = "black"
            text,scor = self.minmax(self.board,self.whos_turn,True,2,-999999999,9999999999)
            
            self.ai_move(text)
            
    def remove_piece(self,x,y):
         for item in self.scene.items():
            if isinstance(item, ChessPiece) and item.posx==x and item.posy==y:
                self.scene.removeItem(item)

    def set_items_movable(self):
        for item in self.scene.items():
            if isinstance(item, ChessPiece):
                item.setFlag(item.ItemIsMovable)


                
    def start_with_timers(self):
        self.add_timers(False)
        
        for item in self.scene_info.items():
            if isinstance(item, QGraphicsProxyWidget):
                widget = item.widget()
                if isinstance(widget, QPushButton) or isinstance(widget, RadioWidget):
                    self.scene_info.removeItem(item)
        self.add_text_gui() 
         
        self.ip_option_window()
        self.init_game_data()
        self.init_save_button()
        
    def start_blitz(self):
        
        self.add_timers(True)
        
        for item in self.scene_info.items():
            if isinstance(item, QGraphicsProxyWidget):
                widget = item.widget()
                if isinstance(widget, QPushButton) or isinstance(widget, RadioWidget):
                    self.scene_info.removeItem(item)
        self.add_text_gui()  
         
        self.ip_option_window()
        self.init_game_data()
        self.init_save_button()
        
    def check_check(self,board_var):
        color_num: int = {"black": -1, "white": 1}[self.whos_turn]
        y,x = np.where(board_var==-6*color_num)
       
        for item in self.scene.items():
            if isinstance(item, ChessPiece) and item.color == self.whos_turn:
                ox = int(item.posx/75)
                oy = int(item.posy/75)
                ny =y[0]
                nx =x[0] 
                if item.is_move_legal(nx,ny,ox,oy,board_var):
                    self.check = color_num
                    print(self.check)
                    
                    
    def ip_option_window(self):
        if self.player_option == 2:
            self.showInputDialog()
        elif self.player_option==3:
            self.showInputDialogShort()
        else:
            self.set_items_movable()
            self.game_started = True
     
            
    def showInputDialog(self):
        dialog = InputDialog()
        result = dialog.exec_()  

        if result == QDialog.Accepted:
            addr = dialog.entry1.text()
            prt = dialog.entry2.text()
            
            #!!!!!!!!!!!!!!!!!!!!!
            self.connect_to_server(addr,prt)
            
            self.address = addr
            self.port = prt
            
            
        else:
            self.set_items_movable
            
            
    def showInputDialogShort(self):
        dialog = InputDialogShort()
        result = dialog.exec_()  
        
        if result == QDialog.Accepted:
            
            prt = dialog.entry2.text()
            #START SERVER!!!!!!!!!!!!!!!!!
            self.port = prt
            self.addrres = 'localhost'
            self.server_thread = threading.Thread(target=self.create_server)
            self.server_thread.start()
            
            
            
            
        else:
            self.set_items_movable    
            
            
            
    def create_server(self):
        self.int_port = int(self.port)
        self.ADDR = (self.addrres,self.int_port)
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        self.start_server()
        
    def start_server(self):
        self.server.listen()
        self.conn, self.addr = self.server.accept()
        #client_thread = threading.Thread(target=self.handle_client, args=(self.conn, self.addr))
        #client_thread.start()
        self.game_started = True
        self.player_color = "white"
        self.move_only_ur_color()
        self.handle_client()
        
    def handle_client(self):
        connected = True
        while connected:
            try:
                move = self.conn.recv(128).decode(FORMAT)
                
                
                
                if move[0]=="/":
                    self.emitter.sgnl.emit(f"Opponent: {move[1:]}")
                else:
                    self.online_emitter.sgnl.emit(move)
            except KeyboardInterrupt:
                break
        
    def send(self,msg):
        message = msg.encode(FORMAT)
        self.conn.send(message)     
    
    def move_to_gui(self,move):
        print("emitted:",move)
        self.make_move(move)

        
        
        
        
   
    def connect_to_server(self,addr,port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((addr, int(port)))
        self.conn = self.client_socket
        self.player_color = "black"
        self.move_only_ur_color()
        self.game_started = True
        self.client_thread = threading.Thread(target=self.comm_with_server)
        self.client_thread.start()
        
        
    def comm_with_server(self):
        while True:
            try:
                move = self.client_socket.recv(1024).decode(FORMAT)
                if move[0]=="/":
                    self.emitter.sgnl.emit(f"Opponent: {move[1:]}")
                else:
                    self.online_emitter.sgnl.emit(move)
                
            except KeyboardInterrupt:
                break

     
        self.client_socket.close()
        
    
    def move_only_ur_color(self):
        for item in self.scene.items():
            if isinstance(item, ChessPiece):
                if item.color == self.player_color:
                    item.setFlag(item.ItemIsMovable)
    
    def init_game_data(self):
        self.game_data = {
            "mode": self.player_option,
            "session_number": self.session_number,
            "address": self.address,
            "port": self.port,
            "timer_white":self.white_timer.remaining_time,
            "timer_black":self.black_timer.remaining_time,
            "moves": []  
        }
        
    def add_move(self, move):
        self.game_data["moves"].append(move)
        
    def init_save_button(self):
        button_save = QPushButton("save game")
        button_save.clicked.connect(self.save_game)
        self.button3 = self.scene_info.addWidget(button_save)
        self.button3.setPos(660,100)
         
        
    
    def save_to_json(self):
        self.game_data["timer_white"] = self.white_timer.remaining_time
        self.game_data["timer_black"] = self.black_timer.remaining_time
        with open(f"game_data_{self.session_number}.json", "w") as f:
            json.dump(self.game_data, f)
    
    
    def save_game(self):
        self.save_to_json()
        self.save_to_xml()
        self.save_to_sql()
        self.open_json()
        
    def open_json(self):
        with open(f"game_data_{self.session_number}.json", "r") as json_file:
            data = json.load(json_file)
            
            
            val1 = data["mode"]
            val2 = data["session_number"]
            val3 = data["address"]
            val4 = data["port"]
            val5 = data["timer_white"]
            val6 = data["timer_black"]
            val7 = data["moves"]
        
        
    def save_to_xml(self):
        root = ET.Element("game_data")

        mode_element = ET.SubElement(root, "mode")
        mode_element.text = str(self.game_data["mode"])

        session_number_element = ET.SubElement(root, "session_number")
        session_number_element.text = str(self.game_data["session_number"])

        address_element = ET.SubElement(root, "address")
        address_element.text = self.game_data["address"]

        port_element = ET.SubElement(root, "port")
        port_element.text = str(self.game_data["port"])

        moves_element = ET.SubElement(root, "moves")
        for move in self.game_data["moves"]:
            move_element = ET.SubElement(moves_element, "move")
            move_element.text = move
        tree = ET.ElementTree(root)
        tree.write(f"game_data_{self.session_number}.xml")

    def save_to_sql(self):
        connection = sqlite3.connect(f"game_data_{self.session_number}.db")
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_data (
            game_id INTEGER PRIMARY KEY AUTOINCREMENT,
            mode INTEGER,
            session_number INTEGER,
            address TEXT,
            port INTEGER,
            moves TEXT
        )
        """)

        cursor.execute("""
        INSERT INTO game_data (mode, session_number, address, port, moves)
        VALUES (?, ?, ?, ?, ?)
        """, (self.game_data["mode"], self.game_data["session_number"], self.game_data["address"], self.game_data["port"], json.dumps(self.game_data["moves"])))

        connection.commit()
        connection.close()
    
    

       
    def get_all_moves(self,board,color):
        all_moves = []
        
        for xa in range(8):
            for ya in range(8):
                if board[ya,xa]!=0:
                    ox = xa
                    oy= ya
                    for x in range(8):
                        for y in range(8):
                            if self.is_move_ok(color,board[ya,xa],x,y,ox,oy,board):
                                word = f'{ox}{oy}{x}{y}'
                                all_moves.append(word)
        
        return all_moves
       
       
    def minmax(self, board, color, maximizing, depth, alpha, beta):
        if depth == 0:
            return None, calculate_board_value(self.board, board, 'black')

        moves = self.get_all_moves(board, color)
        best_move = "0000"

        if maximizing:
            biggest = -infinity
            for move in moves:
                ox = int(move[0])  # current x of piece
                oy = int(move[1])  # current y of piece
                nx = int(move[2])  # possible new x of piece
                ny = int(move[3])  # possible new y of piece
                board_next = self.array_move(board, nx, ny, ox, oy)  # new possible board state after making move
                current_val = self.minmax(board_next, opposite_color(color), False, depth - 1, alpha, beta)[1]
                if current_val > biggest:
                    biggest = current_val
                    best_move = move
                alpha = max(alpha, biggest)
                if beta <= alpha:
                    break
            return best_move, biggest
        else:
            lowest = infinity
            for move in moves:
                ox = int(move[0])
                oy = int(move[1])
                nx = int(move[2])
                ny = int(move[3])
                board_next = self.array_move(board, nx, ny, ox, oy)
                current_val = self.minmax(board_next, opposite_color(color), True, depth - 1, alpha, beta)[1]
                if current_val < lowest:
                    lowest = current_val
                    best_move = move
                beta = min(beta, lowest)
                if beta <= alpha:
                    break
            return best_move, lowest

                
                
                
       
    def is_move_ok(self, color1, number,nx,ny,ox,oy,board):
        if number<0:
            color="black"
        else:
            color="white"
        
        if color!=color1:
            return False
            
        num = np.abs(number)
        
        if num==1:
            piece = Pawn(110,110,color, self, self.emitter)
        elif num==2:
            piece = Rook(110,110,color, self, self.emitter) 
        elif num==3:
            piece = Knight(110,110,color, self, self.emitter) 
        elif num==4:
            piece = Bishop(0,110,color, self, self.emitter)  
        elif num==5:
            piece = Queen(0,0,color, self, self.emitter) 
        elif num==6:
            piece = King(0,0,color, self, self.emitter)      
        return piece.is_move_legal(nx,ny,ox,oy,board)
                
                
                
    def array_move(self,board,nx,ny,ox,oy):
        boardc = np.copy(board)
        o = board[oy,ox]
        #n = boardc[ny,nx]
        boardc[oy,ox] = 0
        boardc[ny,nx] = o
        return boardc

    def ai_move(self,val):
        fig = d_fig2[np.abs(self.board[int(val[1]),int(val[0])])]
        v1 = d_s[int(val[0])]
        v2 = d_n[int(val[1])]
        v3 = d_s[int(val[2])]
        v4 = d_n[int(val[3])]
        
        
        text = f'{fig}{v1}{v2}{v3}{v4}'
        print(text)
        self.make_move(text)
        
        






def opposite_color(color):
    if color=="black":
        return "white"
    else:
        return "black"

def calculate_board_value(starting_board,board,color):
    
    if color=="black":
        target = -1
    else:
        target = 1
    
    
    sum_now = 0
    sum_then = 0
    for x in range(8):
        for y in range(8):
            sum_now += board[y,x]*target
            sum_then += starting_board[y,x]*target
    if sum_now-sum_then!=0:
        ...#print(sum_now,sum_then)
    return sum_now-sum_then
            
    



class InfoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Logg info")
        self.setGeometry(900, 100, 400, 200)
        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(0, 0, 400, 200)
        self.text_edit.setReadOnly(True)
        
        
        self.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    chessboard = MainWindow()
    sys.exit(app.exec_())


