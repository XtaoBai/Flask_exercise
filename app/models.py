# 这里是调取数据库数据的地方
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from app import db,login
from flask_login import UserMixin
from hashlib import md5


# UserMixin 中提供了四个必须的属性/方法：
# is_authenticated 是否通过登录认证
# is_active 账户是否活跃（登录状态 是否是通过用户名 密码方式 “记住我”保持状态是非活跃的
# is_anonymous 是否匿名
# get_id() 返回用户id的方法
# 当继承UserMixin时，方法可以全部使用。

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    # 登录信息：
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index =True, unique = True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy = 'dynamic')

    # 用于个人资料处理：
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)




# 用于插入图片： 
# 有一天不想用Gravatar了可以直接重写 返回其他头像网站的URL 
    def avatar(self, size):
        digest = md5 (self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest,size)
    
# 声明多对多关系
    followed = db.relationship(
        'User', secondary = followers,
        primaryjoin = (followers.c.follower_id == id),
        secondaryjoin = (followers.c.followed_id == id),
        backref = db.backref('followers', lazy = 'dynamic'),
        lazy = 'dynamic'
    )


    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
    
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

# filter() 方法 更加偏向于底层，包含任意的过滤条件。查询结果只会是0 或 1
    def is_following(self,user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() >0

    def followed_posts(self):
        # 将关注的信息连接成一张新表
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)
            ).filter(followers.c.follower_id == self.id)
        # 读取自己信息
        own = Post.query.filter_by(user_id = self.id)
        # 连接并排序
        return followed.union(own).order_by(Post.timestamp.desc())


# 用于传递信息：
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

