# 程序开始的时候， 回先阅读 __init__.py 文件这里完成初始化
import logging
from logging.handlers import SMTPHandler,RotatingFileHandler
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from config import Config


# 加入调用 flask_sqlalchemy 作为ORM（Object-relational mapping） 将对象的性质映射到数据库列中
# flask_migrate用于数据库迁移，将一个数据库的数据迁移到另一个中去

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)

# login 是视图变量名 
# 使用db 表示数据库
# 添加数据库迁移引擎 migrate 
# loginmanager 进行初始化
# routes 表示路径
# models 用于描述数据库结构 


if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME']  or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost = (app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    
    if not os.path.exists('logs'): #如果没有就创建日志文件 
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,backupCount=10)
    #大小限制为10KB，保留最后10个文件作为备份

    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    # 自定义格式 包括时间戳、日志记录级别、消息以及日志来源的源代码文件和行号。
    
    file_handler.setLevel(logging.INFO)
    # 设定到了INFO级别 按照严重程度递增的顺序，分别是DEBUG、INFO、WARNING、ERROR和CRITICAL
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')    

from app import routes,models,errors