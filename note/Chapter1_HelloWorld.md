## "Hello World" Flask 应用

项目结构图：
```
microblog/
    venv/
    app/
        __init__.py
        routes.py
    microblog.py
```

>在Python中，包含`__init__.py`文件的子目录被视为一个可导入的包。 当你导入一个包时，`__init__.py`会执行并定义这个包暴露给外界的属性。

‘app’的包负责存放整个应用，在其下创建文件`__init__.py`，输入如下的代码：
```
from flask import Flask

app = Flask(__name__)

from app import routes
```
脚本是从flask中导入的类‘Flask’，并以此创建了一个应用程序对象。传递给‘Flask’类的‘__name__’它是一个Python预定义的变量，表示当前调用它的模块的名字。Flask就使用这个位置作为起点来计算绝对路径。然后导入‘routes’模块。

这里有两个实体名为`app`。 `app`包由*app*目录和`__init__.py`脚本来定义构成，并在`from app import routes`语句中被引用。 `app`变量被定义为`__init__.py`脚本中的`Flask`类的一个实例，以至于它成为`app`包的属性。

`routes`模块是在底部导入的，而不是在脚本的顶部。 最下面的导入是解决*循环导入*的问题，这是Flask应用程序的常见问题。 你将会看到`routes`模块需要导入在这个脚本中定义的`app`变量，因此将`routes`的导入放在底部可以避免由于这两个文件之间的相互引用而导致的错误。

在`routes`模块中有些什么？ 路由是应用程序实现的不同URL。 在Flask中，应用程序路由的处理逻辑被编写为Python函数，称为*视图函数*。 视图函数被映射到一个或多个路由URL，以便Flask知道当客户端请求给定的URL时执行什么逻辑。

这是需要写入到*app/routes.py*中的第一个视图函数的代码：
```
from app import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"
```
`＠app.route`修饰器在作为参数给出的URL和函数之间创建一个关联。 在这个例子中，有两个装饰器，它们将URL `/`和`/index`索引关联到这个函数。 这意味着，当Web浏览器请求这两个URL中的任何一个时，Flask将调用该函数并将其返回值作为响应传递回浏览器。这样做是为了在运行这个应用程序的时候会稍微有一点点意义。

要完成应用程序，你需要在定义Flask应用程序实例的顶层（译者注：也就是microblog目录下）创建一个命名为*microblog.py*的Python脚本。 它仅拥有一个导入应用程序实例的行：
```
from app import app
```

从app包中调用app对象。

可以准备运行了！在运行之前，需要通过设置`FLASK_ENV`环境变量告诉Flask如何导入它：
```
(venv)> ... > set FLASK_ENV=microblog.py
```
```
(venv) $ flask run
 * Serving Flask app "microblog"
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

服务启动后将处于阻塞监听状态，将等待客户端连接。 `flask run`的输出表明服务器正在运行在IP地址127.0.0.1上，这是本机的回环IP地址。 这个地址很常见，并有一个更简单的名字，你可能已经看过：*localhost*。 网络服务器监听在指定端口号等待连接。 部署在生产Web服务器上的应用程序通常会在端口443上进行监听，如果不执行加密，则有时会监听80，但启用这些端口需要root权限。 由于此应用程序在开发环境中运行，因此Flask使用自由端口5000。 现在打开您的网络浏览器并在地址栏中输入以下URL：
```
    http://localhost:5000/
```
或者，你也可以使用另一个URL：
```
    http://localhost:5000/index
```
完成演示之后，你可以按下Ctrl-C来停止Web服务。

在结束本章节之前，我想提醒一下你，在终端会话中直接设置的环境变量不会永久生效，因此你不得不在每次新开终端时设定 `FLASK_APP` 环境变量，从 1.0 版本开始，Flask 允许你设置只会在运行`flask`命令时自动注册生效的环境变量，要实现这点，你需要安装 `python-dotenv`：
```
(venv) $ pip install python-dotenv
```

此时，在项目的根目录下新建一个名为 `.flaskenv` 的文件，其内容是：
```
FLASK_APP=microblog.py
```

通过此项设置，`FLASK_APP`就可以自动加载了，如果你钟爱手动设定环境变量，那也不错，只是记得每次启动终端后要设定它。



其中用到的cmd命令：

唤起虚拟环境:
```
> python -m venv venv 
```
>不一定成功

激活虚拟环境：
```
>set venv/bin/activate
(venv) >...>_
```
>这里指Windows

创建文件夹： 
```
>mkdir app
```
创建文件：
```
type nul>__init__.py
echo from app import app>microblog.py
```
打开文件：
```
start routes.py
```
