from flask import Flask, request, render_template
import subprocess
from PIL import Image, ImageDraw
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_bot():

    if 'file' not in request.files:
        return "chưa có file đính kèm"
    
    file = request.files['file']
    if file.filename == '':
        return "không có file"
    
    if file:
        current_path = os.getcwd()
        submit_path = os.path.join(current_path, "botfiles")
        submit_file = os.path.join(submit_path, "bot.py")
        file.save(submit_file)

        result = subprocess.run(['python', 'bot.py'], capture_output=True, text=True)

        return render_template('result.html', output=result.stdout)
    
@app.route('/game', methods=['POST'])
def board_to_image():
    pass


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)



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
