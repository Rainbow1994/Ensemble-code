def get_key_value(skey, inputs):
    slist=list()
    vlist=None
    
    if (skey in inputs):
        vlist=inputs[skey]
        vlist=vlist.split(',')
        if (type(vlist)==type(slist)):
            nitem=len(vlist)
            for i in range(nitem):
                vlist[i]=vlist[i].strip()
        else:
            vlist=[vlist]

    return vlist
