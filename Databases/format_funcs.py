def formatuserinput(x):
    # y = x.values()
    if x['tab']=="reg":
        return [x['tab'],x['username'],x['password']]
    elif x['tab']=="jud":
        return [x['tab'],x['username1'],x['password1']]
    else:
        return [x['tab'],x['username2'],x['password2']]

def formatsingininput(x):
    if x['tab']=="jud":
        return [x['username'],x['password'],x['name'],x['tab']]
    else:
        return [x['username1'],x['password1'],x['name1'],x['tab']]

def formatdatetodiff(x):
    a,b,c = x.split('/')
    temp = a+"-"+b+"-"+c
    return temp

def formatdifftodate(x):
    a,b,c = x.split('-')
    temp = a+"/"+b+"/"+c
    return temp