from flask import request
from datetime import datetime,timedelta
from flaskr.common_method import db_setting, security,list_method
import random
def article_list(app):
    @app.route('/article_list', methods=['get'])
    def article_list():  # 首页推荐文章列表
        # select_content = request.json.get('select_content')
        sql="SELECT id,article_title,author_id,name,avatar_image_url,article_content,create_time,article_img,click_count from (select article_id,count(*) as click_count from article_click where click_status=1 GROUP BY article_id) as g right JOIN(select * from (select * from article where view_status=1) as e INNER JOIN(select user_id,name,avatar_image_url from user_message as c INNER JOIN(select user_id,avatar_image_url from user_avatar_image as a INNER JOIN (select MAX(create_time) as create_time from user_avatar_image GROUP BY user_id)as b on a.create_time=b.create_time)as d on c.id=d.user_id)as f on e.author_id=f.user_id )as h on g.article_id=h.id ORDER BY create_time DESC"
        # sql2="select id,article_title,author_id,article_content,create_time,article_img from article where view_status=1 and article_content like '%\%s%'  order by create_time DESC"%(select_content)
        dict = { 'article_id': '', 'article_title': '', 'author_id': '',"name":'',"avatar_image_url":'', 'article_content': '',
                 'article_create_time': '', "article_imglist":'','click_count':''
                                                                               ''
                                                                               ''
                                                                               ''}
        # article_list=db_setting.my_db(sql)
        # if(select_content!=None or select_content!=""):
        #     article_list = list_method.list_method(sql2, dict)
        # else:
        article_list=list_method.list_method(sql,dict)
        return {"code": 200, "message": "ok","data":article_list,"success":"true"}

