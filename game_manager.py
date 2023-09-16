import importlib.util
import sys
import os
from PIL import Image, ImageDraw
from appcg import session
current_username = session['username']
cwd_botfile = os.path.join(os.getcwd(), f'botfile_{current_username}.py')
spec = importlib.util.spec_from_file_location("UserBot", cwd_botfile)
foo = importlib.util.module_from_spec(spec)
sys.modules['UserBot'] = foo
spec.loader.exec_module(foo)
foo.UserBot()

import re
from CGEngine import CGBot

from static.botfiles.bot1 import UserBot
import random

#               ----READ ME PLS----
#   ROW = y, COLUMN = x. AS BOARD USES LIST NOTATION
# ==> board[y][x] == board[ROW][COLUMN]



board = [
    [-1, -1, -1, -1, -1],
    [-1,  0,  0,  0, -1],
    [ 1,  0,  0,  0, -1],
    [ 1,  0,  0,  0,  1],
    [ 1,  1,  1,  1,  1]
]
diag_pos = [(1,1), (1, 3), (3,1), (3,3)]

# Loops through board and gives locations of red and blue
def display():
    for row in game_state["board"]:
        for cell in row:
            if cell == -1:
                print("R", end=" ")  #red piece
            elif cell == 0:
                print(".", end=" ")
            elif cell == 1:
                print("B", end=" ")  #blue piece
        print()


# Generates random sides for each bots
def assign_side():
    assignment = random.choice([-1,1])
    return assignment


# Toggles turn back and forth
def toggle_turn():
    game_state["current_turn"] = game_state["current_turn"]*-1


# Is the main running function in game_manager
def run_game(board):
    player1 = CGBot(assign_side(), game_state["board"])
    player2 = UserBot(-player1.my_piece, game_state["board"])
    winner = None
    move = 1
    del_all_img()

    while winner is None:
        
        input_console = input("enter to continue...")

        if input_console == "del":
            del_all_img()

        if player1.my_piece == game_state["current_turn"]:
            player1.activate()
            game_state["board"] = board
        elif player2.my_piece == game_state["current_turn"]:
            board = player2.activate()
            game_state["board"] = board
        else:
            pass

        ganh_remove = ganh(game_state["current_turn"], -game_state["current_turn"], game_state["board"])
        chet_remove = chet(game_state["current_turn"], -game_state["current_turn"], game_state["board"])

        update_board(game_state["board"], ganh_remove, chet_remove)
        generate_image(game_state["board"], move)

        print("AFTER: \n----------")
        display()
        print("----------")
        toggle_turn()
        winner = game_over()
        move += 1
        
        if winner is not None:
            print(winner)
            break
    
    
