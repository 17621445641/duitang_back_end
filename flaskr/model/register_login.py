from flask import request
from datetime import datetime,timedelta
from flaskr.common_method import db_setting, security
import random

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
                return {"code": 200, "message": '登录成功','access_token':token,"success":"true"}
            else:
                return {"code": '0006', "message": '账户或密码错误',"success":"false"}
        else:
            return {"code": '0001', "message": '账户未注册',"success":"false"}

    @app.route('/register', methods=['post'])
    def register(): # 注册接口
        account = request.json.get('account')
        pwd = request.json.get('password')
        sec_pwd=request.json.get('Confirm_password')
        sql = "SELECT * from user_account where account='%s' " % (account)  # 查询用户是否已注册
        if(len(db_setting.my_db(sql))!=0):#判断用户是否已注册
            return {"code": '0005', "message": '账户已注册',"success":"false"}
        else:
            if(pwd==sec_pwd):
                create_time=datetime.utcnow()
                sql1="INSERT into user_account(account,password,create_time,update_time) values('%s','%s','%s','%s')"% (account,pwd,create_time,create_time)
                db_setting.my_db(sql1)
                sql2="select id from user_account where account='%s'"%(account)#查询之前插入的数据的id
                account_id= db_setting.my_db(sql2)[0][0]
                sql3="INSERT into user_message(account_id,update_time) values('%s','%s')"% (account_id,create_time)
                db_setting.my_db(sql3)
                sql4="INSERT INTO `user_avatar_image` (`user_id`,create_time) VALUES ('%s','%s')"% (account_id,create_time)
                db_setting.my_db(sql4)
                return {"code": 200, "message": '注册成功',"success":"true"}
            else:
                return {"code": '0002', "message": "两次密码输入不一致","success":"false"}

    @app.route('/check_account', methods=['post'])
    def check_account():  # 检查账户是否注册
        account = request.json.get('account')
        sql = "SELECT id from user_account where account='%s' " % (account)  # 查询用户是否已注册
        if (len(db_setting.my_db(sql)) != 0):  # 判断用户是否已注册
            update_code = random.randint(100000, 999999)  # 随机生成6位模拟验证码校验
            create_time = datetime.utcnow()
            sql2 = "INSERT INTO `update_code` (`user_id`, `update_code`, `create_time`) VALUES ('%s', '%s', '%s')" % (
            db_setting.my_db(sql)[0][0], update_code, create_time)
            db_setting.my_db(sql2)
            return {"code": '200', "update_code":update_code,"message": "验证码为：" + str(update_code) + ",有效期限五分钟","success":"true"}
        else:
            return {"code": '0001', "message": "账户未注册","success":"false"}

    @app.route('/check_code', methods=['post'])
    def check_code():  # 检查验证码是否有效
        account = request.json.get('account')
        check_code=request.json.get('check_code')
        sql = "SELECT id from user_account where account='%s' " % (account)  # 查询用户是否已注册
        if (len(db_setting.my_db(sql)) != 0):  # 判断用户是否已注册
            userid=db_setting.my_db(sql)[0][0]
            sql2="SELECT * from update_code where user_id='%s' ORDER BY create_time DESC limit 1"% (userid)
            time_now = datetime.utcnow()
            code_time=db_setting.my_db(sql2)[0][2]#验证码创建时间
            update_code=db_setting.my_db(sql2)[0][1]#验证码\
            if(check_code==str(update_code)):
                if(time_now>code_time+timedelta(minutes=5)):
                    return {"code": '0004', "message": "验证码已失效","success":"false"}
                else:
                    return {"code": '200', "message": "验证码验证成功","success":"true"}
            else:
                return {"code": '0003', "message": "验证码有误","success":"false"}
        else:
            return {"code": '0001', "message": "账户未注册","success":"false"}

    @app.route('/update_pwd', methods=['post'])
    def update_pwd():  # 忘记密码/修改密码修改
        account = request.json.get('account')
        pwd = request.json.get('password')
        sec_pwd = request.json.get('Confirm_password')
        sql = "SELECT * from user_account where account='%s' " % (account)  # 查询用户是否已注册
        if (len(db_setting.my_db(sql)) != 0):  # 判断用户是否已注册
            if (pwd == sec_pwd):
                update_time=datetime.utcnow()
                sql2="UPDATE `user_account` SET  `password` = '%s', `update_time` = '%s' WHERE `id` = '%s'"%(pwd,update_time,db_setting.my_db(sql)[0][0])
                db_setting.my_db(sql2)
                return {"code": '200', "message": "修改密码成功","success":"true"}
            else:
                return {"code": '0002', "message": "两次密码不一致","success":"false"}
        else:
            return {"code": '0001', "message": "账户未注册","success":"false"}
