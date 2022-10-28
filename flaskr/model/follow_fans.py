from flask import request,Response
from datetime import datetime,timedelta
from flaskr.common_method import db_setting, security,list_method,splicing_list
import json
import random

def follow_fans(app):

    @app.route('/add_follow',methods=['post'])
    def add_follow():#用户新增关注接口
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
            be_follow = request.json.get('be_follow')  # 被关注的用户id
            follow_status=request.json.get('follow_status')  # 0不关注，1关注

            if (be_follow):  # 判断是否传了be_follow字段
                sql = "SELECT * from user_account WHERE id='%s'"% (be_follow)
                if (db_setting.my_db(sql)):  # 查询是否含有此被关注用户
                    if(str(userid)!=be_follow):
                        sql2="SELECT * from follow_history WHERE follow_user_id='%s' and be_follow_user_id='%s'" % (
                        userid, be_follow)  # 查询用户是否已关注该用户
                        # sql2 = "select click_status from article_click where user_id='%s'" % (userid)#查询数据库表中是否有记录
                        if(follow_status==0): #判断为0的时候执行取消关注
                            if (db_setting.my_db(sql2) and db_setting.my_db(sql2)[0][2] == 1):  # 查询是否用户已被关注，未有记录则插入一条关注记录,已有记录且状态为未关注，则进行关注
                                update_time = datetime.utcnow()
                                # sql3 = "UPDATE article_click SET click_status=0,update_time = '%s' WHERE user_id = '%s'" % (
                                # update_time, userid)
                                sql3 = "UPDATE `follow_history` SET   `follow_status` = 0,  `update_time` = '%s' WHERE `follow_user_id` = '%s' AND `be_follow_user_id` = '%s'" % (
                                update_time, userid, be_follow)
                                db_setting.my_db(sql3)
                                return {"code": 200, "message": "取消关注成功","success":"true"}
                            elif(db_setting.my_db(sql2) and db_setting.my_db(sql2)[0][2] == 0):
                                return {"code": 500, "message": "已取消关注，无法再取消关注","success":"false"}
                            else:
                                return {"code": 500, "message": "取消关注失败,未找到记录","success":"false"}
                        elif(follow_status==1):#判断为1的时候执行关注
                            if (db_setting.my_db(sql2) and db_setting.my_db(sql2)[0][2] == 0):
                                update_time = datetime.utcnow()
                                sql3 = "UPDATE `follow_history` SET   `follow_status` = 1,  `update_time` = '%s' WHERE `follow_user_id` = '%s' AND `be_follow_user_id` = '%s'" % (
                                update_time, userid, be_follow)
                                db_setting.my_db(sql3)
                                return {"code": 200, "message": "更新关注成功","success":"true"}
                            elif(db_setting.my_db(sql2) and db_setting.my_db(sql2)[0][2] == 1):
                                return {"code": 500, "message": "已关注，无法再关注","success":"false"}
                            else:
                                create_time = datetime.utcnow()
                                sql4 = "INSERT INTO `follow_history` (`follow_user_id`, `be_follow_user_id`, `follow_status`, `create_time`, `update_time`) VALUES ('%s', '%s', '%s', '%s', '%s')"%(userid,be_follow,1,create_time,create_time)
                                db_setting.my_db(sql4)
                                return {"code": 200, "message": '新增关注记录成功',"success":"true"}
                        else:
                            return {"code": 500, "message": "请输入正确的状态码(0取消关注，1关注)","success":"false"}
                    else:
                        return {"code": 500, "message": "不能对自己进行关注","success":"false"}
                else:
                    return {"code": 500, "message": "被关注用户不存在","success":"false"}
            else:
                return {"code": 500, "message": 'be_follow字段不能为空',"success":"false"}

    @app.route('/follow_list', methods=['get'])
    def follow_list():  # 查询用户关注列表，be_follow_user_id为关注的其他用户的is,follow_user_id为当前用户的id
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
            sql = "select * from (SELECT user_avatar_image.user_id as user_id,avatar_image_url FROM user_avatar_image INNER JOIN ( SELECT user_id,max(create_time)AS create_time  from user_avatar_image GROUP BY user_id )AS C ON user_avatar_image.user_id=C.user_id AND user_avatar_image.create_time=C.create_time) as b INNER JOIN  (select follow_user_id,be_follow_user_id,name,sex,province,city,self_description,follow_status,follow_history.update_time as follow_time from user_message INNER JOIN follow_history on account_id=be_follow_user_id and follow_user_id='%s' and follow_status=1)as a on user_id=be_follow_user_id order by follow_time  DESC" % (
                userid)
            dict = {'user_id': '', 'avatar_image_url': '', 'follow_user_id':'','be_follow_user_id':'', 'name': '', 'sex': '',
                    'province': '', 'city': '','self_description':'', 'follow_status': '', 'follow_time': ''}
            follow_list = list_method.list_method(sql, dict)
            be_follow_status_resp=[]
            for i in follow_list:
                if(i['user_id']==""):
                    return {"code": 200, "message": "ok", "data": [], "success": "true"}
                    break
                else:
                    be_follow_user_id = i['follow_user_id']
                    follow_user_id=i['user_id']
                    sql1 = "select follow_status from follow_history where follow_user_id='%s' and be_follow_user_id='%s' and follow_status=1" % (
                    follow_user_id, be_follow_user_id)
                    dict1 = {'be_follow_status': ''}
                    be_follow_status_list = list_method.list_method(sql1, dict1)[0]
                    be_follow_status_resp.append(json.dumps(be_follow_status_list))
                    last_follow_list = splicing_list.splicing_list(follow_list, be_follow_status_resp)
            return {"code": 200, "message": "ok", "data": last_follow_list, "success": "true"}
            # return Response(json.dumps(follow_list, ensure_ascii=False), mimetype='application/json')

    @app.route('/fans_list', methods=['get'])
    def fans_list():  # 查询用户粉丝列表，be_follow_user_id为当前用户id,follow_user_id为关注当前用户的用户id
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
            sql = "select * from (SELECT user_avatar_image.user_id as user_id,avatar_image_url FROM user_avatar_image INNER JOIN ( SELECT user_id,max(create_time)AS create_time  from user_avatar_image GROUP BY user_id )AS C ON user_avatar_image.user_id=C.user_id AND user_avatar_image.create_time=C.create_time) as b INNER JOIN  (select follow_user_id,be_follow_user_id,name,sex,province,city,follow_status,follow_history.update_time as follow_time from user_message INNER JOIN follow_history on account_id=follow_user_id and be_follow_user_id='%s' and follow_status=1)as a on user_id=follow_user_id order by follow_time DESC" % (
                userid)
            dict = {'user_id': '', 'avatar_image_url': '', 'follow_user_id':'','be_follow_user_id':'', 'name': '', 'sex': '',
                    'province': '', 'city': '', 'be_follow_status': '', 'follow_time': ''}

            fans_list = list_method.list_method(sql, dict)
            be_follow_status_resp=[]
            for i in fans_list:
                if(i['user_id']==""):
                    return {"code": 200, "message": "ok", "data": [], "success": "true"}
                    continue
                else:
                    be_follow_user_id=i['user_id']
                    sql1 = "select follow_status from follow_history where follow_user_id='%s' and be_follow_user_id='%s' and follow_status=1" % (
                    userid, be_follow_user_id)
                    dict = {'follow_status': ''}
                    be_follow_status_list=list_method.list_method(sql1, dict)[0]
                    be_follow_status_resp.append(json.dumps(be_follow_status_list))
                    last_fans_list=splicing_list.splicing_list(fans_list, be_follow_status_resp)
            return {"code": 200, "message": "ok", "data": last_fans_list, "success": "true"}
            # return Response(json.dumps(fans_list, ensure_ascii=False), mimetype='application/json')

    @app.route('/is_follow', methods=['get'])#查询用户是否已关注
    def is_follow():
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
            be_follow=request.values.get('be_follow')
            sql="select follow_status from follow_history where follow_user_id='%s' and be_follow_user_id='%s' and follow_status=1"%(userid,be_follow)
            dict={'follow_status':''}
            list_method.list_method(sql,dict)
            return {"code": 200, "message": "ok", "data": list_method.list_method(sql,dict), "success": "true"}
    @app.route('/recommend_user', methods=['get'])#获取推荐关注列表
    def recommend_user():
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

            sql="select id,name,sex,province,city,self_description from user_message where id not in(SELECT be_follow_user_id FROM follow_history where follow_user_id='%s' and follow_status=1 )and id!='%s'"%(userid,userid)
            data_length = len(db_setting.my_db(sql))
            if(data_length==0):
                return {"code": 200, "message": "ok", "data": [], "success": "true"}
            else:
                global num
                global sql2
                if(data_length>5):
                    num = random.randint(0, data_length - 5)
                    sql2 = "select id,name,sex,province,city,self_description,avatar_image_url,follow_status from (select id,name,sex,province,city,self_description,avatar_image_url from(select id,name,sex,province,city,self_description from user_message where id not in(SELECT be_follow_user_id FROM follow_history where follow_user_id='%s' and follow_status=1 )and id!='%s' LIMIT %s,5 ) as c left JOIN (select user_id,avatar_image_url from user_avatar_image as a INNER JOIN (select MAX(create_time) as create_time from user_avatar_image GROUP BY user_id)as b on a.create_time=b.create_time)as d on  c.id=d.user_id)f left join (SELECT be_follow_user_id,follow_status FROM follow_history where follow_user_id='%s' and follow_status=0 ) as g on f.id=g.be_follow_user_id" % (
                    userid, userid, num, userid)
                else:
                    sql2 = "select id,name,sex,province,city,self_description,avatar_image_url,follow_status from (select id,name,sex,province,city,self_description,avatar_image_url from(select id,name,sex,province,city,self_description from user_message where id not in(SELECT be_follow_user_id FROM follow_history where follow_user_id='%s' and follow_status=1 )and id!='%s' LIMIT 0,%s ) as c left JOIN (select user_id,avatar_image_url from user_avatar_image as a INNER JOIN (select MAX(create_time) as create_time from user_avatar_image GROUP BY user_id)as b on a.create_time=b.create_time)as d on  c.id=d.user_id)f left join (SELECT be_follow_user_id,follow_status FROM follow_history where follow_user_id='%s' and follow_status=0 ) as g on f.id=g.be_follow_user_id" % (
                        userid, userid, data_length, userid)
                dict = {'id': '','name':'','sex':'','province':'','city':'','self_description':'','avatar_image_url':'','follow_status':''}
                recommend_userlist=list_method.list_method(sql2,dict)
                return {"code": 200, "message": "ok", "data": recommend_userlist, "success": "true"}