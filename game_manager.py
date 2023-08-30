from CGEngine import CGBot
from bot1 import UserBot
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
    if game_state["current_turn"] == 1:
        game_state["current_turn"] = -1
    else:
        game_state["current_turn"] = 1


# Is the main running function in game_manager
def run_game():
    global board 
    engine_side = CGBot(assign_side(), game_state["board"])
    user_side = UserBot(-engine_side.my_piece, game_state["board"])
    winner = None
    game_over()

    while True:
        if engine_side.my_piece == game_state["current_turn"]:
            engine_side.activate()
            game_state["board"] = board
        if user_side.my_piece == game_state["current_turn"]:
            board = user_side.activate()
            game_state["board"] = board

        chet_remove = chet(game_state["current_turn"], -game_state["current_turn"], game_state["board"])
        ganh_remove = ganh(game_state["current_turn"], -game_state["current_turn"], game_state["board"])

        update_board(game_state["board"], ganh_remove, chet_remove)

        display()
        toggle_turn()
        game_over()

        input("enter to continue...")

    




def ganh(piece, opp_piece, board):
    valid_remove = []
    opp_remove = []
    print(piece)
    print("ganh:\n")
    display()
    print("-----------")
    game_state["board"] = board
    chet_pair = [[(1,0), (-1, 0)], [(0,1), (0, -1)]]
    chet_pair2 = [[(1,0), (-1, 0)], [(0,1), (0, -1)], [(1,1), (-1,-1)], [(-1,1), (1,-1)]]

    pieces_pos = get_position(piece)

    #NOTE: position is saved as {"x": x, "y": y}
    for position in pieces_pos:
        print(position)
        if (position["y"], position["x"]) in diag_pos:
            # Loops through each pair and conclude the opponent piece
            for pair in chet_pair2:
                for y, x in pair:
                    new_posx = position["x"] + x
                    new_posy = position["y"] + y
                    if 0 <= new_posy < len(board) and 0 <= new_posx < len(board[0]):
                        if board[new_posy][new_posx] == opp_piece:
                            opp_remove.append((new_posy, new_posx))
                            print(opp_remove)

                # Check if we have a pair
                if len(opp_remove) < 2:
                    opp_remove = []
                    pass
                else:
                    valid_remove.extend(opp_remove)
                    opp_remove = []

        else:
            # Loops through each pair and conclude the opponent piece
            for pair in chet_pair:
                for y, x in pair:
                    new_posx = position["x"] + x
                    new_posy = position["y"] + y
                    try: 
                        if 0 <= new_posy < len(board) and 0 <= new_posx < len(board[0]):
                            if board[new_posy][new_posx] == opp_piece:
                                opp_remove.append((new_posy, new_posx))
                    except IndexError:
                        pass

                if len(opp_remove) < 2:
                    opp_remove = []
                    pass
                else:
                    print("VALID!")
                    valid_remove.extend(opp_remove)
                    opp_remove = []        


    print(valid_remove)
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

                    except IndexError:
                        pass
                if len(ally_chet) < 2:
                    ally_chet = []
                    pass
                else:
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

                    except IndexError:
                        pass

                    if len(ally_chet) < 2:
                        ally_chet = []
                        pass
                    else:
                        valid_remove.append((position["y"], position["x"]))
                        ally_chet = []
    return valid_remove


def update_board(board, ganh_remove=None, chet_remove=None):
    execute = []

    if ganh_remove:
        execute.extend(ganh_remove)
    
    if chet_remove:
        execute.extend(chet_remove)

    print(execute, "|")
    for row, column in execute:
        board[row][column] = 0

    if execute:
        return board
    else:
        pass

def game_over():
    if not get_position(1) or not get_position(-1):
        return False

    else:
        return True


# Get positions of required color
def get_position(color):
    positions = []
    for row in range(len(board)):
        for column in range(len(board[0])):
            if board[row][column] == color:
                positions.append({"x": column, "y": row})
    return positions


game_state = {
            "board": board,
            "current_turn": 1
}


if __name__ == "__main__":
    run_game()


