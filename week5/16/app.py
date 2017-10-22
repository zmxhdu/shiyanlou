# coding = utf-8

import os
import json
from flask import Flask


def create_app():
    """ 创建并初始化 Flask app

    Returns:
        app (object): Flask App 实例
    """

    app = Flask('rmon')

    # 获取 json 配置文件名称
    file = os.environ.get('RMON_CONFIG')

    # TODO 从 json_file 中读取配置项并将每一项配置写入 app.config 中
    with open(file, 'r', encoding='utf-8') as json_file:
        json_config = []
        for line in json_file:
            if line.strip().startswith(('#', '{', '}')):
                continue
            else:
                line = line.strip()
                configs = line.split(':', 1)
                for i in range(0, len(configs)):
                    configs[i] = configs[i].strip().strip('"')
                configs[0] = configs[0].upper()
                json_config.append(line)
                app.config[configs[0]] = configs[1]
        print(app.config)





    return app


create_app()