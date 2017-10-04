from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pymongo import MongoClient

app = Flask(__name__)
app.config['TEMPLATE_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/shiyanlou'
db = SQLAlchemy(app)

client = MongoClient('127.0.0.1', 27017)
mongo_db = client.shiyanlou


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    files = db.relationship('File')

    def __init__(self, name):
        self.name = name


class File(db.Model):
    __tablename__ = 'file'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category')
    content = db.Column(db.Text)

    def __init__(self, title, created_time, category, content):
        self.title = title
        self.created_time = created_time
        self.category = category
        self.content = content

    def add_tag(self, tag_name):
        file_mongo = mongo_db.file.find_one({'file_id': self.id})
        if file_mongo:
            tag_names = file_mongo['tag_names']
            if tag_name not in tag_names:
                tag_names.append(tag_name)
            mongo_db.file.update_one({'file_id': self.id}, {'$set': {'tag_names': tag_names}})
        else:
            tag_names = [tag_name]
            mongo_db.file.insert_one({'file_id': self.id, 'tag_names': tag_names})
        return tag_names

    def remove_tag(self, tag_name):
        file_mongo = mongo_db.file.find_one({'file_id': self.id})
        if file_mongo:
            tag_names = file_mongo['tag_names']
            if tag_name in tag_names:
                tag_names = tag_names.remove(tag_name)
            else:
                return tag_names
            mongo_db.file.update_one({'file_id': self.id}, {'$set': {'tag_names': tag_names}})
        return []

    @property
    def tags(self):
        file_mongo = mongo_db.file.find_one({'file_id': self.id})
        if file_mongo:
            return file_mongo['tag_names']
        else:
            return []



def insert_datas():
    db.create_all()
    java = Category('Java')
    python = Category('Python')
    file1 = File('Hello Java', datetime.utcnow(), java, 'File Content - Java is cool!')
    file2 = File('Hello Python', datetime.utcnow(), python, 'File Content - Python is cool!')
    db.session.add(java)
    db.session.add(python)
    db.session.add(file1)
    db.session.add(file2)
    db.session.commit()
    file1.add_tag('tech')
    file1.add_tag('java')
    file1.add_tag('linux')
    file2.add_tag('tech')
    file2.add_tag('python')


insert_datas()

@app.route('/')
def index():
    files_mysql = File.query.all()
    return render_template('index.html', files=files_mysql)


@app.route('/files/<int:file_id>')
def file(file_id):
    file_id = db.session.query(File.id).filter_by(id=file_id).first()
    files_id = db.session.query(File.id).all()
    if file_id in files_id:
        title = list(db.session.query(File.title).filter_by(id=file_id).first())[0]
        content = list(db.session.query(File.content).filter_by(id=file_id).first())[0]
        created_time = list(db.session.query(File.created_time).filter_by(id=file_id).first())[0]
        name = list(db.session.query(Category.name).filter_by(id=file_id).first())[0]

        files = {
            'id': file_id,
            'title': title,
            'content': content,
            'created_time': created_time,
            'name': name
        }
        return render_template('file.html', files=files)
    else:
        return not_found(404)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000, debug=True)
