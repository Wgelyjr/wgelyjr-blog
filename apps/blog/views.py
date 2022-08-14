import sqlalchemy.exc
from flask import Blueprint, render_template, request, flash, session, redirect
from database.database import *
import hashlib
from apps.blog.models import *

blog = Blueprint('blog', __name__, template_folder="templates")

salt = 'Sally sells seashells by the seashore!'.encode(encoding='UTF-8', errors='strict')


@blog.route('/')
def home():
    posts = db.session.query(Posts).order_by(Posts.id.desc())
    return render_template('home.html', posts=posts)


@blog.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            userobj = User.query.filter_by(name=username).one()
        except sqlalchemy.exc.NoResultFound:
            flash('incorrect username or password. Please try again.')
            return render_template('login.html')
        passwordhash = hashlib.md5(password.encode(encoding='UTF-8', errors='strict') + salt).digest()
        if passwordhash == userobj.password:
            session['logged_in'] = True
            session['userid'] = userobj.id
            flash('Log-in successful.')
            return redirect('/')
        else:
            flash('incorrect username or password. Please try again.')
            return render_template('login.html')

    if request.method == 'GET':
        return render_template('login.html')


@blog.route('/newuser', methods=['GET', 'POST'])
def newuser():
    if 'logged_in' not in session:
        flash('Only admins can create users.')
        return redirect('/')
    if request.method == 'GET':
        return render_template('newuser.html')
    if request.method == 'POST':
        password = request.form['password']
        username = request.form['username']
        email = request.form['email']
        password_hash = hashlib.md5(password.encode(encoding='UTF-8', errors='strict') + salt)
        newuser = User(name=username, email=email, password=password_hash.digest())
        db.session.add(newuser)
        db.session.commit()
        flash(f'User "{username}" created!')
        session['logged_in'] = True
        return render_template('base.html')


@blog.route('/newpost', methods=['GET', 'POST'])
def newpost():
    if 'logged_in' not in session:
        flash('Only admins can create a new post.')
        return redirect('/')
    if request.method == 'GET':
        return render_template('newpost.html')
    if request.method == 'POST':
        newpost = Posts(
            title=request.form['title'],
            body=request.form['postbody'],
            author=session['userid']
        )
        db.session.add(newpost)
        db.session.commit()
        flash('Post Added Successfully!')
        return redirect('/')


@blog.route('/posts/<id>')
def showpost(id):
    post = Posts.query.filter_by(id=id).one()
    comments = Comments.query.filter_by(postid=id)
    return render_template('post.html', post=post, comments=comments)


@blog.route('/editpost/<id>', methods=['GET', 'POST'])
def editpost(id):
    if 'logged_in' not in session:
        flash('Only admins can edit posts.')
        return redirect(f'/posts/{id}')
    if request.method == 'GET':
        post = Posts.query.filter_by(id=id).one()
        return render_template('editpost.html', post=post)
    if request.method == 'POST':
        newtitle = request.form['title']
        newbody = request.form['postbody']
        post = Posts.query.filter_by(id=id).one()
        post.title = newtitle
        post.body = newbody
        db.session.commit()
        flash(f'Post {id} has been updated.')
        return redirect(f'/posts/{id}')


@blog.route('/deletepost/<id>', methods=['GET'])
def deletepost(id):
    if 'logged_in' not in session:
        flash('Only admins can edit posts.')
        return redirect(f'/posts/{id}')
    post = Posts.query.filter_by(id=id).one()
    db.session.delete(post)
    db.session.commit()
    flash(f'Post {id} deleted.')
    return redirect('/')


@blog.route('/newcomment/<postid>', methods=['GET', 'POST'])
def newcomment(postid):
    if request.method == 'GET':
        post = Posts.query.filter_by(id=postid).one()
        return render_template('newcomment.html', post=post)
    if request.method == 'POST':
        if 'userid' in session:
            authorid = session['userid']
        else:
            authorid = None
        newcomment = Comments(postid=postid, author=authorid, body=request.form['commentbody'])
        db.session.add(newcomment)
        db.session.commit()
        flash('Comment posted!')
        return redirect(f'/posts/{postid}')

@blog.route('/about')
def about():
    return render_template('about.html')


@blog.context_processor
def inject_data():
    postindex = db.session.query(Posts).order_by(Posts.id.desc())
    return dict(postindex=postindex)


@blog.app_errorhandler(404)
def page_not_found(e):
    flash('404: Page not found.')
    return redirect('/')
