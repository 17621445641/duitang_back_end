from flask import request
from datetime import datetime
from flaskr.common_method import db_setting, security


def auth(app):

    @app.route('/login',methods=['post'])
    def login():#登录接口
        account=request.json.get('account')
        pwd = request.json.get('password')
        sql = "SELECT * from user_account where account='%s' " % (account)  # 查询用户是否已注册
        if(len(db_setting.my_db(sql))!=0):#判断用户是否已注册
            userid= db_setting.my_db(sql)[0][0]#查询用户id
            user_account = db_setting.my_db(sql)[0][1]  # 查询用户账户
            user_pwd = db_setting.my_db(sql)[0][2]  # 查询用户密码
            if(account==user_account and pwd==user_pwd):#判断账户和密码是否一致
                token= security.generate_token(userid)#生成token
                return token
            else:
                return '账户或密码错误'
        else:
            return '用户未注册'

    @app.route('/register', methods=['post'])
    def register(): # 注册接口
        account = request.json.get('account')
        pwd = request.json.get('password')
        sec_pwd=request.json.get('Confirm_password')
        sql = "SELECT * from user_account where account='%s' " % (account)  # 查询用户是否已注册
        if(len(db_setting.my_db(sql))!=0):#判断用户是否已注册
            return '账户已注册'
        else:
            if(pwd==sec_pwd):
                create_time=datetime.utcnow()
                sql1="INSERT into user_account(account,password,create_time) values('%s','%s','%s')"% (account,pwd,create_time)
                db_setting.my_db(sql1)
                sql2="select id from user_account where account='%s'"%(account)#查询之前插入的数据的id
                account_id= db_setting.my_db(sql2)[0][0]
                sql3="INSERT into user_message(account_id,update_time) values('%s','%s')"% (account_id,create_time)
                db_setting.my_db(sql3)
                return '注册成功'
            else:
                return  "两次密码输入不一致"