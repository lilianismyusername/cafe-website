from flask import Flask,render_template,redirect,url_for,request,flash
from flask_wtf import FlaskForm
from wtforms import SubmitField,PasswordField,StringField,validators,SelectField,TextAreaField
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,login_required,logout_user,current_user,LoginManager,UserMixin
from flask_gravatar import Gravatar
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base #creat the database relationship

Base = declarative_base()
app = Flask(__name__)
app.secret_key = 'jslkdflsjkdfflsjdlkfjskjghghhhsjdkjfajk'
Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)


gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)

@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))
# -----------------------------------------------------------------------------------form
class login_form(FlaskForm):

    account = StringField(label='Account',validators=[validators.DataRequired()])
    password = PasswordField(label='Password',validators=[validators.DataRequired()])
    submit = SubmitField(label='Submit')
# ----------------------------------------------------------------------------------form add cafe
class add_cafe(FlaskForm):

    name = StringField(label="Cafe's name",validators=[validators.DataRequired()])
    location = StringField(label='Location',validators=[validators.DataRequired()])
    stars = SelectField(choices=['🌟','🌟🌟','🌟🌟🌟'],validators=[validators.DataRequired()])
    opening_hours = StringField(label="Opening hours",validators=[validators.DataRequired()])
    wifi = SelectField(label='Wifi',choices=['yes','no'])
    sockets = SelectField(label='Sockets',choices=['yes','no'])
    long_stay = SelectField(label='Long_stay', choices=['yes','no'])
    tables = SelectField(label='Tables', choices=['yes','no'])
    quiet = SelectField(label='Quiet',choices=['yes','no'])
    coffee = SelectField(label='Coffee', choices=['yes','no'])
    food = SelectField(label='Food', choices=['yes','no'])
    alcohol = SelectField(label='Alcohol', choices=['yes','no'])
    restroom = SelectField(label='Restroom', choices=['yes','no'])
    parking = SelectField(label='Parking', choices=['yes','no'])
    submit = SubmitField(label='Submit')
# -----------------------------------------------------------------------------------form comment
class comment_form(FlaskForm):

    user_name = StringField(label='User name',validators=[validators.DataRequired()])
    user_comment = TextAreaField(label='Comment',validators=[validators.DataRequired()])
    submit = SubmitField(label='Submit')
# -----------------------------------------------------------------------------------database
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class users(db.Model,UserMixin):
    __tablename__ = 'all_users'
    id = db.Column(db.Integer,primary_key = True)
    user = db.Column(db.String(1000),nullable=False)
    pwd = db.Column(db.String(1000),nullable = False)
    posts = relationship('post',back_populates='user_post')
    comments = relationship('comment',back_populates= 'user')
# ----------------------------------------------------------------------------------database post
class post(db.Model):
    __tablename__ = 'all_posts'
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('all_users.id'))
    name = db.Column(db.String(1000),nullable=True)
    location = db.Column(db.String(1000),nullable=True)
    stars = db.Column(db.String(1000))
    opening_hours = db.Column(db.String(1000),nullable=True)
    wifi = db.Column(db.String)
    sockets = db.Column(db.String)
    long_stay = db.Column(db.String)
    tables = db.Column(db.String)
    quiet = db.Column(db.String)
    coffee = db.Column(db.String)
    food = db.Column(db.String)
    alcohol = db.Column(db.String)
    restroom = db.Column(db.String)
    parking = db.Column(db.String)
    posts_count = db.Column(db.Integer)

    user_post = relationship('users',back_populates='posts')
    comment_post = relationship('comment',back_populates='blog')
