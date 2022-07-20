from flask import request,Response
from datetime import datetime
from flaskr.common_method import db_setting, security,list_method,splicing_list
import json
# server=Flask(__name__)
def usermessage(app):
    @app.route('/userinfo',methods=['get'])
    def select_userinfo():#查看用户信息
        token = request.headers['access_token']  # 获取header里的token
        parse_token= security.parse_token(token)#解析token
        if (parse_token == 1):
            return {"code": 1, "message": "token已过期", "success": "false"}
        elif (parse_token == 2):
            return {"code": 2, "message": "token认证失败", "success": "false"}
        elif (parse_token == 3):
            return {"code": 3, "message": "非法的token", "success": "false"}
        else:
            # user_id=request.values.get('user_id')
            userid=(parse_token['data']['userid'])#查询用户id
            sql = "select user_id,name,birth_day,sex,hobby,province,city,self_description,avatar_image_url from user_message INNER JOIN user_avatar_image on id=user_id WHERE user_id='%s' ORDER BY user_avatar_image.create_time DESC LIMIT 1" % (userid)
            db_setting.my_db(sql)
            #查询用户关注和粉丝数量
            sql2="select follow_count,be_follow_count as fans_count  from (select count(*) as follow_count from follow_history where follow_user_id='%s' and follow_status=1)as a,(select count(*) as be_follow_count  from follow_history where be_follow_user_id='%s' and follow_status=1)as b"%(userid,userid)
            tinydict = {'user_id':"",'user_name': '', 'birthday': '', 'sex': '','hobby': '','province': '','city': '','self_description':'','avatar_image_url':''}
            list1=list_method.list_method(sql,tinydict)
            tinydict2={"follow_count":'',"fans_count":""}
            resp=[]
            resp.append(json.dumps(list_method.list_method(sql2,tinydict2)[0]))
            user_info_list=splicing_list.splicing_list(list1,resp)
            return {"code": 200, "message": "ok", "data": user_info_list, "success": "true"}
            # return Response(json.dumps(tinydict,ensure_ascii=False),mimetype='application/json')

    @app.route('/author_info', methods=['get'])
    def select_authorinfo():  # 查看作者信息
        # user_id=request.values.get('user_id')
        author_id = request.values.get('author_id')  # 查询用户id
        sql = "select user_id,name,birth_day,sex,hobby,province,city,self_description,avatar_image_url from user_message INNER JOIN user_avatar_image on id=user_id WHERE user_id='%s' ORDER BY user_avatar_image.create_time DESC LIMIT 1" % (
            author_id)
        db_setting.my_db(sql)
        tinydict = {'user_id': "", 'user_name': '', 'birthday': '', 'sex': '', 'hobby': '', 'province': '',
                    'city': '', 'self_description': '', 'avatar_image_url': ''}
        list_method.list_method(sql, tinydict)
        return {"code": 200, "message": "ok", "data": tinydict, "success": "true"}
        # return Response(json.dumps(tinydict,ensure_ascii=False),mimetype='application/json')

    @app.route('/update_userinfo', methods=['post'])
    def update_userinfo():  # 更改用户信息
        token = request.headers['access_token']  # 获取header里的token
        parse_token = security.parse_token(token)  # 解析token
        if (parse_token == 1):
            return {"code": 1, "message": "token已过期", "success": "false"}
        elif (parse_token == 2):
            return {"code": 2, "message": "token认证失败", "success": "false"}
        elif (parse_token == 3):
            return {"code": 3, "message": "非法的token", "success": "false"}
        else:
            userid = (parse_token['data']['userid'])  # 查询用户id
            user_name = request.json.get('user_name')
            sex = request.json.get('sex')
            birthday = request.json.get('birthday')
            hobby = request.json.get('hobby')
            province = request.json.get('province')
            city = request.json.get('city')
            self_description = request.json.get('self_description')
            update_time = datetime.utcnow()
            sql = "UPDATE user_message SET `name` = '%s', `sex` = '%s', `birth_day` = '%s', `hobby` = '%s', `province` = '%s', `city` = '%s', `self_description` = '%s', `update_time` = '%s' WHERE `id` = '%s';" % (user_name,sex,birthday,hobby,province,city,self_description,update_time,userid)
            db_setting.my_db(sql)
            return {"code": 200, "message": "更改用户信息成功",  "success": "true"}
            # return '更改用户信息成功'

    @app.route('/get_avatar', methods=['get'])
    def get_avatar():  # 查看用户头像，用户名等信息
        token = request.headers['access_token']  # 获取header里的token
        parse_token = security.parse_token(token)  # 解析token
        if (parse_token == 1):
            return {"code": 1, "message": "token已过期", "success": "false"}
        elif (parse_token == 2):
            return {"code": 2, "message": "token认证失败", "success": "false"}
        elif (parse_token == 3):
            return {"code": 3, "message": "非法的token", "success": "false"}
        else:
            userid = request.values.get('user_id')
            sql = "SELECT name,avatar_image_url from user_message INNER JOIN user_avatar_image on account_id=user_id and user_id='%s' order by create_time DESC limit 1" % (
            userid)
            tinydict={'name': '', 'avatar_image_url': ''}
            list_method.list_method(sql,tinydict)
            return {"code": 200, "message": "ok", "data": tinydict, "success": "true"}

