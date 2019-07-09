import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # 获得密钥位置 如没有设定初始位置

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    # Flask-SQLAlchemy插件从SQLALCHEMY_DATABASE_URI配置变量中获取应用的数据库的位置。 
    # 首先从环境变量获取配置变量，未获取到就使用默认值，这样做是一个好习惯。 
    # 本处，我从DATABASE_URL环境变量中获取数据库URL，
    # 如果没有定义，我将其配置为basedir变量表示的应用顶级目录下的一个名为app.db的文件路径。
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SQLALCHEMY_TRACK_MODIFICATIONS配置项用于设置数据发生变更之后是否发送信号给应用.
    # 此处不需要这项功能，因此将其设置为False。