def del_all_img():
    try:
        cwd = os.getcwd() #Get current directory
        img_dir = cwd + "/static/upload_video"
        images = os.listdir(img_dir)
        for file in images:
            file_path = os.path.join(img_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print("deletion successful")
    except OSError:
        print("OS error")




def ganh(piece, opp_piece, board):
    valid_remove = []
    opp_remove = []
    print(piece)

    print("BEFORE \n----------")
    display()
    print("----------")

    game_state["board"] = board
    ganh_pair = [[(1,0), (-1, 0)], [(0,1), (0, -1)]]
    ganh_pair2 = [[(1,0), (-1, 0)], [(0,1), (0, -1)], [(1,1), (-1,-1)], [(-1,1), (1,-1)]]

    pieces_pos = get_position(piece)

    #NOTE: position is saved as {"x": x, "y": y}
    for position in pieces_pos:
        print(position)
        if (position["y"], position["x"]) in diag_pos:
            # Loops through each pair and conclude the opponent piece
            for pair in ganh_pair2:
                for y, x in pair:
                    new_posx = position["x"] + x
                    new_posy = position["y"] + y
                    if 0 <= new_posy < len(board) and 0 <= new_posx < len(board[0]):
                        if board[new_posy][new_posx] == opp_piece:
                            opp_remove.append((new_posy, new_posx))
                            print("Recieved ganh2:", opp_remove)

                # Check if we have a pair
                if len(opp_remove) < 2:
                    opp_remove = []
                    pass
                else:
                    print("VALID GANH2")
                    valid_remove.extend(opp_remove)
                    opp_remove = []

        else:
            # Loops through each pair and conclude the opponent piece
            for pair in ganh_pair:
                for y, x in pair:
                    new_posx = position["x"] + x
                    new_posy = position["y"] + y
                    try: 
                        if 0 <= new_posy < len(board) and 0 <= new_posx < len(board[0]):
                            if board[new_posy][new_posx] == opp_piece:
                                opp_remove.append((new_posy, new_posx))
                                print("Recieved ganh:", opp_remove)
                    except IndexError:
                        pass

                if len(opp_remove) < 2:
                    opp_remove = []
                    pass
                else:
                    print("VALID GANH")
                    valid_remove.extend(opp_remove)
                    opp_remove = []        


    print("GANH VALID:", valid_remove)
    return valid_remove


def chet(piece, opp_piece, board):
    valid_remove = []
    ally_chet = []
    game_state["board"] = board
    chet_pair = [[(1,0), (-1, 0)], [(0,1), (0, -1)]]
    chet_pair2 = [[(1,0), (-1, 0)], [(0,1), (0, -1)], [(1,1), (-1,-1)], [(-1,1), (1,-1)]]

    opp_pieces_pos = get_position(opp_piece)

    #NOTE: position is saved as {"x": x, "y": y}
    for position in opp_pieces_pos:
        if (position["y"], position["x"]) in diag_pos:
            # Loops through each pair and conclude the opponent piece
            for pair in chet_pair2:
                for y, x in pair:
                    new_posx = position["x"] + x
                    new_posy = position["y"] + y
                    try:
                        if 0 <= new_posy < len(board) and 0 <= new_posx < len(board[0]):
                            if board[new_posy][new_posx] == piece:
                                ally_chet.append((new_posy, new_posx))
                                print("Recieved chet2:", ally_chet)

                    except IndexError:
                        pass
                if len(ally_chet) < 2:
                    ally_chet = []
                    pass
                else:
                    print("CHET VALID2")
                    valid_remove.append((position["y"], position["x"]))
                    ally_chet = []

        else:
            # Loops through each pair and conclude the opponent piece
            for pair in chet_pair:
                for y, x in pair:
                    new_posx = position["x"] + x
                    new_posy = position["y"] + y
                    try:
                        if 0 <= new_posy < len(board) and 0 <= new_posx < len(board[0]):
                            if board[new_posy][new_posx] == piece:
                                ally_chet.append((new_posy, new_posx))
                                print("Recieved chet:", ally_chet)

                    except IndexError:
                        pass

                if len(ally_chet) < 2:
                    ally_chet = []
                    pass
                else:
                    print("CHET VALID")
                    valid_remove.append((position["y"], position["x"]))
                    ally_chet = []

    print("CHET VALID:", valid_remove)
    return valid_remove


def update_board(board, ganh_remove=None, chet_remove=None):
    execute = []

    if ganh_remove:
        execute.extend(ganh_remove)
    
    if chet_remove:
        execute.extend(chet_remove)

    print("EXECUTION:", execute)
    for row, column in execute:
        board[row][column] = 0

    if execute:
        return board
    else:
        pass


def game_over():
    if not get_position(1): 
        return "red wins"
    elif not get_position(-1):
        return "blue wins"
    elif len(get_position(1)) == 1 and len(get_position(-1)) == 1:
        return "Tie"
    else:
        return None


# Get positions of required color
def get_position(color):
    positions = []
    for row in range(len(board)):
        for column in range(len(board[0])):
            if board[row][column] == color:
                positions.append({"x": column, "y": row})
    return positions


def generate_video():
    cwd = os.getcwd()
    img_dir = cwd + "/static/upload_video/"
    out_vid_dir = cwd + "/cg-replay/"
    out_vid_name = "cg-replay.mp4"
    vid_path = out_vid_dir + out_vid_name

    images = os.listdir(img_dir)
    img_list = []

    for file in images:
        re.compiler


def generate_image(board, move):
    image = Image.new("RGB", (600, 600), "WHITE")
    draw = ImageDraw.Draw(image)

    draw.line((100, 100, 500, 100), fill="black", width=3)
    draw.line((100, 200, 500, 200), fill="black", width=3)
    draw.line((100, 300, 500, 300), fill="black", width=3)
    draw.line((100, 400, 500, 400), fill="black", width=3)
    draw.line((100, 500, 500, 500), fill="black", width=3)
    draw.line((100, 100, 100, 500), fill="black", width=3)

    draw.line((200, 100, 200, 500), fill="black", width=3)
    draw.line((300, 100, 300, 500), fill="black", width=3)
    draw.line((400, 100, 400, 500), fill="black", width=3)
    draw.line((500, 100, 500, 500), fill="black", width=3)
    draw.line((100, 100, 500, 500), fill="black", width=3)
    draw.line((100, 500, 500, 100), fill="black", width=3)

    draw.line((100, 300, 300, 100), fill="black", width=3)
    draw.line((300, 100, 500, 300), fill="black", width=3)
    draw.line((500, 300, 300, 500), fill="black", width=3)
    draw.line((300, 500, 100, 300), fill="black", width=3)

    x = 80
    y = 80 
    for row in range(len(board)):
        for column in range(len(board[0])):
            if board[row][column] == -1:
                draw.ellipse((x, y, x + 40, y + 40), fill="red", outline="red")
            elif board[row][column] == 1:
                draw.ellipse((x, y, x + 40, y + 40), fill="blue", outline="blue")
            else:
                pass
            x = x + 100
        x = 80
        y = y + 100

    cwd = os.getcwd()
    img_dir = cwd + "/static/upload_video"

    image.save(f"{img_dir}/chessboard{move}.png", "PNG")


game_state = {
            "board": board,
            "current_turn": 1
}

if __name__ == "__main__":
    run_game(board)


