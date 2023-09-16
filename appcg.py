from flask import Flask, flash, request, redirect, url_for, render_template, session
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os

from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SECRET_KEY'] = 'pkH{XQup/)QikTx'
app.app_context().push()

#Flask Alchemy initialization
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

admin = Admin(app, name='microblog', template_mode='bootstrap3')

app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 100  #Max file size
app.config['UPLOAD_FOLDER'] = "static/botfiles"
ALLOWED_EXTENSIONS = {'py'}

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'    


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin): 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'Username'})

    password =  PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'Password'})
    
    submit = SubmitField("Đăng Nhập")


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'Username'})

    password =  PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'Password'})
    
    submit = SubmitField("Đăng ký")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError('Tên đăng nhập đã được sử dụng')


def allowed_file(filename):
    return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        session['username'] = request.form['username']
    if form.validate_on_submit():   
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('menu'))

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username= form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    session.pop('username', None)
    logout_user()
    return redirect(url_for('login'))


@app.route('/menu', methods=['GET', 'POST'])
@login_required
def menu():
    if 'username' in session:
        username_loggedin = session['username']

    return render_template('menu.html', username_loggedin=username_loggedin)


@app.route('/submit', methods=['GET' ,'POST'])
def submit_bot():
    if 'file' not in request.files:
        flash("chưa có file đính kèm")
        return redirect(url_for('/menu'))
    
    file = request.files['file']
    if file.filename == '':
        flash("không có file")
        return redirect('/menu')
    
    if file and not allowed_file(file.filename):
        flash('loại file không cho phép')
        return redirect('/menu')

    if file and allowed_file(file.filename):
        user = session['username']
        file.filename = f'botfile_{user}.py'
        filename = secure_filename(file.filename)
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], filename))

        return render_template('result.html')


@app.route('/matchreplay')
def process_match(match_file):
    pass


if __name__ == '__main__': 
    app.run(debug=True, use_reloader=False)


