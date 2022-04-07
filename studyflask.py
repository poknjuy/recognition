import os

from flask import Flask, flash, redirect, render_template, request, url_for, send_from_directory
from markupsafe import escape
from werkzeug.utils import secure_filename

import forflask
import function
import main

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'jpg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    # forflask.myuse().forrec()
    return redirect('/login/')
    

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form)
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        if username == 'name' and password == 'pass':
            return redirect('/upload/')
        else:
            return render_template('login.html' , errMessages="用户名或密码错误")
    else:
        return render_template('login.html')

@app.route('/upload/', methods = ['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('recognition', filename=filename))
    return render_template('upload.html')

@app.route('/upload/<filename>')
def uploaded(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/recognition/<filename>')
def recognition(filename):
    print(filename)
    filepath = 'D:/recognition/uploads/' + filename
    return render_template('recognition.html', ans = forflask.myuse().forrec(filepath))

@app.route('/login2/')
def login2():
    username = request.args.get('username', None)
    password = request.args.get('password', None)
    if username == 'name' and password == 'pass':
        return redirect('/')
    else:
        return '登录失败'

@app.route('/user/<username>')
def profile(username):
    return '{}\s profile'.format(escape(username))

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name = None):
    return render_template('hello.html', name = name)

@app.route('/query')
def query():
    # 获取客户端的用户代理;
    user_agent = request.user_agent
    # 获取客户端的IP地址;
    req_addr = request.remote_addr

    # 获取用户请求url地址里面key值对应的value值;
    id = request.args.get('id')
    name = request.args.get('name')

    # 查看客户端的HTTP请求方式;
    reqMethod = request.method

    # 将字符串信息返回给客户端浏览器/其他, 默认以html方式显示， 如果需要换行， 加html的标签<br/>;
    return  """
    请求的用户代理: %s  <br/>
    请求的客户端Ip： %s  <br/>
    请求的id号: %s   <br/>
    用户名: %s  <br/>
    请求方式: %s
    """ %(user_agent, req_addr, id, name, reqMethod)

with app.test_request_context('/hello', method = 'POST'):
    # print(url_for('index'))
    assert request.path == '/hello'
    assert request.method == 'POST'

