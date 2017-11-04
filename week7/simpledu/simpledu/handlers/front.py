# coding = utf-8
from flask import Blueprint, render_template
from simpledu.models import Course
from simpledu.forms import LoginForm, RegisterForm

#省略了 url_prefix, 那么默认就是'/'
front = Blueprint('front', __name__)


@front.route('/')
def index():
    courses = Course.query.all()
    return render_template('index.html', courses=courses)


@front.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


@front.route('/register')
def register():
    form = RegisterForm()
    return render_template('register.html', form=form)
