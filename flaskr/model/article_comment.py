from flask import request
import json
from datetime import datetime,timedelta
from flaskr.common_method import db_setting, security,list_method,splicing_list
import random
def article_comment(app):
    @app.route('/get_comment', methods=['get'])
    def get_comment():  # 查询文章评论
        article_id = request.values.get('article_id')
        user_id = request.values.get('user_id')
        # 查询一级评论
        sql="select comment_id,article_id,e.user_id,name,avatar_image_url,reply_id,reply_user,comment,level,create_time from(select * from article_comment where article_id='%s' and level=0 )as e  LEFT JOIN (select name,avatar_image_url,user_id from user_message as c INNER JOIN(select user_id,avatar_image_url from user_avatar_image as a INNER JOIN (select MAX(create_time) as create_time from user_avatar_image GROUP BY user_id)as b on a.create_time=b.create_time)as d on c.id=d.user_id )as f on e.user_id=f.user_id ORDER BY create_time DESC"%(article_id)

        tinydict2_click_count = {"click_count": ''}


        if(db_setting.my_db(sql)):
            tinydict = {'comment_id': '', 'article_id': '', 'user_id': '','user_name':'', 'avatar_image_url':'','reply_id': '', 'reply_user': '',
                    'comment': '', 'level': '','create_time':''}
            comment_list1=list_method.list_method(sql,tinydict)

        else:
            comment_list1=[]
        #查询对应一级评论下的二级评论
        resp1_click_stauts=[]
        resp1_click_count = []
        for i in comment_list1:
            tinydict3_click_status = {"click_status": ''}
            comment_id = i['comment_id']
            # 查询评论点赞数量
            sql_comment_count = "select count(*)as click_count from comment_click where comment_id='%s' and click_status=1" % (
                comment_id)
            click_count = list_method.list_method(sql_comment_count, tinydict2_click_count)[0]
            change_type_click_count = json.dumps(click_count)
            resp1_click_count.append(change_type_click_count)
            comment_list1 = splicing_list.splicing_list(comment_list1, resp1_click_count)

            # 查询用户是否点赞该评论
            sql3_comment_click_status = "select click_status from comment_click where comment_id='%s' and user_id='%s' and click_status=1" % (
                comment_id, user_id)
            # print('dsfsd', tinydict3_click_status)
            click_status = list_method.list_method(sql3_comment_click_status, tinydict3_click_status)[0]

            # print("tinydict3",tinydict3_click_status)
            change_type_click_status = json.dumps(click_status)
            resp1_click_stauts.append(change_type_click_status)
            comment_list1 = splicing_list.splicing_list(comment_list1, resp1_click_stauts)
            # 查询二级评论
            sql2 = "select comment_id,article_id,e.user_id,name,avatar_image_url,reply_id,reply_user,comment,level,create_time from(select * from article_comment where article_id='%s' and level=1 and reply_id='%s')as e  LEFT JOIN (select name,avatar_image_url,user_id from user_message as c INNER JOIN(select user_id,avatar_image_url from user_avatar_image as a INNER JOIN (select MAX(create_time) as create_time from user_avatar_image GROUP BY user_id)as b on a.create_time=b.create_time)as d on c.id=d.user_id )as f on e.user_id=f.user_id ORDER BY create_time DESC" % (
            article_id,comment_id)
            tinydict2 = {'comment_id': '', 'article_id': '', 'user_id': '','user_name':'', 'avatar_image_url':'','reply_id': '', 'reply_user': '',
                    'comment': '', 'level': '','create_time':''}
            if(db_setting.my_db(sql2)):
                comment_list2 = list_method.list_method(sql2, tinydict2)
                i['data'] =comment_list2
            else:
                i['data'] = []


        resp2_click_stauts = []
        resp2_click_count = []
        for i in comment_list1:
            for j in i['data']:
                tinydict3_click_status = {"click_status": ''}
                comment_id = j['comment_id']
                # 查询评论点赞数量
                sql_comment_count = "select count(*)as click_count from comment_click where comment_id='%s' and click_status=1" % (
                    comment_id)
                click_count = list_method.list_method(sql_comment_count, tinydict2_click_count)[0]
                change_type_article_list = json.dumps(click_count)
                resp2_click_count.append(change_type_article_list)
                i['data'] = splicing_list.splicing_list(i['data'], resp2_click_count)

                # 查询用户是否点赞该评论
                sql3_comment_click_status = "select click_status from comment_click where comment_id='%s' and user_id='%s' and click_status=1" % (
                    comment_id, user_id)
                # print(i['data'])
                click_status = list_method.list_method(sql3_comment_click_status, tinydict3_click_status)[0]
                change_type_click_status = json.dumps(click_status)
                resp2_click_stauts.append(change_type_click_status)
                i['data'] = splicing_list.splicing_list(i['data'], resp2_click_stauts)
        # 查询对应二级评论下的三级级评论
        # for i in comment_list1:
        #     for j in i['data']:
        #         comment_id=j['comment_id']
        #         # 查询三级评论
        #         sql3 = "select * from article_comment where article_id='%s' and level=2 and reply_id='%s' ORDER BY create_time DESC" % (
        #             article_id,comment_id)
        #         tinydict3 = {'comment_id': '', 'article_id': '', 'user_id': '', 'reply_id': '', 'reply_user': '',
        #                      'comment': '', 'level': '', 'create_time': ''}
        #         if (db_setting.my_db(sql3)):
        #             comment_list3 = list_method.list_method(sql3, tinydict3)
        #             j['data']=comment_list3
        #         else:
        #             j['data'] = []
        return {"code": 200, "message": "ok","data":comment_list1,"success":"true"}

    @app.route('/publish_comment', methods=['post'])
    def publish_comment():  # 发布文章评论
        token = request.headers['access_token']  # 获取header里的token
        parse_token = security.parse_token(token)  # 解析token
        if (parse_token == 1):
            return {"code": 1, "message": "token已过期", "success": "false"}
        elif (parse_token == 2):
            return {"code": 2, "message": "token认证失败", "success": "false"}
        elif (parse_token == 3):
            return {"code": 3, "message": "非法的token", "success": "false"}
        else:
            article_id = request.json.get('article_id')
            reply_id = request.json.get('reply_id')
            user_id = (parse_token['data']['userid'])
            comment=request.json.get('comment')
            reply_user=request.json.get('reply_user')
            create_time = datetime.utcnow()
            global level
            if (reply_id == None):
                level=0
            else:
                level=1
            sql="INSERT INTO `article_comment` ( `article_id`, `user_id`, `reply_id`, `reply_user`, `comment`, `level`, `create_time`, `update_time`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');"%(
                article_id,user_id,reply_id,reply_user,comment,level,create_time,create_time
            )
            db_setting.my_db(sql)
            return {"code": 200, "message": "发布评论成功", "success": "true"}

    @app.route('/comment_click', methods=['post'])
    def comment_click():  # 文章评论点赞
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
            comment_id = request.json.get('comment_id')  # 评论id
            status = request.json.get('status')  # 根据status执行点赞或者取消点赞
            if (comment_id):  # 判断是否传了comment_id字段
                sql = "select comment_id from article_comment where comment_id='%s'" % (comment_id)
                if (db_setting.my_db(sql)):  # 查询是否含有此评论id
                    sql2 = "select click_status from comment_click where user_id='%s'and comment_id='%s'" % (
                    userid, comment_id)  # 查询数据库表中是否有记录
                    if (status == 0):  # 判断为0的时候执行取消点赞
                        if (db_setting.my_db(sql2) and db_setting.my_db(sql2)[0][
                            0] == 1):  # 查询是否用户已点赞，未有记录则插入一条点赞记录,已有记录且状态为未点赞，则进行点赞
                            update_time = datetime.utcnow()
                            sql3 = "UPDATE comment_click SET click_status=0,update_time = '%s' WHERE user_id = '%s' and comment_id='%s'" % (
                                update_time, userid, comment_id)
                            db_setting.my_db(sql3)
                            return {"code": 200, "message": "取消点赞成功", "success": "true"}
                        elif (db_setting.my_db(sql2) and db_setting.my_db(sql2)[0][0] == 0):
                            return {"code": 500, "message": "已取消点赞,无法再取消点赞", "success": "false"}
                        else:
                            return {"code": 500, "message": "取消点赞失败,未找到记录", "success": "false"}
                    elif (status == 1):  # 判断为1的时候执行点赞
                        if (db_setting.my_db(sql2) and db_setting.my_db(sql2)[0][0] == 0):
                            update_time = datetime.utcnow()
                            sql3 = "UPDATE comment_click SET click_status=1,update_time = '%s' WHERE user_id = '%s' and comment_id='%s'" % (
                                update_time, userid, comment_id)
                            db_setting.my_db(sql3)
                            return {"code": 200, "message": "更新点赞成功", "success": "true"}
                        elif (db_setting.my_db(sql2) and db_setting.my_db(sql2)[0][0] == 1):
                            return {"code": 500, "message": "点赞失败，已点赞", "success": "false"}
                        else:
                            create_time = datetime.utcnow()
                            sql4 = "INSERT INTO comment_click (user_id, comment_id, click_status, create_time, update_time) VALUES ( '%s', '%s', '%s', '%s', '%s')" % (
                                userid, comment_id, 1, create_time, create_time)
                            db_setting.my_db(sql4)
                            return {"code": 200, "message": "新增点赞成功", "success": "true"}
                    else:
                        return {"code": 500, "message": "请输入正确的状态码(0取消点赞，1点赞)", "success": "false"}
                else:
                    return {"code": 500, "message": "不存在的评论", "success": "false"}
            else:
                return {"code": 500, "message": 'comment_id字段不能为空', "success": "false"}




