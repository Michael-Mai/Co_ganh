import random
import os
from PIL import Image, ImageDraw
import copy
from importlib.machinery import SourceFileLoader
import math



def load_player(option, session_name):
    cwd = os.getcwd()
    current_session_username = session_name
    current_user_file = f'botfile_{current_session_username}.py'
    UserBot = SourceFileLoader(current_user_file, os.path.join(cwd, f"static/botfiles/{current_user_file}")).load_module()
    if option == "bot":
        import CGEngine as CGBot
        player2 = CGBot
    if option == "player":
        player_file_list = os.listdir(os.path.join(cwd, "static/botfiles"))
        load_rand_player = random.choice(player_file_list)

        pfile_name = load_rand_player.rsplit(".", 1)[0]
        if pfile_name == current_user_file:
            load_player(option)
        else:
            UserBot2 = SourceFileLoader(pfile_name, f"static/botfiles/{load_rand_player}").load_module()
            player2 = UserBot2
    
    run_game(UserBot, player2, game_state["board"])

#               ----READ ME PLS----
#   ROW = y, COLUMN = x. AS BOARD USES LIST NOTATION
# ==> board[y][x] == board[ROW][COLUMN]

#[0,0,0,0],


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


# Main running function in game_manager
def run_game(UserBot, Bot2, board):
    player1 = {"side": assign_side(), "operator": UserBot}
    player2 = {"side": -player1["side"], "operator": Bot2}
    player1_info = {"your_pieces": get_position(player1["side"]),
                    "your_side": player1["side"],
                    "oponent_position": get_position(player2["side"]), 
                    "board": copy.deepcopy(game_state["board"])
                    }
    player2_info = {"your_pieces": get_position(player2["side"]), 
                    "your_side": player2["side"],
                    "oponent_position": get_position(player1["side"]), 
                    "board": copy.deepcopy(game_state["board"])
                    }
    winner = None
    move_counter = 1
    init_img(game_state["board"])

    while winner is None:
    
        player1_info["board"] = copy.deepcopy(game_state["board"])
        player2_info["board"] = copy.deepcopy(game_state["board"])

        if player1["side"] == game_state["current_turn"]:
            move = player1["operator"].main(player1_info)
        elif player2["side"] == game_state["current_turn"]:
            move = player2["operator"].main(player2_info)
        else:
            pass

        move_is_legal = is_valid_move(move, game_state["current_turn"], game_state["board"])
        
        if move_is_legal:
            pass
        else:
            if player1["side"] != game_state["current_turn"]:
                winner = player1
            else:
                winner = player2

        print(move)

        board = execute(game_state["board"], move, game_state["current_turn"])
        game_state["board"] = board

        ganh_remove = ganh(game_state["current_turn"], -game_state["current_turn"], game_state["board"])
        chet_remove = chet(game_state["current_turn"], -game_state["current_turn"], game_state["board"])

        update_board(game_state["board"], ganh_remove, chet_remove)

        generate_image(game_state["board"], move_counter, move, ganh_remove, chet_remove)

        print("AFTER: \n----------")
        display()
        print("----------")
        toggle_turn()
        move_counter += 1
        winner = result()


        
        
        if winner is not None:
            print(winner)
            break
        if move_counter == 201:
            break
    

def execute(board, move, side):
    current_x = move["selected_pos"]["x"]
    current_y = move["selected_pos"]["y"]
    new_x = move["new_pos"]["x"]
    new_y = move["new_pos"]["y"]

    for row in range(len(board)):
        for column in range(len(board[0])):
            if (row,column) == (new_y, new_x):
                board[row][column] = side
            if (row,column) == (current_y, current_x):
                board[row][column] = 0

    return board


def del_all_img():
    try:
        cwd = os.getcwd() #Get current directory
        img_dir = cwd + "/static/upload_img"
        images = os.listdir(img_dir)
        for file in images:
            file_path = os.path.join(img_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print("deletion successful")
    except OSError:
        print("OS error")


def is_valid_move(move, current_side, board):
    current_x = move["selected_pos"]["x"]
    current_y = move["selected_pos"]["y"]
    new_x = move["new_pos"]["x"]
    new_y = move["new_pos"]["y"]

    #Checking if move is out of bounds
    if (current_x < 0 or current_x >= len(game_state["board"]) or
        current_y < 0 or current_y >= len(game_state["board"])
        ):
        
        return False
    
    #Checking if selected position and new position is legal
    if (board[new_y][new_x] != 0 or board[current_y][current_x] != current_side or board[current_y][current_x] == 0):
        return False

    #Checking if the piece has moved one position away (Using the Manhattan distance formula)
    if (current_y, current_x) in diag_pos:
        dx = abs(new_x-current_x)
        dy = abs(new_y-current_y)
        if  (abs(new_x - current_x) + abs(new_y - current_y) == 1) or \
            (math.sqrt(dx**2+dy**2) == math.sqrt(2)):
            return True
        
    else:
        if (abs(new_x - current_x) + abs(new_y - current_y) == 1):
            return True
        
    return False


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
    board = board

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


def result():
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


def init_img(board):
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
    img_dir = cwd + "/static/upload_img"

    image.save(f"{img_dir}/chessboard0.png", "PNG")

def generate_image(board, move_counter, move, ganh_remove, chet_remove):

    print(f"MY SHITS{chet_remove}")
    print(f"MY SHITS{ganh_remove}")
    new_x = move["new_pos"]["x"]
    new_y = move["new_pos"]["y"]
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
            if (row, column) in ganh_remove:
                draw.ellipse((x, y, x + 40, y + 40), fill=None, outline="#FFC900", width=4)
            if (row, column) in chet_remove:
                draw.ellipse((x, y, x + 40, y + 40), fill=None, outline="#FFC900", width=4)
            if board[row][column] == -1:
                draw.ellipse((x, y, x + 40, y + 40), fill="red", outline="red")
                if (row,column) == (new_y,new_x):
                    draw.ellipse((x , y , x + 40, y + 40), fill="red", outline="green", width=5)
            elif board[row][column] == 1:
                draw.ellipse((x, y, x + 40, y + 40), fill="blue", outline="blue")
                if (row,column) == (new_y,new_x):
                    draw.ellipse((x , y , x + 40, y + 40), fill="blue", outline="green", width=5)

            else:
                pass
            x = x + 100
        x = 80
        y = y + 100

    cwd = os.getcwd()
    img_dir = cwd + "/static/upload_img"

    image.save(f"{img_dir}/chessboard{move_counter}.png", "PNG")



game_state = {
            "board": board,
            "current_turn": 1
}


def activation(option, session_name):
    if option == "bot":
        load_player(option, session_name)
    if option == "player":
        load_player(option, session_name)



