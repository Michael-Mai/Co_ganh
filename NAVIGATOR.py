import tkinter as tk
from tkinter import ttk
from tkinter import *

class AppCoGanh(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('vietnamese chess')
        self.minsize(400, 400)

     

        Frame_container = tk.Frame(self)
        Frame_container.pack(fill=BOTH, expand=TRUE)
        Frame_container.grid_rowconfigure(0,weight=1)
        Frame_container.grid_columnconfigure(0,weight=1)

        #Chuyển qua lại giữa các Frames và các chức năng nút của màn hình chính (MHC)
        self.frames = {}
        for F in (CoGanhUI, BanCo, DHL):
            print(F)
            page_name = F.__name__
            frame = F(parent=Frame_container,controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky=NSEW)

        self.frame_open("CoGanhUI")
    
    def frame_open(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
    
    def thoat_game(self):
        self.destroy()


class CoGanhUI(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        


        self.style = ttk.Style()
        self.style.configure('TButton', font =('Helvetica', 11 ), borderwidth = '4')
        self.style.map('TButton', foreground = [('active', 'green')], background = [('active', 'blue')])

       
        Thoat_Game = ttk.Button(self, text='Thoát', command=lambda: controller.thoat_game()).pack(padx=5, pady=5, side=BOTTOM)
        DauHangLoat = ttk.Button(self, text='Đấu hàng loạt', command=lambda: controller.frame_open("DHL")).pack(padx=5, pady=5, side=BOTTOM)
        Start = ttk.Button(self, text='Bắt Đầu', command=lambda: controller.frame_open('BanCo')).pack(padx=5, pady=5, side=BOTTOM)

        DropmenuVAR1 = StringVar()
        DropmenuVAR2 = StringVar()
        Dropmenu_PLAYER1 = ttk.Combobox(self, textvariable=DropmenuVAR1, values=('Người chơi 1', 'Máy'), state='readonly', justify='center').pack(padx=5, pady=20, side=LEFT)
        Dropmenu_PLAYER2 = ttk.Combobox(self, textvariable=DropmenuVAR2, values=('Người chơi 2', 'Máy'), state='readonly', justify='center').pack(padx=5, pady=20, side=RIGHT)
        
        self.pack()


class BanCo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        HEIGHT = 500
        WIDTH = 500
        BORDER = 50
        LINE_WIDTH = 2
        MINIPOINT_R = 4
        PIECE_R = 15
        BG = 'white'
        MINIPOINT_COLOR = 'black'
        P1_COLOR = 'blue'
        P2_COLOR = 'red'

        canvas = Canvas(self , width = WIDTH, height = HEIGHT, bg = BG)

        Quay_Lai = ttk.Button(self, text='Back', command=lambda: controller.frame_open('CoGanhUI')).pack(padx=5 , pady=5, side=RIGHT)
        A1 = BORDER, BORDER
        A2 = BORDER+(WIDTH-2*BORDER)/4, BORDER
        A3 = WIDTH/2, BORDER
        A4 = BORDER+(WIDTH-2*BORDER)/4*3, BORDER
        A5 = WIDTH - BORDER, BORDER
        B1 = BORDER, BORDER+(HEIGHT-2*BORDER)/4
        B2 = BORDER+(WIDTH-2*BORDER)/4, BORDER+(HEIGHT-2*BORDER)/4
        B3 = WIDTH/2, BORDER+(HEIGHT-2*BORDER)/4
        B4 = BORDER+(WIDTH-2*BORDER)/4*3, BORDER+(HEIGHT-2*BORDER)/4
        B5 = WIDTH - BORDER, BORDER+(HEIGHT-2*BORDER)/4
        C1 = BORDER, HEIGHT/2
        C2 = BORDER+(WIDTH-2*BORDER)/4, HEIGHT/2
        C3 = WIDTH/2, HEIGHT/2
        C4 = BORDER+(WIDTH-2*BORDER)/4*3, HEIGHT/2
        C5 = WIDTH - BORDER, HEIGHT/2
        D1 = BORDER, BORDER+(HEIGHT-2*BORDER)/4*3
        D2 = BORDER+(WIDTH-2*BORDER)/4, BORDER+(HEIGHT-2*BORDER)/4*3
        D3 = WIDTH/2, BORDER+(HEIGHT-2*BORDER)/4*3
        D4 = BORDER+(WIDTH-2*BORDER)/4*3, BORDER+(HEIGHT-2*BORDER)/4*3
        D5 = WIDTH - BORDER, BORDER+(HEIGHT-2*BORDER)/4*3
        E1 = BORDER, HEIGHT - BORDER
        E2 = BORDER+(WIDTH-2*BORDER)/4, HEIGHT - BORDER
        E3 = WIDTH/2, HEIGHT - BORDER
        E4 = BORDER+(WIDTH-2*BORDER)/4*3, HEIGHT - BORDER
        E5 = WIDTH - BORDER, HEIGHT - BORDER

        #HORIZONTAL LINES
        canvas.create_line(A1, A5, width = LINE_WIDTH)
        canvas.create_line(B1, B5, width = LINE_WIDTH)
        canvas.create_line(C1, C5, width = LINE_WIDTH)
        canvas.create_line(D1, D5, width = LINE_WIDTH)
        canvas.create_line(E1, E5, width = LINE_WIDTH)

        #VERTICAL LINES
        canvas.create_line(A1, E1, width = LINE_WIDTH)
        canvas.create_line(A2, E2, width = LINE_WIDTH)
        canvas.create_line(A3, E3, width = LINE_WIDTH)
        canvas.create_line(A4, E4, width = LINE_WIDTH)
        canvas.create_line(A5, E5, width = LINE_WIDTH)

        #DIAGONAL LINES
        canvas.create_line(A1, E5, width = LINE_WIDTH)
        canvas.create_line(A5, E1, width = LINE_WIDTH)
        canvas.create_line(C1, A3, width = LINE_WIDTH)
        canvas.create_line(A3, C5, width = LINE_WIDTH)
        canvas.create_line(C5, E3, width = LINE_WIDTH)
        canvas.create_line(E3, C1, width = LINE_WIDTH)

        #MINI POINTS
        mini_points = [A1, A2, A3, A4, A5, B1, B2, B3, B4, B5, C1, C2, C3, C4, C5, D1, D2, D3, D4, D5, E1, E2, E3, E4, E5]
        for i in mini_points:
            canvas.create_oval(i[0] + MINIPOINT_R, i[1] - MINIPOINT_R, i[0] - MINIPOINT_R, i[1] + MINIPOINT_R, fill = MINIPOINT_COLOR)


        #CHESS PIECES
        chess_points_P2 = [A1, A2, A3, A4, A5, B1, B5, C5]
        for i in chess_points_P2:
            canvas.create_oval(i[0] + PIECE_R, i[1] - PIECE_R, i[0] - PIECE_R, i[1] + PIECE_R, fill = P2_COLOR)

        chess_points_P1 = [C1, D1, D5, E1, E2, E3, E4, E5]
        for i in chess_points_P1:
            canvas.create_oval(i[0] + PIECE_R, i[1] - PIECE_R, i[0] - PIECE_R, i[1] + PIECE_R, fill = P1_COLOR)


        canvas.pack()
        
class DHL(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        Label1 = ttk.Label(self, text="Chua co Dau Hang Loat").pack(side=TOP)
        Button1 = ttk.Button(self, text='Back', command=lambda: controller.frame_open('CoGanhUI')).pack(padx=5 , pady=5, side=RIGHT)




if __name__  == '__main__':
    Window = AppCoGanh()
    Window.mainloop()






