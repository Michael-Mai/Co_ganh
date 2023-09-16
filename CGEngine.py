#from flask import Flask, request, render_template
#import subprocess
#from PIL import Image, ImageDraw
#import os

import random



#@app.route('/game', methods=['POST'])
#def board_to_image():
#    pass

diag_pos = [(1,1), (1, 3), (3,1), (3,3)] 

class CGBot:
    def __init__(self, side, board):
        self.my_piece = side
        self.board = board
        self.opponent_piece = -self.my_piece
        self.empty = 0 


    def is_valid_move(self, move, board):
        # Check if the piece is yours
        piece = move["piece"]

        if board[piece["y"]][piece["x"]] != self.my_piece:
            return False

        # Check if the new position is empty
        new_pos = move["new_pos"]

        try: 
            if board[new_pos["y"]][new_pos["x"]] != self.empty:
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
        except IndexError:
            return False
        return True



    def main(self, input):
        # This is the main function that will be called by the game engine
        while True:
            selected_piece = random.choice(input["your_pieces"])
            board = input["board"]

            new_pos_select = self.random_move(selected_piece)
            new_pos = {"x": new_pos_select["x"], "y": new_pos_select["y"]}
            move = {"piece": selected_piece, "new_pos": new_pos}

            if self.is_valid_move(move, board):
                return move
            else:
                continue

                


    def execute_move(self, move, board):
        piece = move["piece"]
        new_pos = move["new_pos"]
        board[piece["y"]][piece["x"]] = self.empty
        board[new_pos["y"]][new_pos["x"]] = self.my_piece
        return board

    def print_board(board):
        for i in range(len(board)):
            print(board[i])
        print()


    def random_move(self, position):
        movement = [(0, -1), (0, 1), (1, 0), (-1, 0), (-1, 1), (1, -1), (1, 1), (-1, -1)]  #possible moves
        movement_select = random.choice(movement)  #Randomize movement
        new_pos_x = position["x"] + movement_select[1]
        new_pos_y = position["y"] + movement_select[0]
        new_pos = {"x": new_pos_x, "y": new_pos_y}
        return new_pos
    

    def get_position(self, color): #parameter color: "-1" as red and "1" as blue
        positions = []
        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                if self.board[row][column] == color:
                    positions.append({"x": column, "y": row})
        return positions
    

    def activate(self):
        
        # Test everything here
        your_pieces = self.get_position(self.my_piece)
        opponent_pieces = self.get_position(self.opponent_piece)
        board = self.board
    

        my_input = {
            "your_pieces": your_pieces,
            "opponent_pieces": opponent_pieces,
            "board": board
        }
        
        move = False

        move = self.main(my_input)

        if move:
            board = self.execute_move(move, my_input["board"])

        return board


