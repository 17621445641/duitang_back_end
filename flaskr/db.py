import pymysql
sql='SELECT * from user_message '
def my_db(sql):
    conn=pymysql.connect(host='127.0.0.1',user='root',password='123456',db='myproject',
                port=3306,charset='utf8',autocommit=True)
    cur=conn.cursor()
    cur.execute(sql)
    res=cur.fetchall()
    # for row in cur:
    print(res[0][1])
    cur.close()
    conn.close()
    return res
if __name__ == '__main__':
    my_db(sql)



