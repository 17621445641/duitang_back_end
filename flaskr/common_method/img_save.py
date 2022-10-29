import json
import random

from flask import Flask,request,Response,render_template
from werkzeug.utils import secure_filename
import os
import uuid
from flaskr.common_method import security,db_setting
from datetime import datetime
def img_save(img_data,img_category):
    allow_format = ['png', 'jpg', 'jpeg']  # 允许图片上传格式
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[-1] in allow_format
    def img_transformation(avatar_image):#图片转换
            # secure_filename方法会去掉文件名中的中文，获取文件的后缀名
            file_suffix = secure_filename(avatar_image.filename).split('.')[-1]  # 获取文件后缀，即后缀.jpg，.jpeg等
            first_name = str(uuid.uuid4())  # uuid生成唯一的名称编码
            # # 将 uuid和后缀拼接为完整的文件名
            file_name = first_name + '.' + file_suffix
            avatar_image.save(os.path.join(upload_folder, file_name))  # 保存图片到指定目录
            # print(token)
            image_fullpath = image_url + file_name#拼接完整路径用来保存数据库中
            return image_fullpath

    if(img_category==1):#头像图片
        upload_folder = './static/avatar_images/'
        image_url = 'http://127.0.0.1:8998/static/avatar_images/'
        if img_data and allowed_file(img_data.filename):
            image_fullpath=img_transformation(img_data)
            return image_fullpath
        else:
            return "图片格式有误"
    elif(img_category==2):#动态图片
        upload_folder = './static/article_img/'
        image_url = 'http://127.0.0.1:8998/static/article_img/'
        all_image_fullpath = []
        for avatar_image in img_data:
            print(avatar_image)
            if avatar_image and allowed_file(avatar_image.filename):
                image_fullpath = img_transformation(avatar_image)
                all_image_fullpath.append(image_fullpath)
            else:
                return "图片格式有误"
        return all_image_fullpath
    elif(img_category==3):#背景图片
        upload_folder = './static/background_images/'
        image_url = 'http://127.0.0.1:8998/static/background_images/'
        if img_data and allowed_file(img_data.filename):
            image_fullpath = img_transformation(img_data)
            return image_fullpath
        else:
            return "图片格式有误"
    else:
        return "暂无其他种类图片"



    # all_image_fullpath = []
    # for avatar_image in img_data:
    #     if avatar_image and allowed_file(avatar_image.filename):
    #         # secure_filename方法会去掉文件名中的中文，获取文件的后缀名
    #         file_suffix = secure_filename(avatar_image.filename).split('.')[-1]  # 获取文件后缀，即后缀.jpg，.jpeg等
    #         first_name = str(uuid.uuid4())  # uuid生成唯一的名称编码
    #         # # 将 uuid和后缀拼接为完整的文件名
    #         file_name = first_name + '.' + file_suffix
    #
    #         avatar_image.save(os.path.join(upload_folder, file_name))  # 保存图片到指定目录
    #         # print(token)
    #         image_fullpath = image_url + file_name
    #         all_image_fullpath.append(image_fullpath)
    #         return all_image_fullpath