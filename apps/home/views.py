from flask import Blueprint, render_template, request, flash, session, redirect

home = Blueprint('home', __name__, template_folder="templates")


@home.route('/')
def admin_home():
    return 'this is home - append /blog, /deluge, or /admin to get somewhere. . .'