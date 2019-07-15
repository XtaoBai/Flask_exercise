from datetime import datetime
from flask import render_template,flash,redirect,url_for,request
from app import app, db
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user,login_required
from app.models import User
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User 




@app.route('/')
@app.route('/index')
@login_required # 页面保护 无法匿名访问
def index():
    user = {'username': 'Garan'}
    posts = [
        {
            'author':{'username':'John'},
            'body': 'Beautiful day in Porland!'
        },
        {
            'author':{'username':'Susan'},
            'body':'The Averangers movie was so cool!'
        }
    ]

    return render_template('index.html',title='Home Page',posts=posts)

@app.route('/login',methods=['GET','POST'])
def login():

# 处理一下非预期情况： 用户已经登录，却又导航道路 /login 地址
# current_user 变量来自Flask-Login 可以在处理过程中 调用获取对象 is_authenticated 
# 检查登录。

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

# 数据库加载数据 

    if form.validate_on_submit():
# SQLAlchemy 查询对象的 filter_by()方法；结果返回只包含具有匹配用户名对象的查询结果集合
# 因为只有有/无 这里使用 first() 来完成/此时只需要一个，没有则返回None

        user = User.query.filter_by(username=form.username.data).first()

# 没有 或 不正确
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

# 正确则调用 切换成已登录：
        login_user(user,remember=form.remember_me.data) 
        
#        flash('Login requested for user {}, remember_me = {}'.format(
#            form.username.data,form.remember_me.data))
#        return redirect(url_for('index'))
    
# 查询下一个对象 
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html',title ='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# 建立注册页面：
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# 建立个人主页：

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username = username).first_or_404()
    posts =[
        {'author':user,'body':'Test post #1'},
        {'author':user,'body':'Test post #2'}
    ]
    return render_template('user.html',user=user,posts= posts)

# <>包裹为动态的；
# 只能被已登录的用户使用所以加上 @login_required 
# first_or_404 如果有问题会返回404 给服务器
#  如果没有触发则找到用户 下面初始化渲染对象


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/edit_profile', methods =['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',form=form)


