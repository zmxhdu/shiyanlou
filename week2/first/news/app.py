from flask import Flask, render_template
import json, os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['TEMPLATE_AUTO_RELOAD'] = True
app.config['SQLALCHMNY_DATABASE_URI'] = 'mysql://root@localhost/shiyanlou'
db = SQLAlchemy(app)

jsonpath = '/home/shiyanlou/files'
jsonfilenames = os.listdir(jsonpath)


def jsonfile(jsonfilename):
    with open(os.path.join(jsonpath, jsonfilename), 'r') as jsonfile:
        jsonfilecontent = json.loads(jsonfile.read())
    return jsonfilecontent


@app.route('/')
def index():
    titles = []
    for jsonfilename in jsonfilenames:
        title = jsonfile(jsonfilename)['title']
        titles.append(title)
    
    files = {
        'titles': titles
    }

    return render_template('index.html', files=files)


@app.route('/files/<filename>')
def file(filename):
    jsonfilename = filename+'.json'
    if jsonfilename in jsonfilenames:
        title = jsonfile(jsonfilename)['title']
        created_time = jsonfile(jsonfilename)['created_time']
        content = jsonfile(jsonfilename)['content']

        files = {
            'title': title,
            'time': created_time,
            'content': content
        }
        return render_template('file.html', files=files)
    else:
        return not_found(404)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = 3000, debug = True)
