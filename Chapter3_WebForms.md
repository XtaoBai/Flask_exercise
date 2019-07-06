# Web 表单

在本章中，我将解决这个应用程序中仍然存在的众多遗漏之一，那就是如何通过Web表单接受用户的输入。

Web表单是所有Web应用程序中最基本的组成部分之一。 我将使用表单来为用户发表动态和登录认证提供途径。


## Flask-WTF简介

我将使用[Flask-WTF](http://packages.python.org/Flask-WTF)插件来处理本应用中的Web表单，它对[WTForms](https://wtforms.readthedocs.io/)进行了浅层次的封装以便和Flask完美结合。这是本应用引入的第一个Flask插件，但绝不是最后一个。插件是Flask生态中的举足轻重的一部分，Flask故意设计为只包含核心功能以保持代码的整洁，并暴露接口以对接解决不同问题的插件。

Flask插件都是常规的Python三方包，可以使用`pip`安装。 那就继续在你的虚拟环境中安装Flask-WTF吧：
```
(venv) $ pip install flask-wtf

```
## 配置

可以界定什么样的配置变量列表到框架中。

可以用几种途径来设置。最基本的解决方案是使用`app.config`对象，它是一个类似字典的对象，可以将配置以键值的方式存储其中。例如，你可以这样做：
```
app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
# ... add more variables here as needed
```
但这样就将配置与应用代码处于同一个部分。

使用类来存储配置变量，才是我真正的风格。我会将这个配置类存储到单独的Python模块，以保持良好的组织结构。下面就让你见识一下这个存储在顶级目录下，名为*config.py*的模块的配置类吧：
```
import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
```

 配置设置被定义为`Config`类中的属性。 一旦应用程序需要更多配置选项，直接依样画葫芦，附加到这个类上即可，稍后如果我发现需要多个配置集，则可以创建它的子类。现在则不用操心。


`SECRET_KEY`是我添加的唯一配置选项，对大多数Flask应用来说，它都是极其重要的。Flask及其一些扩展使用密钥的值作为加密密钥，用于生成签名或令牌。Flask-WTF插件使用它来保护网页表单免受名为[Cross-Site Request Forgery](http://en.wikipedia.org/wiki/Cross-site_request_forgery)或CSRF（发音为“seasurf”）的恶意攻击。顾名思义，密钥应该是隐密的，因为由它产生的令牌和签名的加密强度保证，取决于除了可信维护者之外，没有任何人能够获得它。

密钥被定义成由`or`运算符连接两个项的表达式。第一个项查找环境变量`SECRET_KEY`的值，第二个项是一个硬编码的字符串。这种首先检查环境变量中是否存在这个配置，找不到的情况下就使用硬编码字符串的配置变量的模式你将会反复看到。在开发阶段，安全性要求较低，因此可以直接使用硬编码字符串。但是，当应用部署到生产服务器上的时候，我将设置一个独一无二且难以揣摩的环境变量，这样，服务器就拥有了一个别人未知的安全密钥了。

拥有了这样一份配置文件，我还需要通知Flask读取并使用它。可以在生成Flask应用之后，利用`app.config.from_object()`方法来完成这个操作：
```
from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import routes
```

导入`Config`类的方式，乍一看可能会让人感到困惑，不过如果你注意到从`flask`包导入`Flask`类的过程，就会发现这其实是类似的操作。 显而易见，小写的“config”是Python模块*config.py*的名字，另一个含有大写“C”的是类。

正如我上面提到的，可以使用`app.config`中的字典语法来访问配置项。 在下面的Python交互式会话中，你可以看到密钥的值：
```
>>> from microblog import app
>>> app.config['SECRET_KEY']
'you-will-never-guess'
```
## 用户登录表单

Flask-WTF插件使用Python类来表示Web表单。表单类只需将表单的字段定义为类属性即可。

为了再次践行我的*松耦合*原则，我会将表单类单独存储到名为*app/forms.py*的模块中。就让我们来定义用户登录表单来做一个开始吧，它会要求用户输入username和password，并提供一个“remember me”的复选框和提交按钮：
```
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
```
这里包含一个建立表的类。


大多数Flask插件使用`flask_ <name>`命名约定来导入，Flask-WTF的所有内容都在`flask_wtf`包中。在本例中，*app/forms.py*模块的顶部从`flask_wtf`导入了名为`FlaskForm`的基类。

由于Flask-WTF插件本身不提供字段类型，因此我直接从WTForms包中导入了四个表示表单字段的类。每个字段类都接受一个描述或别名作为第一个参数，并生成一个实例来作为`LoginForm`的类属性。

你在一些字段中看到的可选参数`validators`用于验证输入字段是否符合预期。`DataRequired`验证器仅验证字段输入是否为空。更多的验证器将会在未来的表单中接触到。



## 表单模板

下一步是将表单添加到HTML模板以便渲染到网页上。 令人高兴的是在LoginForm类中定义的字段支持__自渲染__为HTML元素，所以这个任务相当简单。 我将把登录模板存储在文件*app/templates/login.html *中，代码如下：
```
{% extends "base.html" %}

{% block content %}
    <h1>Sign In</h1>
    <form action="" method="post" novalidate>
        {{ form.hidden_tag() }}
        <p>
            {{ form.username.label }}<br>
            {{ form.username(size=32) }}
        </p>
        <p>
            {{ form.password.label }}<br>
            {{ form.password(size=32) }}
        </p>
        <p>{{ form.remember_me() }} {{ form.remember_me.label }}</p>
        <p>{{ form.submit() }}</p>
    </form>
{% endblock %}
```

一如[第二章](https://github.com/luhuisicnu/The-Flask-Mega-Tutorial-zh/blob/master/docs/%E7%AC%AC%E4%BA%8C%E7%AB%A0%EF%BC%9A%E6%A8%A1%E6%9D%BF.md)，在这个模板中我再次使用了`extends`来继承`base.html`基础模板。事实上，我将会对所有的模板继承基础模板，以保持顶部导航栏风格统一。

这个模板需要一个form参数的传入到渲染模板的函数中，form来自于`LoginForm`类的实例化，不过我现在还没有编写它。

HTML`<form>`元素被用作Web表单的容器。 表单的`action`属性告诉浏览器在提交用户在表单中输入的信息时应该请求的URL。 当`action`设置为空字符串时，表单将被提交给当前地址栏中的URL，即当前页面。 `method`属性指定了将表单提交给服务器时应该使用的HTTP请求方法。 默认情况下是用`GET`请求发送，但几乎在所有情况下，使用`POST`请求会提供更好的用户体验，因为这种类型的请求可以在请求的主体中提交表单数据， `GET`请求将表单字段添加到URL，会使浏览器地址栏变得混乱。

`form.hidden_tag()`模板参数生成了一个隐藏字段，其中包含一个用于保护表单免受CSRF攻击的`token`。 对于保护表单，你需要做的所有事情就是在模板中包括这个隐藏的字段，并在Flask配置中定义`SECRET_KEY`变量，Flask-WTF会完成剩下的工作。

如果你以前编写过HTML Web表单，那么你会发现一个奇怪的现象——在此模板中没有HTML表单元素，这是因为表单的字段对象的在渲染时会自动转化为HTML元素。 我只需在需要字段标签的地方加上`{{ form.<field_name>.label }}`，需要这个字段的地方加上`{{ form.<field_name>() }}`。 对于需要附加HTML属性的字段，可以作为关键字参数传递到函数中。 此模板中的username和password字段将`size`作为参数，将其作为属性添加到`<input>` HTML元素中。 你也可以通过这种手段为表单字段设置class和id属性。

## 表单视图

完成这个表单的最后一步就是编写一个新的视图函数来渲染上面创建的模板。

函数的逻辑只需创建一个form实例，并将其传入渲染模板的函数中即可，然后用*/login* URL来关联它。这个视图函数也存储到*app/routes.py*模块中，代码如下：
```
from flask import render_template
from app import app
from app.forms import LoginForm

# ...

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)
```

我从*forms.py*导入`LoginForm`类，并生成了一个实例传入模板。`form=form`的语法看起来奇怪，这是Python函数或方法传入关键字参数的方式，左边的`form`代表在模板中引用的变量名称，右边则是传入的*form*实例。这就是获取表单字段渲染结果的所有代码了。

在基础模板*templates/base.html*的导航栏上添加登录的链接，以便访问：
```
<div>
    Microblog:
    <a href="/index">Home</a>
    <a href="/login">Login</a>
</div>
```

此时，你可以验证结果了。运行该应用，在浏览器的地址栏中输入`http://localhost:5000/`，然后点击顶部导航栏中的“Login”链接来查看新的登录表单。 是不是非常炫酷？

![登录表单](http://upload-images.jianshu.io/upload_images/4961528-6d1753699807685a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
