from flaskr.common_method import db_setting
from datetime import datetime,date
def list_method(sql,dict):
    sql_data= db_setting.my_db(sql)
    # print(len(sql_data))
    final_list = []
    if(len(sql_data)!=0):
        for i in sql_data:
            key_list = list(dict.keys())#把字典的key值存list列表中
            index=0
            for j in i:
                if(index<len(dict)):#根据传入的字典长度来赋值
                    if (isinstance(j, datetime)):#判断日期类型则进行转换
                        dict[key_list[index]] = j.strftime('%Y-%m-%d %H:%M:%S')
                        index = index + 1
                    elif(isinstance(j,date)):
                        dict[key_list[index]] = j.strftime('%Y-%m-%d')
                        index = index + 1
                    else:
                        dict[key_list[index]] = j#把元组的数据赋值给字典
                        index=index+1
            copy_dict=dict.copy()
            final_list.append(copy_dict)#多个字典合并成一个字典列表,通过copy实现深拷贝
        return final_list
    else:
        final_list.append(dict)
        return final_list