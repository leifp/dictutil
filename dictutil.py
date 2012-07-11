from collections import defaultdict

## clojure
def merge(d1, d2, *ds):
    d = d1.copy()  #TODO shouldn't copy
    for k in d2:
        d[k] = d2[k]
    if ds:
        return merge(d, ds[0], *ds[1:])  #TODO shouldn't copy
    else:
        return d

def merge_with(f, d1, d2, *ds):
    d = d1.copy()  #TODO shouldn't copy
    for k in d2:
        if k in d:
            d[k] = f(d[k], d2[k])
        else:
            d[k] = d2[k]
    if ds:
        return merge_with(f, d, ds[0], *ds[1:])  #TODO shouldn't copy
    else:
        return d
    pass

def zipmap(ks, vs):
    return dict(zip(ks, vs))

## different semantics
#def zipmap(ks, vs):
#    return dict.fromkeys(ks, vs)

def get_in(d, ks):
    tmp = d
    for k in ks:
        tmp = tmp[k]
    return tmp

#TODO: as useful in python?
#def set_in(d, ks, v):
#def update_in(d, ks, f, *restargs):

## haskell

#union is like merge (but merge prefers later args)
#def union(d1, d2):
#    pass

def intersection(d1, d2):
    #TODO: using the simplest possible implementation, not optimal
    ks1 = set(d1.iterkeys())
    ks2 = set(d2.iterkeys())
    ks = ks1 & ks2
    return dict((k, d1[k]) for k in ks)

def difference(d1, d2):
    #TODO: using the simplest possible implementation, not optimal
    ks1 = set(d1.iterkeys())
    ks2 = set(d2.iterkeys())
    ks = ks1 - ks2
    return dict((k, d1[k]) for k in ks)

def map_values(f, d):
    return dict((k, f(v)) for k, v in d.iteritems())

def map_keys(f, d):
    return dict((f(k), v) for k, v in d.iteritems())

def partition_on_value(pred, d):
    pred_true = {}
    pred_false = {}
    for k, v in d.iteritems():
        if pred(v):
            pred_true[k] = v
        else:
            pred_false[k] = v
    return pred_true, pred_false

def partition_on_key(pred, d):
    pred_true = {}
    pred_false = {}
    for k, v in d.iteritems():
        if pred(k):
            pred_true[k] = v
        else:
            pred_false[k] = v
    return pred_true, pred_false

def issubdict(d1, d2):
    return all((k in d2 and d1[k] == d2[k]) for k in d1)

def key_set(d):
    return set(d.iterkeys())
def val_set(d):
    return set(d.itervalues())

## sql
##TODO: group by f key, f val, f (key, val)?
def group_by(f, d):
    res = defaultdict(list)
    for k, v in d.iteritems():
        newk = f(k)
        res[newk].append(v)
    return res

def project(d, ks):
    return dict((k, d[k]) for k in ks)

# ruby values_at
def project_list(d, ks):
    return [d[k] for k in ks]

def where(pred, d):
    return dict((k, v) for k, v in d.iteritems() if pred(k, v))
def where_key(pred, d):
    return dict((k, v) for k, v in d.iteritems() if pred(k))
def where_value(pred, d):
    return dict((k, v) for k, v in d.iteritems() if pred(v))

## ruby
def del_if(pred, d):
    to_del = [k for k,v in d.iteritems() if pred(k,v)]
    for k in to_del:
        del d[k]

def isempty(d):
    return len(d) == 0

# flatten

def invert(d):
    return dict((v,k) for k,v in d.iteritems())

#rename?
def rassoc(d, val):
    for k,v in d.iteritems():
        if v == val:
            return k,v
    return None

# same as 'where' above (but faster?!)
# make an iterator?
def select(pred, d):
    ret = {}
    for k,v in d.iteritems():
        if pred(k,v):
            ret[k] = v
    return ret

# has_value
# values_at

## javascript
#TODO: js object-like dict class?
# e.g. d.foo is an alias for d['foo']

## perl
# eh.
