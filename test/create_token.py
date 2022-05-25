import jwt
from jwt import exceptions
from datetime import datetime,timedelta
headers = {
    "typ": "JWT",
    "alg": "HS256",
}
playod = {
    # 'exp': datetime.datetime.now() + datetime.timedelta(seconds=3),  # 过期时间
    'exp': datetime.utcnow() + timedelta(seconds=60),  # 过期时间，或者minutes,days
    # 'iat': datetime.datetime.now(),  # 开始时间：可不设置
    'iat': datetime.utcnow(),  # 开始时间：可不设置
    'iss': 'lianzong',  # 签名:可不设置
    'data': {  # 内容，一般存放该用户id和开始时间
        'userid': "张三",
    }
}
key='test_key'
# token_data=jwt.encode(playod,key,algorithm='HS256',headers=headers)#headers可不写，默认会进行加密
# print(token_data)
token_data='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTM1NTA1ODIsImlhdCI6MTY1MzQ2NDE4MiwiaXNzIjoia3hwIiwiZGF0YSI6eyJ1c2VyaWQiOjF9fQ.MpFJTnNTlGA6xA1VAmi1UHlfn05-eKepxbcg0Y7GlHY'
def m():
    try:
        parse_token=jwt.decode(token_data,key,algorithms='HS256')
        print(parse_token)
        # print(jwt.get_unverified_header())
    except exceptions.ExpiredSignatureError:
        print('token已过期')
    except jwt.DecodeError:
        print("token认证失败")
    except jwt.InvalidTokenError:
        print("非法的token")
    else:
        # return parse_token
        # parse_token = jwt.decode(token_data, key, algorithms='HS256', headers=headers)
        # print(parse_token)
        print("正确解析")

m()