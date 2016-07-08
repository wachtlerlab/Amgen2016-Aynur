import json

def fromdict(stri, d, a, dolists):
    for k in d:
        nstr = stri+"_"+k if stri!='' else k
        if type(d[k])==dict:
            fromdict(nstr, d[k], a)
        elif type(d[k])==list:
            if dolists:
                fromlist(nstr, d[k], a)
            else: a[nstr] = "\n".join(map(str, d[k]))
        else:   a[nstr] = d[k]

def fromlist(stri, l, a):
    for i in xrange(len(l)):
        nstr = stri+"_" + str(i) if stri!='' else str(i)
        if type(l[i])==dict:
            fromdict(nstr, l[i], a)
        elif type(l[i])==list:
            fromlist(nstr, l[i], a)
        else:   a[nstr] = l[i]

def fromfile(filename, name, dolists=True):
    a = {}
    with open(filename) as f:
        d = json.load(f)
    fromdict(name, d, a, dolists)
    return a