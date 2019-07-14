from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from app import db
from flask_login import UserMixin
from app import login

# UserMixin 中提供了四个必须的属性/方法：
# is_authenticated 是否通过登录认证
# is_active 账户是否活跃（登录状态 是否是通过用户名 密码方式 “记住我”保持状态是非活跃的
# is_anonymous 是否匿名
# get_id() 返回用户id的方法
# 当继承UserMixin时，方法可以全部使用。


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index =True, unique = True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy = 'dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)






