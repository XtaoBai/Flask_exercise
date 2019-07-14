# 程序开始的时候， 回先阅读 __init__.py 文件这里完成初始化

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# 加入调用 flask_sqlalchemy 作为ORM（Object-relational mapping） 将对象的性质映射到数据库列中
# flask_migrate用于数据库迁移，将一个数据库的数据迁移到另一个中去

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
login = LoginManager(app)
login.login_view = 'login'

# login 是视图变量名 

# 使用db 表示数据库
# 添加数据库迁移引擎 migrate 
# loginmanager 进行初始化

from app import routes, models

# routes 表示路径
# models 用于描述数据库结构 