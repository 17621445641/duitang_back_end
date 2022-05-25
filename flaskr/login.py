from flask import Flask,request
import security
import json
import db_setting
def auth(app):
    @app.route('/login',methods=['post'])
    def login():
        account=request.json.get('account')
        pwd = request.json.get('password')
        sql="SELECT * from user_account where account='%s' " % (account)#查询用户是否已注册
        if(len(db_setting.my_db(sql))!=0):#判断用户是否注册
            userid=db_setting.my_db(sql)[0][3]#查询用户id
            user_account = db_setting.my_db(sql)[0][1]  # 查询用户账户
            user_pwd = db_setting.my_db(sql)[0][2]  # 查询用户密码
            if(account==user_account and pwd==user_pwd):#判断账户和密码是否一致
                token=security.generate_token(userid)#生成token
                return token
            else:
                message = {'message': '账户或密码错误'}
                return json.dumps(message, ensure_ascii=False, indent=4)
        else:
            message = {'message':'用户暂未注册'}
            return json.dumps(message, ensure_ascii=False, indent=4)
# if __name__ == '__main__':
#     server.run(host='127.0.0.1',port=8998,debug=True)

