# coding = utf-8
from flask import Blueprint, render_template, request, current_app
from simpledu.models import Course
from simpledu.decorators import admin_required


admin = Blueprint('admin', __name__, url_prefix='/admin')


#注意路由和函数名的变化
@admin.route('/')
@admin_required
def index():
    return render_template('admin/index.html')


@admin.route('/course')
@admin_required
def courses():
    page = request.args.get('page', default=1, type=int)
    pagination = Course.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PRE_PAGE'],
        error_out=False
    )
    return render_template('admin/courses.html', pagination=pagination)
