from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from .models.ModelBook import ModelBook
from .models.ModelUser import ModelUser
from .models.entities.User import User
from .models.entities.Book import Book
from .models.entities.Buyout import Buyout
from .models.ModelPurchase import ModelPurchase

from .const import *

app = Flask(__name__)

csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)


@login_manager_app.user_loader
def load_user(id_u):
    return ModelUser.get_id(db, id_u)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(None, request.form['user'], request.form['password'], None)
        logged_user = ModelUser.login(db, user)
        if logged_user is not None:
            login_user(logged_user)
            flash(WELCOME, 'success')
            return redirect(url_for('index'))
        else:
            flash(LOGIN_INVALID, 'warning')
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


@app.route('/logout')
def logout():
    logout_user()
    flash(LOGOUT, 'success')
    return redirect(url_for('login'))


@app.route('/')
@login_required
def index():
    if current_user.is_authenticated:
        if current_user.usertype.id == 1:
            books_sold = []
            data = {
                'title': 'Books sold',
                'books_sold': books_sold
            }
        else:
            purchases = ModelPurchase.list_user_purchase(db, current_user)
            data = {
                'title': 'My purchases',
                'purchases': purchases
            }
        return render_template('index.html', data=data)
    else:
        return redirect(url_for('login'))


@app.route('/books')
@login_required
def list_books():
    try:
        books = ModelBook.list_books(db)
        data = {
            'title': 'List of books',
            'books': books
        }
        return render_template('list_books.html', data=data)
    except Exception as ex:
        return render_template('errors/error.html', message=format(ex))


@app.route('/buyBook', methods=['POST'])
@login_required
def buy_book():
    data_request = request.get_json()
    data = {}
    try:
        book = Book(data_request['isbn'], None, None, None, None)
        purchase = Buyout(None, book, current_user)
        data['success'] = ModelPurchase.register_purchase(db, purchase)
    except Exception as ex:
        data['message'] = format(ex)
        data['success'] = False
    return jsonify(data)


def page_not_found(error):
    return render_template('errors/404.html'), 404


def page_not_authorized(error):
    return redirect(url_for('login'))


def initialize_app(config):
    app.config.from_object(config)
    csrf.init_app(app)
    app.register_error_handler(401, page_not_authorized)
    app.register_error_handler(404, page_not_found)
    return app
