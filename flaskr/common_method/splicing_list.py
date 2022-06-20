def splicing_list(list1,list2):
    index=0
    # print(list2)
    for i in list1:
        if(index+1<=len(list2)):
            # print(index)
            i.update(eval(list2[index]))
            # print(i)
            index=index+1
    # print(list1)
    return list1