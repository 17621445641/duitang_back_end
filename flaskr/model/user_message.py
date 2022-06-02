from flask import request,Response
from datetime import datetime
from flaskr.common_method import db_setting, security,list_method
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
            sql = "SELECT user_id,name,birth_day,sex,hobby,province,city,self_description,avatar_image_url,follow_count,count(*) as fans_count,f.follow_user_id from (SELECT follow_user_id,be_follow_user_id from follow_history where be_follow_user_id='%s' and follow_status=1)as e INNER JOIN (select *,count(*)as follow_count  from (SELECT * from user_message INNER JOIN(SELECT follow_user_id,be_follow_user_id from follow_history where follow_user_id='%s' and follow_status=1)as d on  id=follow_user_id ) AS a INNER JOIN (select avatar_image_url,user_id from user_avatar_image where user_id='%s' ORDER BY create_time DESC LIMIT 1)as b where a.id=b.user_id) as f where e.be_follow_user_id=f.follow_user_id" % (userid,userid,userid)
            db_setting.my_db(sql)
            tinydict = {'user_id':"",'user_name': '', 'birthday': '', 'sex': '','hobby': '','province': '','city': '','self_description':'','avatar_image_url':'',"follow_count":"","fans_count":""}
            list_method.list_method(sql,tinydict)
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

