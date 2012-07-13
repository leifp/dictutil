"""Useful functions for working with dicts."""
from collections import defaultdict

## clojure
def merge(*args):
    """Returns a dict that consists of the rest of the dicts merged with
    the first.  If a key occurs in more than one map, the value from the
    latter (left-to-right) will be the value in the result."""
    d = dict()
    for arg in args:
        d.update(arg)
    return d

def merge_with(f, d1, d2, *ds):
    """Returns a dict that consists of the rest of the dicts merged with
    the first.  If a key occurs in more than one map, the value from the
    latter (left-to-right) will be the combined with the value in the former
    by calling f(former_val, latter_val)."""
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

def zipdict(ks, vs):
    """Returns a dict with the keys mapped to the corresponding vals."""
    return dict(zip(ks, vs))

## different semantics
#def zipdict(ks, vs):
#    return dict.fromkeys(ks, vs)

def get_in(d, ks):
    """ Returns the value in a nested associative structure, where `ks` is a 
    sequence of keys. Returns None if the key is not present.  Returns `d` if
    `ks` is empty."""
    tmp = d
    for k in ks:
        tmp = tmp.get(k)
        if tmp is None:
            return None
    return tmp

#TODO: as useful in python?
#def set_in(d, ks, v):
#def update_in(d, ks, f, *restargs):

## haskell

#union is like merge (but merge prefers later args)
#def union(d1, d2):
#    pass

def intersection(d1, d2):
    """Intersection of two dicts. 
    Return data in the first dict for the keys existing in both dicts."""
    #TODO: using the simplest possible implementation, not optimal
    ks1 = set(d1.iterkeys())
    ks2 = set(d2.iterkeys())
    ks = ks1 & ks2
    return dict((k, d1[k]) for k in ks)

def difference(d1, d2):
    """Difference of two dicts.
    Return elements of the first dict not existing in the second dict."""
    #TODO: using the simplest possible implementation, not optimal
    ks1 = set(d1.iterkeys())
    ks2 = set(d2.iterkeys())
    ks = ks1 - ks2
    return dict((k, d1[k]) for k in ks)

def map_values(f, d):
    """Map a function over all values in the dict."""
    return dict((k, f(v)) for k, v in d.iteritems())

def map_keys(f, d):
    """Map a function over all keys in the dict."""
    return dict((f(k), v) for k, v in d.iteritems())

def partition_on_value(pred, d):
    """Partition the dict according to a predicate on the values. 
    Returns a tuple of two dicts:
    The first dict contains all elements that satisfy the predicate, 
    the second all elements that fail the predicate."""
    pred_true = {}
    pred_false = {}
    for k, v in d.iteritems():
        if pred(v):
            pred_true[k] = v
        else:
            pred_false[k] = v
    return pred_true, pred_false

def partition_on_key(pred, d):
    """Partition the dict according to a predicate on the keys. 
    Returns a tuple of two dicts:
    The first dict contains all elements that satisfy the predicate, 
    the second all elements that fail the predicate."""
    pred_true = {}
    pred_false = {}
    for k, v in d.iteritems():
        if pred(k):
            pred_true[k] = v
        else:
            pred_false[k] = v
    return pred_true, pred_false

def issubdict(d1, d2):
    """All keys in `d1` are in `d2`, and corresponding values are equal."""
    return all((k in d2 and d1[k] == d2[k]) for k in d1)

def key_set(d):
    """A set of all the keys of a dict."""
    return set(d.iterkeys())
def value_set(d):
    """A set of all the values of a dict."""
    return set(d.itervalues())

## sql
##TODO: group by f key, f val, f (key, val)?
def group_by(f, d):
    """Group by a function of the keys.  Returns a dict given by 
    return_dict[f(k)] = [all values of original with same f(k)]."""
    res = defaultdict(list)
    for k, v in d.iteritems():
        newk = f(k)
        res[newk].append(v)
    return res

def project(d, ks):
    """Return the subdict of `d` containing only the keys in `ks`."""
    return dict((k, d[k]) for k in ks)

# ruby values_at
def project_list(d, ks):
    """Return a list of the values of `d` at `ks`."""
    return [d[k] for k in ks]

def where(pred, d):
    """Return the subdict of `d` where `pred(k,v)` holds."""
    return dict((k, v) for k, v in d.iteritems() if pred(k, v))
def where_key(pred, d):
    """Return the subdict of `d` where `pred(k)` holds."""
    return dict((k, v) for k, v in d.iteritems() if pred(k))
def where_value(pred, d):
    """Return the subdict of `d` where `pred(v)` holds."""
    return dict((k, v) for k, v in d.iteritems() if pred(v))

## ruby
def del_if(pred, d):
    """Delete all items of `d` for which `pred(k,v)` holds.
    Operates on the dict in-place."""
    to_del = [k for k, v in d.iteritems() if pred(k, v)]
    for k in to_del:
        del d[k]

def isempty(d):
    """Is the dict empty?"""
    return len(d) == 0

# flatten

def invert(d):
    """Return a new dict, with the keys and values reversed.
    If there are duplicate values in the original, the result will only
    have one of the corresponding keys."""
    return dict((v, k) for k, v in d.iteritems())

#rename?
def rassoc(d, val):
    """Searches through the dict comparing `val` with the value. Returns
    the first item (k, v) that matches."""
    for k, v in d.iteritems():
        if v == val:
            return k, v
    return None

# same as 'where' above (but faster?!)
# make an iterator?
def select(pred, d):
    """Return the subdict of `d` where `pred(k,v)` holds."""
    ret = {}
    for k, v in d.iteritems():
        if pred(k, v):
            ret[k] = v
    return ret

# has_value
# values_at

## javascript
#TODO: js object-like dict class?
# e.g. d.foo is an alias for d['foo']

## perl
# eh.