# ----------------------------------------------------------------------------------database comment
class comment(db.Model):
    __tablename__ = 'all_comments'
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('all_users.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('all_posts.id'))
    user_name = db.Column(db.String(1000),nullable=True)
    comment = db.Column(db.String(1000),nullable=True)
    user = relationship('users',back_populates='comments')
    blog = relationship('post',back_populates='comment_post')

# db.create_all()
# db.session.commit()
pressed_btn = []
@app.route('/',methods=['POST','GET'])
def home():

    if request.method == 'POST':
        if request.form.get('rechoose') == 'yes':
            pressed_btn.clear()
            posts = reversed(post.query.order_by(post.stars).all())
            for a in db.session.query(post).all():
                a.posts_count = 0
                db.session.commit()

        elif request.form.get(list(request.values.keys())[0])== 'yes':

            if list(request.values.keys())[0] not in pressed_btn:
                pressed_btn.append(list(request.values.keys())[0])

                if list(request.values.keys())[0] == 'wifi':
                    items1 = post.query.filter_by(wifi='yes').all()
                    for a in items1:
                        if not(a.posts_count):
                            a.posts_count = 0

                        a.posts_count += 1

                        db.session.commit()

                elif list(request.values.keys())[0] == 'sockets':
                    items1 = post.query.filter_by(sockets='yes').all()
                    for a in items1:
                        if not(a.posts_count):
                            a.posts_count = 0
                        a.posts_count += 1

                        db.session.commit()

                elif list(request.values.keys())[0] == 'tables':
                    items1 = post.query.filter_by(tables='yes').all()
                    for a in items1:
                        if not(a.posts_count):
                            a.posts_count = 0
                        a.posts_count += 1

                        db.session.commit()

                elif list(request.values.keys())[0] == 'food':
                    items1 = post.query.filter_by(food='yes').all()
                    for a in items1:
                        if not(a.posts_count):
                            a.posts_count = 0
                        a.posts_count += 1

                        db.session.commit()

                elif list(request.values.keys())[0] == 'long_stay':
                    items1 = post.query.filter_by(long_stay='yes').all()
                    for a in items1:
                        if not(a.posts_count):
                            a.posts_count = 0
                        a.posts_count += 1

                        db.session.commit()

                elif list(request.values.keys())[0] == 'quiet':
                    items1 = post.query.filter_by(quiet='yes').all()
                    for a in items1:
                        if not(a.posts_count):
                            a.posts_count = 0
                        a.posts_count += 1

                        db.session.commit()

                elif list(request.values.keys())[0] == 'coffee':
                    items1 = post.query.filter_by(coffee='yes').all()
                    for a in items1:
                        if not(a.posts_count):
                            a.posts_count = 0
                        a.posts_count += 1

                        db.session.commit()

                elif list(request.values.keys())[0] == 'alcohol':
                    items1 = post.query.filter_by(alcohol='yes').all()
                    for a in items1:

                        if not(a.posts_count):
                            a.posts_count = 0
                        a.posts_count += 1

                        db.session.commit()

                elif list(request.values.keys())[0] == 'restroom':
                    items1 = post.query.filter_by(restroom='yes').all()
                    for a in items1:

                        if not(a.posts_count):
                            a.posts_count = 0
                        a.posts_count += 1

                        db.session.commit()

                elif list(request.values.keys())[0] == 'parking':
                    items1 = post.query.filter_by(parking='yes').all()
                    for a in items1:

                        if not(a.posts_count):
                            a.posts_count = 0
                        a.posts_count += 1

                        db.session.commit()

            posts = reversed(post.query.order_by(post.posts_count,post.stars).all())

    else:
        posts = reversed(post.query.order_by(post.stars).all())

    return render_template('index.html',user=current_user.is_authenticated,cafes=posts,pressed_btn = pressed_btn)

@app.route('/login or register',methods=['POST','GET'])
def login():
    global  key_w
    form = login_form()
    if request.args.get('key') == 'log_in':
        key_w = 'Log in'
    elif request.args.get('key') == 'register':
        key_w = 'Register'

    if form.validate_on_submit():

        if request.args.get('key') == 'register':

            if users.query.filter_by(user = form.data.get('account')).first():
                flash('this email already exists.')
                return redirect(url_for('login',key='log_in'))

            new_user = users(user = form.data.get('account'), pwd=generate_password_hash(form.data.get('password'),method='pbkdf2:sha256', salt_length=8))
            db.session.add(new_user)
            db.session.commit()
            print(type(new_user))
            login_user(new_user)

            return redirect(url_for('home'))


        elif request.args.get('key') == 'log_in':

            if users.query.filter_by(user = form.data.get('account')).first():

                if check_password_hash(users.query.filter_by(user = form.data.get('account')).first().pwd,form.data.get('password')):
                    user = users.query.filter_by(user = form.data.get('account')).first()
                    login_user(user)
                    return redirect(url_for('home'))

                else:
                    flash('the password is wrong.')
                    return redirect(url_for('login',key= 'log_in'))
            else:
                flash("account doesn't exist.")
                return redirect(url_for('login',key='register'))

    return render_template('login.html',form=form,key = key_w)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/add',methods=['POST','GET'])
@login_required
def add():
    form = add_cafe()

    if form.validate_on_submit() and current_user.is_authenticated:
        new_post= post(name=form.data.get('name'),
             location=form.data.get('location'),
             stars = form.data.get('stars'),
             opening_hours = form.data.get('opening_hours'),
             wifi=form.data.get('wifi'),
             sockets=form.data.get('sockets'),
             long_stay=form.data.get('long_stay'),
             tables=form.data.get('tables'),
             quiet=form.data.get('quiet'),
             coffee=form.data.get('coffee'),
             food=form.data.get('food'),
             alcohol=form.data.get('alcohol'),
             restroom=form.data.get('restroom'),
             parking=form.data.get('parking'),
                       user_post=current_user)

        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('home'))

    elif form.validate_on_submit():
        flash('please log in or register to add a column of cafe')
        return redirect(url_for('login',key="log_in"))

    return render_template('add.html',form=form,user=current_user.is_authenticated)


@app.route('/post/<cafe_>',methods=['POST','GET'])
def post_cafe(cafe_):
    # 沒有給他她會拿前面測到的參數
    form  = comment_form()
    comments = db.session.query(comment).all()
    # cafe_=request.args.get('cafe_')  it doesn't work!!
    if form.validate_on_submit() and current_user.is_authenticated:

        new_comment = comment(user_name=form.data.get('user_name'),comment=form.data.get('user_comment'),user=current_user,blog=post.query.get(int(cafe_)))
        db.session.add(new_comment)
        db.session.commit()
        # -----------------------------------------------給他一個參數!
        return redirect(url_for('post_cafe',cafe_=cafe_))

    elif form.validate_on_submit():
        flash("you should log in to leave a comment.")
        return redirect(url_for('login',key='log_in'))

    return render_template('post.html',cafe=post.query.get(int(cafe_)),user=current_user.is_authenticated,form=form,comments=comments)


if __name__ == '__main__':
    app.run(debug=True)