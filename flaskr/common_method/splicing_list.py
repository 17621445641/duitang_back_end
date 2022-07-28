import json


def splicing_list(list1,list2):
    index=0
    for i in list1:
        if(index+1<=len(list2)):
            # print(type(list2[index]))
            i.update(json.loads(list2[index]))
            # i.update(eval(list2[index]))
            index=index+1
    return list1