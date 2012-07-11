import unittest
from dictutil import *

class TestDictUtil(unittest.TestCase):
    """
    Tests for the dictutils library.
    """
## clj
    def test_merge(self):
        d1 = {'lancelot': 'brave', 'galahad': 'pure'}
        d2 = {'robin': 'not-quite-so-brave'}
        self.assertEqual(merge(d1, d2), {'lancelot': 'brave', 
            'galahad': 'pure', 'robin': 'not-quite-so-brave'})
        self.assertEqual(merge(d1, {}), d1)
        self.assertEqual(merge({}, d1), d1)
        self.assertEqual(merge({}, {}), {})
        d3 = {'bedevere': 'wise'}
        d4 = {'arthur': 'kingly'}
        self.assertEqual(merge(d1, d2, d3, d4),
            {'lancelot': 'brave', 'galahad': 'pure', 'arthur': 'kingly',
             'robin': 'not-quite-so-brave', 'bedevere': 'wise'})
        d5 = {'robin': 'brave-in-the-end'}
        self.assertEqual(merge(d2, d5), d5) #later keys overwrite
        self.assertEqual(merge(d5, d2), d2)

    def test_merge_with(self):
        f = lambda x, y: x + y
        d1 = {1: 2, 3: 4, 5: 6}
        d2 = {1: 40, 4: 3, 5: -6}
        d3 = {1: -42, 3: -1, 4: -3, 5: 5}
        d4 = {1: 11, 2: 22, 9: 99}
        self.assertEqual(merge_with(f, d1, d2), {1: 42, 3: 4, 4: 3, 5: 0})
        self.assertEqual(merge_with(f, d1, {}), d1)
        self.assertEqual(merge_with(f, {}, d1), d1)
        self.assertEqual(merge_with(f, {}, {}), {})
        self.assertEqual(merge_with(f, d1, d2, d3), {1: 0, 3: 3, 4: 0, 5: 5})
        self.assertEqual(merge_with(f, d1, d2, d3, d4), 
                {1: 11, 2: 22, 3: 3, 4: 0, 5: 5, 9: 99})
        f = lambda x, y: (x + (y, )) if isinstance(x, tuple) else (x, y)
        self.assertEqual(merge_with(f, d1, d2, d3), 
                {1: (2, 40, -42), 3: (4, -1), 4: (3, -3), 5: (6, -6, 5)})

    def test_zipmap(self):
        ks = [1, 2, 3]; vs = "abc"
        self.assertEqual(zipmap(ks, vs), {1: 'a', 2: 'b', 3: 'c'})
        ks = [1, 2, 3]; vs = [2, 4, 6]
        self.assertEqual(zipmap(ks, vs), {1: 2, 2: 4, 3: 6})
        ks = [1, 2, 3]; vs = [2, 4]
        self.assertEqual(zipmap(ks, vs), {1: 2, 2: 4})
        ks = [1, 2, 3]; vs = [2]
        self.assertEqual(zipmap(ks, vs), {1: 2})
        ks = [1, 2, 3]; vs = []
        self.assertEqual(zipmap(ks, vs), {})
        ks = [1, 2]; vs = [2, 4, 6]
        self.assertEqual(zipmap(ks, vs), {1: 2, 2: 4})
        ks = [1]; vs = [2, 4, 6]
        self.assertEqual(zipmap(ks, vs), {1: 2})
        ks = []; vs = [2, 4, 6]
        self.assertEqual(zipmap(ks, vs), {})

    #def test_zipmap(self):
    #    self.assertTrue(False)

    def test_get_in(self):
        d = {1: {2: {3: 'data'}}}
        self.assertEqual(get_in(d, [1,2,3]), 'data')
        self.assertEqual(get_in(d, [1,2]), {3: 'data'})
        self.assertEqual(get_in(d, [1]), {2: {3: 'data'}})
        self.assertEqual(get_in(d, []), d)

#def set_in(d, ks, v):

## haskell
    #union is like merge
    #def test_union(self): #union(d1, d2)
    #    self.assertTrue(False)

    def test_intersection(self): #intersection(d1, d2)
        self.assertTrue(False)

    def test_difference(self): #difference(d1, d2)
        self.assertTrue(False)

    def test_map_values(self): #map_values(f, d)
        self.assertTrue(False)

    def test_map_keys(self): #map_keys(f, d)
        self.assertTrue(False)

    def test_partition(self): #partition(pred, d)
        self.assertTrue(False)

    def test_split(self): #split(pred, d)
        self.assertTrue(False)

    def test_issubdict(self): #issubdict(d1, d2)
        self.assertTrue(False)

    def test_key_set(self):
        d = {1: 2, 3: 4, 5: 6}
        self.assertEqual(key_set(d), set([1,3,5]))
        d = {1: 2, 3: 4}
        self.assertEqual(key_set(d), set([1,3]))
        d = {}
        self.assertEqual(key_set(d), set())

    def test_val_set(self):
        d = {1: 2, 3: 4, 5: 6}
        self.assertEqual(val_set(d), set([2,4,6]))
        d = {1: 0, 3: 0, 5: 0}
        self.assertEqual(val_set(d), set([0]))
        d = {}
        self.assertEqual(val_set(d), set())

