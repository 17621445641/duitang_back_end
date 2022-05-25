from flask import Flask
from flaskr import register_login
from flaskr import user_message
app=Flask(__name__)#创建app应用
#调用其他文件下的
register_login.auth(app)#注册和登录
user_message.usermessage(app)#查看和修改用户信息
if __name__=='__main__':
    app.run(debug=True, host='127.0.0.1', port=8998, )