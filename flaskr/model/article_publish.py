import random

from flask import request,Response
from datetime import datetime
from flaskr.common_method import db_setting, security,list_method,splicing_list,img_save
import json
import requests
def article_publish(app):
    @app.route('/dynamic_publish', methods=['post'])  # 发布动态
    def dynamic_add():
        token = request.headers['access_token']  # 获取header里的token
        parse_token = security.parse_token(token)  # 解析token
        if (parse_token == 1):
            return {"code": 1, "message": "token已过期", "success": "false"}
        elif (parse_token == 2):
            return {"code": 2, "message": "token认证失败", "success": "false"}
        elif (parse_token == 3):
            return {"code": 3, "message": "非法的token", "success": "false"}
        else:
            article_type = request.form['article_type']
            author_id = (parse_token['data']['userid'])
            view_status = request.form['view_status']
            article_content = request.form['article_content']
            all_avatar_image = request.files.getlist('file')
            article_img_list=img_save.img_save(all_avatar_image,2)
            if (int(article_type) == 1):
                if (view_status == "0" or view_status == "1"):
                    random_code = random.randint(100000, 999999)
                    article_date = datetime.utcnow().strftime('%Y%m%d')
                    article_id = article_date + str(random_code)
                    article_datetime = datetime.utcnow()
                    sql = "INSERT INTO `article` (`id`,  `author_id`, `article_content`,`article_img`, `view_status`, `create_time`, `update_time`,article_type) VALUES ('%s',  '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                        article_id, author_id, article_content, json.dumps((article_img_list)),view_status, article_datetime, article_datetime,article_type)
                    db_setting.my_db(sql)
                    return {"code": 200, "message": "动态发布成功", "article_id": article_id, "success": "true"}
                else:
                    return {"code": 500, "message": "view_status只能为0或1", "success": "false"}
            elif (article_type == 2):
                return {"code": 200, "message": "文章发布成功", "success": "true"}
            else:
                return {"code": 500, "message": "article_type只能为1或2", "success": "false"}

    @app.route('/dynamic_delete', methods=['post'])  # 删除动态
    def dynamic_delete():
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
            userid = (parse_token['data']['userid'])
            sql="select * from article where id='%s' and author_id='%s' "%(article_id,userid)
            if(db_setting.my_db(sql)):
                sql2="select * from article where id='%s' and author_id='%s' and is_delete!=1"%(article_id,userid)
                if(db_setting.my_db(sql2)):
                    sql3="update article set is_delete=1 where id='%s' and author_id='%s'"%(article_id,userid)
                    db_setting.my_db(sql3)
                    return {"code": 200, "message": "文章删除成功", "success": "true"}
                else:
                    return {"code": 500, "message": "文章已被删除", "success": "false"}
            else:
                return {"code": 500, "message": "不存在该文章", "success": "false"}


