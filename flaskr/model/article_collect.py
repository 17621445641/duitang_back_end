from flask import request,Response
from datetime import datetime
import json
from flaskr.common_method import db_setting, security, list_method,splicing_list
import requests

def article_collect(app):
    @app.route('/article_collect', methods=['post'])
    def article_collect():  # 文章收藏和取消收藏
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
            article_id = request.json.get('article_id')  # 文章id
            status = request.json.get('status')  # 根据status执行收藏或者不收藏
            if (article_id):  # 判断是否传了article_id字段
                sql = "select id from article where id='%s' and is_delete!=1" % (article_id)
                if (db_setting.my_db(sql)):  # 查询是否含有此文章id
                    sql2 = "select collect_status from article_collect where user_id='%s' and article_id='%s'" % (userid,article_id)#查询数据库表中是否有记录
                    if(status==0): #判断执行取消收藏
                        if (db_setting.my_db(sql2) and db_setting.my_db(sql2)[0][0] == 1):  # 查询是否用户已收藏，未有记录则插入一条收藏记录,已有记录且状态为未收藏，则进行收藏
                            update_time = datetime.utcnow()
                            sql3 = "UPDATE article_collect SET collect_status=0,update_time = '%s' WHERE user_id = '%s'and article_id='%s' " % (
                            update_time, userid,article_id)
                            db_setting.my_db(sql3)
                            return {"code": 200, "message": "取消收藏成功","success":"true"}
                        elif(db_setting.my_db(sql2) and db_setting.my_db(sql2)[0][0] == 0):
                            return {"code": 500, "message": "已取消收藏，无法再取消收藏","success":"false"}
                        else:
                            return {"code": 500, "message": "取消收藏失败,未找到记录","success":"false"}
                    elif(status==1):#判断执行收藏
                        if (db_setting.my_db(sql2) and db_setting.my_db(sql2)[0][0] == 0):
                            update_time = datetime.utcnow()
                            sql3 = "UPDATE article_collect SET collect_status=1,update_time = '%s' WHERE user_id = '%s' and article_id='%s'" % (
                                update_time, userid,article_id)
                            db_setting.my_db(sql3)
                            return {"code": 200, "message": "更新收藏成功","success":"true"}
                        elif(db_setting.my_db(sql2) and db_setting.my_db(sql2)[0][0] == 1):
                            return {"code": 500, "message": "收藏失败,已收藏","success":"false"}
                        else:
                            create_time = datetime.utcnow()
                            sql4 = "INSERT INTO article_collect (user_id, article_id, collect_status, create_time, update_time) VALUES ( '%s', '%s', '%s', '%s', '%s')" % (
                            userid, article_id, 1, create_time, create_time)
                            db_setting.my_db(sql4)
                            return {"code": 200, "message": '新增收藏成功',"success":"true"}
                    else:
                        return {"code": 500, "message": "请输入正确的状态码(0取消收藏，1收藏)","success":"false"}
                else:
                    return {"code": 500, "message": '不存在的文章',"success":"false"}
            else:
                return {"code": 500, "message": 'article_id字段不能为空',"success":"false"}

    @app.route('/collect_list', methods=['get'])
    def collect_list():  # 查询用户收藏列表
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
            sql="select  a.user_id,b.id,b.article_title,author_id,article_content,view_status,article_img,b.create_time as article_createtime,a.update_time as collect_time from article_collect as a INNER JOIN article as b on a.article_id=b.id and a.user_id='%s' and a.collect_status=1 and is_delete!=1 and article_id not in(select article_id from article_collect as a INNER JOIN article as b on a.article_id=b.id and user_id!=author_id and view_status=0 and user_id='%s')ORDER BY collect_time DESC"%(userid,userid)
            dict = {'user_id': '', 'article_id': '', 'article_title': '', 'author_id': '', 'article_content': '',
                    'view_status': '', 'article_img':'','article_create_time': '','collect_time':''}
            collect_list= list_method.list_method(sql, dict)

            user_message={
                'user_name': '', 'avatar_image_url': ''
            }
            resp = []
            like_count_list = {'like_count': '', }
            like_status_list = {'like_status': '', }
            like_count_resp = []
            like_status_resp = []
            collect_status_resp = []
            collect_status_list = {'collect_status': '', }
            for num in collect_list:
                if (num['author_id'] == ""):
                    last_list = []
                    break
                else:
                    # 查询用户头像，用户名信息
                    sql1 = "select name,avatar_image_url from user_message as c INNER JOIN(select user_id,avatar_image_url from user_avatar_image as a INNER JOIN (select MAX(create_time) as create_time from user_avatar_image GROUP BY user_id)as b on a.create_time=b.create_time)as d on c.id=d.user_id and user_id='%s'" % (
                        num['author_id'])
                    user_message_list=json.dumps(list_method.list_method(sql1,user_message)[0])
                    resp.append(user_message_list)
                    article_list=splicing_list.splicing_list(collect_list, resp)

                    # 查询文章喜欢数量
                    sql2 = "select count(*)as like_count from article_click where article_id='%s' and click_status=1" % (
                        num['article_id'])
                    change_like_count_list = list_method.list_method(sql2, like_count_list)[0]
                    like_count_resp.append(json.dumps(change_like_count_list))
                    last_count_list = splicing_list.splicing_list(article_list, like_count_resp)

                    # 查询用户是否喜欢该文章
                    sql3 = "select click_status as like_status from article_click where article_id='%s' and user_id='%s'" % (
                        num['article_id'], userid)
                    change_like_status_list = list_method.list_method(sql3, like_status_list)[0]
                    like_status_resp.append(json.dumps(change_like_status_list))
                    last_status_list = splicing_list.splicing_list(last_count_list, like_status_resp)

                    # 查询用户是否收藏该文章
                    sql4 = "select collect_status from article_collect where article_id='%s' and user_id='%s'" % (
                    num['article_id'], userid)
                    change_collect_status_list = list_method.list_method(sql4, collect_status_list)[0]
                    collect_status_resp.append(json.dumps(change_collect_status_list))
                    last_list = splicing_list.splicing_list(last_status_list, collect_status_resp)

            # last_list = splicing_list.splicing_list(collect_list, resp)
            return {"code": 200, "message": "ok", "data": last_list, "success": "true"}
            # return Response(json.dumps(collect_list,ensure_ascii=False),mimetype='application/json')