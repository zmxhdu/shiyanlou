# coding = utf-8
from flask import Blueprint, render_template
from simpledu.models import db, User, Course


user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/<username>')
def index(username):
    user_name = db.session.query(User.username).filter_by(username=username).first()
    user_names = db.session.query(User.username).all()

    if user_name in user_names:
        id = db.session.query(User.id).filter_by(username=user_name).first()[0]
        courses = db.session.query(Course.name).filter_by(author_id=id).all()
        for i in range(0,len(courses)):
            courses[i] = courses[i][0]

        users = {
            'id' : id,
            'username' : username,
            'courses' : courses
        }
        return render_template('user.html', users=users)

    else:
        return not_found(404)

@user.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

