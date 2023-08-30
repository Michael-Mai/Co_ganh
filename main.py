from flask import Flask, flash, request, redirect, url_for, render_template
import subprocess
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "botfiles")
ALLOWED_EXTENSIONS = {'py'}

def allowed_file(filename):
    return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_bot():

    if 'file' not in request.files:
        flash("chưa có file đính kèm")
        return redirect(request.base_url)
    
    file = request.files['file']
    if file.filename == '':
        flash("không có file")
        return redirect(request.base_url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config[UPLOAD_FOLDER], filename))

        result = subprocess.run(['python', 'bot.py'], capture_output=True, text=True)
        return render_template('result.html', output=result.stdout)



if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)


