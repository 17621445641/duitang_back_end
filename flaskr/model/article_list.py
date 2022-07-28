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
        sql="select * from (SELECT id,article_title,author_id,name,avatar_image_url,article_content,create_time,article_img,like_count from (select article_id,count(*) as like_count from article_click where click_status=1 GROUP BY article_id) as g right JOIN(select * from (select * from article where view_status=1) as e INNER JOIN(select user_id,name,avatar_image_url from user_message as c INNER JOIN(select user_id,avatar_image_url from user_avatar_image as a INNER JOIN (select MAX(create_time) as create_time from user_avatar_image GROUP BY user_id)as b on a.create_time=b.create_time)as d on c.id=d.user_id )as f on e.author_id=f.user_id and (f.name like '%%%s%%' or e.article_content like'%%%s%%' ) )as h on g.article_id=h.id )as j LEFT JOIN (SELECT click_status,article_id from article_click where user_id='%s')as k on j.id=k.article_id ORDER BY create_time DESC"%(search_word,search_word,user_id)
        # sql2="SELECT click_status from article_click where user_id='%s'"%(user_id)
        # sql2="select id,article_title,author_id,article_content,create_time,article_img from article where view_status=1 and article_content like '%\%s%'  order by create_time DESC"%(select_content)
        dict = { 'article_id': '', 'article_title': '', 'author_id': '',"name":'',"avatar_image_url":'', 'article_content': '',
                 'article_create_time': '', "article_imglist":'','like_count':'','like_status':''}
        # dict2={'click_status':''}
        article_list=list_method.list_method(sql,dict)
        return {"code": 200, "message": "ok","data":article_list,"success":"true"}

    #热门搜索词
    @app.route('/hot_search', methods=['get'])
    def hot_search():
        #查询热门搜索词
        sql="select search_word,count(search_word) as search_count,MAX(create_time)as lately_time from search_history group by search_word ORDER BY search_count DESC LIMIT 0,10"
        tinydict={'search_word': '', 'search_count': '','lately_time':''}
        hot_search_list=list_method.list_method(sql,tinydict)
        return {"code": 200, "message": "ok", "data": hot_search_list ,"success": "true"}

    #查询发布过的动态列表
    @app.route('/my_dynamic', methods=['get'])
    def my_dynamic_list():  # 查询我发布的动态列表
        token = request.headers['access_token']  # 获取header里的token
        parse_token = security.parse_token(token)  # 解析token
        if (parse_token == 1):
            return {"code": 1, "message": "token已过期", "success": "false"}
        elif (parse_token == 2):
            return {"code": 2, "message": "token认证失败", "success": "false"}
        elif (parse_token == 3):
            return {"code": 3, "message": "非法的token", "success": "false"}
        else:
            user_id = (parse_token['data']['userid'])  # 查询用户id
            # 查询发布过的动态
            sql = "select id,article_title,author_id,article_content,view_status,article_img,article_type,create_time from article where author_id='%s' order by create_time desc" % (user_id)


            if(db_setting.my_db(sql)):
                list1 = {'article_id': '', 'article_title': '', 'author_id': '', 'article_content': '', 'view_status': '', 'article_img': '','article_type': '',
                            'create_time': ''}
                dynamic_list=list_method.list_method(sql,list1)
            else:
                dynamic_list=[]

            like_count_list={'like_count': '',}
            like_status_list = {'like_status': '', }
            like_count_resp = []
            like_status_resp = []
            collect_status_resp=[]
            collect_status_list = {'collect_status': '', }
            for i in dynamic_list:
                article_id=i['article_id']
                # 查询文章喜欢数量
                sql2 = "select count(*)as like_count from article_click where article_id='%s' and click_status=1" % (
                    article_id)
                change_like_count_list=list_method.list_method(sql2,like_count_list)[0]
                like_count_resp.append(json.dumps(change_like_count_list))
                last_count_list=splicing_list.splicing_list(dynamic_list,like_count_resp)

                # 查询用户是否喜欢该文章
                sql3 = "select click_status as like_status from article_click where article_id='%s' and user_id='%s'" % (
                article_id, user_id)
                change_like_status_list = list_method.list_method(sql3, like_status_list)[0]
                like_status_resp.append(json.dumps(change_like_status_list))
                last_status_list= splicing_list.splicing_list(last_count_list, like_status_resp)

                #查询用户是否收藏该文章
                sql4="select collect_status from article_collect where article_id='%s' and user_id='%s'"%(article_id,user_id)
                change_collect_status_list = list_method.list_method(sql4, collect_status_list)[0]
                collect_status_resp.append(json.dumps(change_collect_status_list))
                last_list = splicing_list.splicing_list(last_status_list, collect_status_resp)
            return {"code": 200, "message": "ok","data":last_list,"success":"true"}

    # 更改动态是否可见
    @app.route('/update_view_status', methods=['post'])
    def update_view_status():
        token = request.headers['access_token']  # 获取header里的token
        parse_token = security.parse_token(token)  # 解析token
        if (parse_token == 1):
            return {"code": 1, "message": "token已过期", "success": "false"}
        elif (parse_token == 2):
            return {"code": 2, "message": "token认证失败", "success": "false"}
        elif (parse_token == 3):
            return {"code": 3, "message": "非法的token", "success": "false"}
        else:
            article_id = request.json.get('article_id')  # 文章id
            view_status=request.json.get('view_status')#1为可见，0为私密不可见
            update_time=datetime.utcnow()
            sql="UPDATE `article` SET `view_status` = '%s',`update_time` = '%s' WHERE `id` = '%s';"%(view_status,update_time,article_id)
            db_setting.my_db(sql)
            return {"code": 200, "message": '更新动态状态成功', "success": "true"}


