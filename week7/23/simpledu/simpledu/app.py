# coding=utf-8
from flask import Flask, render_template
from simpledu.config import configs
from simpledu.models import db, Course, User
from flask_migrate import Migrate
from flask_login import LoginManager


def create_app(config):
    """可以根据传入的config 名称，加在不同的配置
    """
    """
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    # SQLAlchemy的初始化方式改为使用 init_app
    db.init_app(app)

    #路由函数暂时写在这里，后面会介绍使用Flask 的Blueprint实现路由的模块化
    
    @app.route('/')
    def index():
        courses = Course.query.all()
        return render_template('index.html', courses=courses)

    @app.route('/admin')
    def admin_index():
        return 'admin'
    """
    """ APP 工厂
    """
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    register_extensions(app)
    register_blueprints(app)

    return app


def register_blueprints(app):
    from .handlers import front, course, admin

    app.register_blueprint(front)
    app.register_blueprint(course)
    app.register_blueprint(admin)


def register_extensions(app):
    db.init_app(app)
    Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(id)

    login_manager.login_view = 'front.login'
