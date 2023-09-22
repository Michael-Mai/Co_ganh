
import random

# Remember that board[y][x] is the tile at (x, y) when printing
    
def is_valid_move(move, board, my_piece):
    # Check if the piece is yours
    piece = move["selected_pos"]
    if board[piece["y"]][piece["x"]] != my_piece:
        return False
    # Check if the new position is empty
    new_pos = move["new_pos"]
    try:
        if board[new_pos["y"]][new_pos["x"]] !=  0:
            return False
        # Check if it is not moving to the same position
        if piece["x"] == new_pos["x"] and piece["y"] == new_pos["y"]:
            return False
        # Check if the new position is not more than 1 tile away
        if abs(piece["x"] - new_pos["x"]) > 1 \
                or abs(piece["y"] - new_pos["y"]) > 1:
            return False
        # Check if the new position is not out of bounds
        max_x = len(board[0]) - 1
        max_y = len(board) - 1
        min_x = 0
        min_y = 0
        if new_pos["x"] > max_x \
                or new_pos["x"] < min_x \
                or new_pos["y"] > max_y \
                or new_pos["y"] < min_y:
            return False
        # Check if there is a road to the new position
        # Piece can move 8 directions if x + y is even
        # Piece can move 4 directions if x + y is odd
        move_direction = {
            "x": new_pos["x"] - piece["x"],
            "y": new_pos["y"] - piece["y"]
        }
        valid_directions = [
            {"x": 1, "y": 0},
            {"x": 0, "y": 1},
            {"x": -1, "y": 0},
            {"x": 0, "y": -1}
        ]
        if (piece["x"] + piece["y"]) % 2 == 0:
            valid_directions.extend([
                {"x": 1, "y": 1},
                {"x": -1, "y": 1},
                {"x": -1, "y": -1},
                {"x": 1, "y": -1}
            ])
        if move_direction not in valid_directions:
            return False
        return True
    except IndexError:
        return False
    

def main(input):

    # This is the main function that will be called by the game engine
    while True:
        selected_pos = random.choice(input["your_pieces"])
        board = input["board"]
        new_pos_select = random_move(selected_pos)
        new_pos = {"x": new_pos_select["x"], "y": new_pos_select["y"]}
        move = {"selected_pos": selected_pos, "new_pos": new_pos}
        if is_valid_move(move, board, input["your_side"]):
            return move

            

# Function of the game manager
def execute_move(move, board, my_piece):
    piece = move["selected_pos"]
    new_pos = move["new_pos"]
    board[piece["y"]][piece["x"]] = 0
    board[new_pos["y"]][new_pos["x"]] = my_piece
    return board


def print_board(board):
    for i in range(len(board)):
        print(board[i])
    print()


def random_move(position):
    movement = [(0, -1), (0, 1), (1, 0), (-1, 0), (-1, 1), (1, -1), (1, 1), (-1, -1)]  #possible moves
    movement_select = random.choice(movement)  #Randomize movement
    new_pos_x = position["x"] + movement_select[1]
    new_pos_y = position["y"] + movement_select[0]
    new_pos = {"x": new_pos_x, "y": new_pos_y}
    return new_pos

