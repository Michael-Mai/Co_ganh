from flask import Flask, request, render_template
import subprocess
from PIL import Image, ImageDraw
import os
from main import *

@app.route('/game', methods=['POST'])
def board_to_image():
    pass

board = [
    [-1, -1, -1, -1, -1],
    [-1,  0,  0,  0, -1],
    [ 1,  0,  0,  0, -1],
    [ 1,  0,  0,  0,  1],
    [ 1,  1,  1,  1,  1]
]



def move_assess(board):
    pass


def bot():
    pass

def valid_move():
    pass
