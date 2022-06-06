def methd(list1,list2):
    index=0
    for i in list1:
        i.update(list2[index])
        index=index+1
    return list1