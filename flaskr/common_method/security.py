import jwt
from jwt import exceptions
from datetime import datetime,timedelta
key = 'test_key'
def generate_token(userid):#token生成
    playod = {
    # 'exp': datetime.datetime.now() + datetime.timedelta(seconds=3),  # 过期时间
    'exp': datetime.utcnow() + timedelta(days=7),  # 过期时间，或者minutes,days，seconds
    # 'iat': datetime.datetime.now(),  # 开始时间：可不设置
    'iat': datetime.utcnow(),  # 开始时间：可不设置
    'iss': 'kxp',  # 签名:可不设置
    'data': {  # 内容，一般存放该用户id和开始时间
        'userid': userid,
    }
}
    token_data = jwt.encode(playod, key, algorithm='HS256')
    return token_data

def parse_token(token_data):#解析token校验是否合法
    try:
        parse_token=jwt.decode(token_data,key,algorithms='HS256')
    except exceptions.ExpiredSignatureError:
        return 1#token已过期
    except jwt.DecodeError:
        return 2#token认证失败
    except jwt.InvalidTokenError:
        return 3#非法的token
    else:
        return parse_token



