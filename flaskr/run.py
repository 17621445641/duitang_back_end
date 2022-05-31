from flask import Flask
from flaskr.model import article_click, article_like, article_views, register_login, user_message,upload_avatar,follow_fans
app=Flask(__name__)#创建app应用
#调用其他文件下的
register_login.auth(app)#注册和登录
user_message.usermessage(app)#查看和修改用户信息
article_click.article_click(app)#文章点赞和取消点赞
article_like.article_like(app)#文章喜欢和取消喜欢和喜欢列表
article_views.article_views(app)#文章浏览记录新增，获取文章浏览量，用户浏览记录
upload_avatar.upload_avatar(app)#用户头像上传
follow_fans.follow_fans(app)#用户关注/取消关注，查询用户关注和粉丝列表
if __name__=='__main__':
    app.run(debug=True, host='127.0.0.1', port=8998 )