from collections import defaultdict

## clj
def merge(d1, d2, *ds):
    pass

def merge_with(f, d1, d2, *ds):
    pass

def zipmap(ks, vs):
    return dict(zip(ks, vs))

def zipmap(ks, vs):
    return dict.fromkeys(ks, vs)

def get_in(d, ks):
    tmp = d
    for k in ks:
        tmp = tmp[k]
    return tmp

#def set_in(d, ks, v):

## haskell
def union(d1, d2):
    pass
def intersection(d1, d2):
    pass
def difference(d1, d2):
    pass
def map_values(f, d):
    pass
def map_keys(f, d):
    pass

def partition(pred, d):
    pass
def split(pred, d):
    pass
def issubdict(d1, d2):
    pass

def key_set(d):
    return set(d.iterkeys())
def val_set(d):
    return set(d.itervalues())

## sql
def group_by(f, d):
    pass

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
# js object-like dict class?
# e.g. d.foo is an alias for d['foo']

## perl
# eh.
