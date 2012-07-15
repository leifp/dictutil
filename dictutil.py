"""Useful functions for working with dicts."""
from collections import defaultdict

## clojure
def merge(*dicts):
    """Returns a dict that consists of the rest of the dicts merged with
    the first.  If a key occurs in more than one map, the value from the
    latter (left-to-right) will be the value in the result."""
    d = dict()
    for _dict in dicts:
        d.update(_dict)
    return d

def merge_with(f, *dicts):
    """Returns a dict that consists of the rest of the dicts merged with
    the first.  If a key occurs in more than one map, the value from the
    latter (left-to-right) will be the combined with the value in the former
    by calling f(former_val, latter_val).  Calling with no dicts returns {}."""
    d = dict()
    for _dict in dicts:
        for k in _dict:
            if k in d:
                d[k] = f(d[k], _dict[k])
            else:
                d[k] = _dict[k]
    return d

def zipdict(ks, vs):
    """Returns a dict with the keys mapped to the corresponding vals."""
    return dict(zip(ks, vs))

## different semantics
#def zipdict(ks, vs):
#    return dict.fromkeys(ks, vs)

#TODO: add not_found=None ?
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

def set_in(d, ks, v):
    """ Sets the value in a nested associative structure, where `ks` is a
    sequence of keys. Creates the key if the key is not present.
    MUTATES `d`."""
    tmp = d
    i = None
    for i, next_key in enumerate(ks):
        if i > 0:
            tmp = tmp.setdefault(current_key, {})
        current_key = next_key
    if i is None:
        raise KeyError("Empty keys iterable")
    tmp[current_key] = v

def update_in(d, ks, f, *restargs):
    """'Updates' the value in a nested associative structure, where `ks` is a
    sequence of keys and `f` is a function that will take the old value and 
    any supplied args and return the new value.  Equivalent to
    d[k1][k2][...] = f(d[k1][k2][...], *restargs).
    An error is raised if the key at any level does not exist.
    MUTATES `d`.
    """
    tmp = d
    i = None
    for i, next_key in enumerate(ks):
        if i > 0:
            tmp = tmp.setdefault(current_key, {})
        current_key = next_key
    if i is None:
        raise KeyError("Empty keys iterable")
    tmp[current_key] = f(tmp[current_key], *restargs)

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

def partition(f, d):
    """Partition the dict according to an equivalence relation.

    Calls f(key, value) for all (key, value) pairs in the dict d.  The return
    value of f must be hashable.
    Returns a new dict where the keys are distinct return values of f, and the
    values are dicts containing the equivalence classes distinguished by those
    return values:

    >>> partition(lambda k, v: (k % 3), {0: 1, 1: 2, 2: 3, 3: 4, 4: 5})
    {0: {0: 1, 3: 4}, 1: {1: 2, 4: 5}, 2: {2: 3}}
    """
    partition = defaultdict(dict)
    for k, v in d.iteritems():
        partition[f(k, v)][k] = v
    return partition

def partition_on_value(pred, d):
    """Partition the dict according to a predicate on the values.
    Returns a tuple of two dicts:
    The first dict contains all elements that satisfy the predicate,
    the second all elements that fail the predicate."""
    f = lambda k, v: bool(pred(v))
    p = partition(f, d)
    return p[True], p[False]

def partition_on_key(pred, d):
    """Partition the dict according to a predicate on the keys.
    Returns a tuple of two dicts:
    The first dict contains all elements that satisfy the predicate,
    the second all elements that fail the predicate."""
    f = lambda k, v: bool(pred(k))
    p = partition(f, d)
    return p[True], p[False]

def issubdict(d1, d2):
    """All keys in `d1` are in `d2`, and corresponding values are equal."""
    return all((k in d2 and d1[k] == d2[k]) for k in d1)

#TODO: for python >= 2.7, reference dictviews
def key_set(d):
    """A set of all the keys of a dict."""
    return set(d.iterkeys())
def value_set(d):
    """A set of all the values of a dict."""
    return set(d.itervalues())

## sql
##TODO: group by f key, f val, f (key, val)?
def group_by(f, d, cmp=None, key=None, reverse=None):
    """Group by a function of the keys.  Returns a dict given by
    return_dict[f(k)] = [all values of original with same f(k)].
    If any of `cmp`, `key`, or `reverse` is given, sort all of the values
    of the result with `list.sort`."""
    res = defaultdict(list)
    for k, v in d.iteritems():
        newk = f(k)
        res[newk].append(v)
    if cmp or key or (reverse is not None):
        reverse = False if reverse is None else reverse
        for k in res:
            res[k].sort(cmp=cmp, key=key, reverse=reverse)
    return res

def index(d, index_f):
    """Creates an index of `d`:
    * Calls `index_f` for each value of `d`; this should return an iterable.
    * For each index_key in the iterable, add the item key to the set at
      result[index_key].
    E.g.,
    >>> index({1: 'foo bar', 2: 'foo baz'}, str.split)
    {'foo': set([1, 2]), 'bar': set([1]), 'baz': set([2])}"""
    res = defaultdict(set)
    for k, v in d.iteritems():
        idx_ks = index_f(v)
        for idx_k in idx_ks:
            res[idx_k].add(k)
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
    MUTATES `d`."""
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
# This has been done in a lot of places...
# for reference see attributedict at https://github.com/bitprophet/lexicon

## perl
# eh.
