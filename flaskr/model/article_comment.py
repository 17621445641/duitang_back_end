from flask import request
from datetime import datetime,timedelta
from flaskr.common_method import db_setting, security,list_method,splicing_list
import random
def article_comment(app):
    @app.route('/get_comment', methods=['get'])
    def get_comment():  # 查询文章评论
        article_id = request.values.get('article_id')
        # 查询一级评论
        sql="select * from article_comment where article_id='%s' and level=0 ORDER BY create_time DESC"%(article_id)
        if(db_setting.my_db(sql)):
            tinydict = {'comment_id': '', 'article_id': '', 'user_id': '', 'reply_id': '', 'reply_user': '',
                    'comment': '', 'level': '','create_time':''}

            comment_list1=list_method.list_method(sql,tinydict)
        else:
            comment_list1=[]
        #查询对应一级评论下的二级评论
        for i in comment_list1:
            comment_id = i['comment_id']
            # 查询二级评论
            sql2 = "select * from article_comment where article_id='%s' and level=1 and reply_id='%s' ORDER BY create_time DESC" % (
            article_id,comment_id)
            tinydict2 = {'comment_id': '', 'article_id': '', 'user_id': '', 'reply_id': '', 'reply_user': '',
                         'comment': '', 'level': '', 'create_time': ''}
            if(db_setting.my_db(sql2)):
                comment_list2 = list_method.list_method(sql2, tinydict2)
                i['data'] =comment_list2
            else:
                i['data'] = []

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
            if (reply_id == ""):
                level=0
            else:
                level=1
            sql="INSERT INTO `article_comment` ( `article_id`, `user_id`, `reply_id`, `reply_user`, `comment`, `level`, `create_time`, `update_time`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');"%(
                article_id,user_id,reply_id,reply_user,comment,level,create_time,create_time
            )
            db_setting.my_db(sql)
            return {"code": 200, "message": "发布评论成功", "success": "true"}




