import apps.admin.utils as utils
from flask import Blueprint, render_template, request, flash, session, redirect

admin = Blueprint('admin', __name__, template_folder="templates", url_prefix='/admin')


@admin.route('/')
def admin_home():
    return 'this is the admin homepage'
