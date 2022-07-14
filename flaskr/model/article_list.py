import json

from flask import request
from datetime import datetime,timedelta
from flaskr.common_method import db_setting, security,list_method,splicing_list
import random
def article_list(app):
    @app.route('/article_list', methods=['get'])
    def article_list():  # 首页推荐文章列表
        user_id=request.values.get('user_id')
        search_word=request.values.get('search_word')
        # global search_word
        if(search_word=="" or search_word==None ):
            search_word="%"
        else:
            #新增搜索记录
            create_time=datetime.utcnow()
            sql2="INSERT INTO `search_history` ( `user_id`, `search_word`, `create_time`) VALUES ( '%s', '%s', '%s');"%(user_id,search_word,create_time)
            db_setting.my_db(sql2)

        #查询文章列表信息
        sql="select * from (SELECT id,article_title,author_id,name,avatar_image_url,article_content,create_time,article_img,click_count from (select article_id,count(*) as click_count from article_click where click_status=1 GROUP BY article_id) as g right JOIN(select * from (select * from article where view_status=1) as e INNER JOIN(select user_id,name,avatar_image_url from user_message as c INNER JOIN(select user_id,avatar_image_url from user_avatar_image as a INNER JOIN (select MAX(create_time) as create_time from user_avatar_image GROUP BY user_id)as b on a.create_time=b.create_time)as d on c.id=d.user_id )as f on e.author_id=f.user_id and (f.name like '%%%s%%' or e.article_content like'%%%s%%' ) )as h on g.article_id=h.id )as j LEFT JOIN (SELECT click_status,article_id from article_click where user_id='%s')as k on j.id=k.article_id ORDER BY create_time DESC"%(search_word,search_word,user_id)
        # sql2="SELECT click_status from article_click where user_id='%s'"%(user_id)
        # sql2="select id,article_title,author_id,article_content,create_time,article_img from article where view_status=1 and article_content like '%\%s%'  order by create_time DESC"%(select_content)
        dict = { 'article_id': '', 'article_title': '', 'author_id': '',"name":'',"avatar_image_url":'', 'article_content': '',
                 'article_create_time': '', "article_imglist":'','click_count':'','click_status':''}
        # dict2={'click_status':''}
        article_list=list_method.list_method(sql,dict)
        # resp = []
        # click_status_list=list_method.list_method(sql2,dict2)[0]
        # change_click_status_list=json.dumps(click_status_list)
        # resp.append(change_click_status_list)
        # last_list=splicing_list.splicing_list(article_list,resp)
        return {"code": 200, "message": "ok","data":article_list,"success":"true"}

    #热门搜索词
    @app.route('/hot_search', methods=['get'])
    def hot_search():
        #查询热门搜索词
        sql="select search_word,count(search_word) as search_count,MAX(create_time)as lately_time from search_history group by search_word ORDER BY search_count DESC LIMIT 0,10"
        tinydict={'search_word': '', 'search_count': '','lately_time':''}
        hot_search_list=list_method.list_method(sql,tinydict)
        return {"code": 200, "message": "ok", "data": hot_search_list ,"success": "true"}

