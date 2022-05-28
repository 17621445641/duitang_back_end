import pymysql
account='17600000000'
sql="SELECT * from user_account where account='%s' " % (account)
sql2="INsERT into user_account(account,password) values('17600000002','123456') "
def my_db(sql2):
    conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='myproject',
                           port=3306, charset='utf8', autocommit=True)
    cur = conn.cursor()
    be = sql2.split(" ")[0]
    print(be.lower())
    if(be.lower()=='insert'):
        print('相等')
        row = cur.execute(sql2)
        if(row==1):
            res = cur.fetchall()
            cur.close()
            conn.close()
            print(row)  # 输出插入语句的影响行数
            return res
        else:
            print('数据插入失败')
            return '数据插入失败'

    else:
        print('不等')
        cur.execute(sql)
        # print(row)#输出插入语句的影响行数
        res=cur.fetchall()
        print(res)
        if(len(res)!=0):
            print(1)
        else:
            print('用户暂未注册')
        cur.close()
        conn.close()
        return res
if __name__ == '__main__':
    my_db(sql2)