## sql
    def test_group_by(self): #group_by(f, d)
        self.assertTrue(False)

    def test_project(self):
        d = {1: 'one', 2: 'two', 'knights': 'ni'}
        self.assertEqual(project(d, [1, 2]), {1: 'one', 2: 'two'})
        self.assertEqual(project(d, [1]), {1: 'one'})
        self.assertEqual(project(d, [2, 'knights']), {2: 'two', 'knights': 'ni'})
        self.assertEqual(project(d, []), {})

# ruby values_at
    def test_project_list(self):
        d = {1: 'one', 2: 'two', 'knights': 'ni'}
        self.assertEqual(project_list(d, [1, 2]), ['one', 'two'])
        self.assertEqual(project_list(d, [1]), ['one'])
        self.assertEqual(project_list(d, [2, 'knights']), ['two', 'ni'])
        self.assertEqual(project_list(d, []), [])

    def test_where(self):
        d = {1: 2, 2: 1, 3: 4, 4: 4}
        pred = lambda k,v: k < v
        self.assertEqual(where(pred, d), {1: 2, 3: 4})
        pred = lambda k,v: k > v
        self.assertEqual(where(pred, d), {2: 1})
        pred = lambda k,v: k == v
        self.assertEqual(where(pred, d), {4: 4})
        pred = lambda k,v: False
        self.assertEqual(where(pred, d), {})

    def test_where_key(self):
        d = {1: 2, 2: 1, 3: 4, 4: 4}
        pred = lambda k: k < 3
        self.assertEqual(where_key(pred, d), {1: 2, 2: 1})
        pred = lambda k: k > 3
        self.assertEqual(where_key(pred, d), {4: 4})
        pred = lambda k: k == 3
        self.assertEqual(where_key(pred, d), {3: 4})
        pred = lambda k: False
        self.assertEqual(where_key(pred, d), {})

    def test_where_value(self):
        d = {1: 2, 2: 1, 3: 4, 4: 4}
        pred = lambda v: v < 3
        self.assertEqual(where_value(pred, d), {1: 2, 2: 1})
        pred = lambda v: v > 3
        self.assertEqual(where_value(pred, d), {3: 4, 4: 4})
        pred = lambda v: v == 3
        self.assertEqual(where_value(pred, d), {})
        pred = lambda v: False
        self.assertEqual(where_value(pred, d), {})

## ruby
    def test_del_if(self):
        d = {1: 2, 2: 1, 3: 4, 4: 4}
        pred = lambda k,v: k < v
        del_if(pred, d)
        self.assertEqual(d, {2: 1, 4: 4})

        d = {1: 2, 2: 1, 3: 4, 4: 4}
        pred = lambda k,v: True
        del_if(pred, d)
        self.assertEqual(d, {})

        old_d = {1: 2, 2: 1, 3: 4, 4: 4}
        d = {1: 2, 2: 1, 3: 4, 4: 4}
        pred = lambda k,v: False
        del_if(pred, d)
        self.assertEqual(d, old_d)

    def test_isempty(self):
        self.assertTrue(isempty({}))
        self.assertFalse(isempty({1:2}))
        self.assertFalse(isempty({1:2, 3:4}))
        self.assertFalse(isempty({1:2, 3:4, 5:6}))

# flatten

    def test_invert(self):
        d = {1: 2, 3: 4}
        self.assertEqual(invert(d), {2: 1, 4: 3})
        d = {1: 1, 2: 2}
        self.assertEqual(invert(d), d)
        d = {1: 1, 2: 1}  # repeated value, inversion ambiguous
        self.assertIn(invert(d), [{1: 1}, {1: 2}])
        d = {}
        self.assertEqual(invert(d), {})

#rename?
    def test_rassoc(self):
        d = {1: 2, 3: 4}
        self.assertEqual(rassoc(d, 2), (1, 2))
        self.assertEqual(rassoc(d, 4), (3, 4))
        self.assertIs(rassoc(d, 1), None)
        self.assertIs(rassoc(d, 3), None)
        d = {1: 2, 3: 2}
        self.assertIn(rassoc(d, 2), [(1,2), (3,2)])

# same as 'where' above (but faster?!)
# make an iterator?
    def test_select(self): #select(pred, d)
        d = {1: 2, 2: 1, 3: 4, 4: 4}
        pred = lambda k,v: k < v
        self.assertEqual(select(pred, d), {1: 2, 3: 4})
        pred = lambda k,v: k > v
        self.assertEqual(select(pred, d), {2: 1})
        pred = lambda k,v: k == v
        self.assertEqual(select(pred, d), {4: 4})
        pred = lambda k,v: False
        self.assertEqual(select(pred, d), {})

# has_value
# values_at

