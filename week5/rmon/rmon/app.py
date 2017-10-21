"""rmon.app

该模块主要实现了app创建函数
"""
import os
from flask import Flask

from rmon.views import api
from rmon.models import db
from rmon.config import DevConfig, ProductConfig


def create_app():
    """创建并初始化Flask app
    """

    app = Flask('rmon')

    #根据环境变量加在开发环境或生产环境配置
    env = os.environ.get('RMON_ENV')

    if env in ('pro', 'prod', 'product'):
        app.config.from_object(ProductConfig)
    else:
        app.config.from_object(DevConfig)

    #从环境变量RMON_SETTINGS指定的文件中加在配置
    app.config.from_envvar('RMON_SETTINGS', silent=True)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #注册Blueprint
    app.rgister_blueprint(api)
    #初始化数据库
    db.init_app(app)
    #如果是开发环境则创建所有数据库表
    if app.debug:
        with app.app_contex():
            db.create_all()
    return app
