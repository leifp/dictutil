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
        self.assertEqual(merge_with(f), {})
        self.assertEqual(merge_with(f, d1), d1)

    def test_zipdict(self):
        ks = [1, 2, 3]; vs = "abc"
        self.assertEqual(zipdict(ks, vs), {1: 'a', 2: 'b', 3: 'c'})
        ks = [1, 2, 3]; vs = [2, 4, 6]
        self.assertEqual(zipdict(ks, vs), {1: 2, 2: 4, 3: 6})
        ks = [1, 2, 3]; vs = [2, 4]
        self.assertEqual(zipdict(ks, vs), {1: 2, 2: 4})
        ks = [1, 2, 3]; vs = [2]
        self.assertEqual(zipdict(ks, vs), {1: 2})
        ks = [1, 2, 3]; vs = []
        self.assertEqual(zipdict(ks, vs), {})
        ks = [1, 2]; vs = [2, 4, 6]
        self.assertEqual(zipdict(ks, vs), {1: 2, 2: 4})
        ks = [1]; vs = [2, 4, 6]
        self.assertEqual(zipdict(ks, vs), {1: 2})
        ks = []; vs = [2, 4, 6]
        self.assertEqual(zipdict(ks, vs), {})

    #def test_zipdict(self):
    #    self.assertTrue(False)

    def test_get_in(self):
        d = {1: {2: {3: 'data'}}}
        self.assertEqual(get_in(d, [1, 2, 3]), 'data')
        self.assertEqual(get_in(d, [1, 2]), {3: 'data'})
        self.assertEqual(get_in(d, [1]), {2: {3: 'data'}})
        self.assertEqual(get_in(d, []), d)
        self.assertIs(get_in(d, [1, 999]), None)

    def test_set_in(self):
        d = {}
        set_in(d, [1, 2, 3, 4], 'test')
        self.assertEqual(d, {1: {2: {3: {4: 'test'}}}})
        d = {1: {2: {3: {4: 'anything but original'}}}}
        set_in(d, [1, 2, 3, 4], 'test')
        self.assertEqual(d, {1: {2: {3: {4: 'test'}}}})
        d = {1: {2: {3: {4: 'anything but original'}, 'x': 5}}}
        set_in(d, [1, 2, 3, 4], 'test')
        self.assertEqual(d, {1: {2: {3: {4: 'test'}, 'x': 5}}})

        self.assertRaisesRegexp(KeyError, "Empty keys iterable",
            set_in, {}, [], 'test')
        self.assertRaisesRegexp(KeyError, "Empty keys iterable",
            set_in, {'answer': 42}, [], 'test')

        # this will raise an exception
        d = {1: {2: {3: 'anything but original'}, 'x': 5}}
        try:
            d[1][2][3][4] = 'test'
            # unreachable
            self.fail("python dicts seem to have changed semantics.")
        except TypeError, e:
            self.assertTrue(
              0 <= e.message.find(
                "'str' object does not support item assignment"))
        # so we should, too
        d = {1: {2: {3: 'anything but original'}, 'x': 5}}
        self.assertRaisesRegexp(
          TypeError, "'str' object does not support item assignment",
          set_in, d, [1,2,3,4], 'test')

        # this will happily update lists
        d = {1: {2: [1, 2, 3, 4]}}
        d[1][2][3] = 999
        self.assertEqual(d, {1: {2: [1, 2, 3, 999]}})
        # so we should, too
        d = {1: {2: [1, 2, 3, 4]}}
        set_in(d, [1, 2, 3], 999)
        self.assertEqual(d, {1: {2: [1, 2, 3, 999]}})

        # make sure we don't modify the `ks` argument
        d = {}
        ks = [1, 2, 3, 4]
        set_in(d, ks, 'test')
        self.assertEqual(d, {1: {2: {3: {4: 'test'}}}})
        self.assertEqual(ks, [1, 2, 3, 4])

    def test_update_in(self):
        add10 = lambda v: v + 10
        addn = lambda v, n: v + n

        d = {1: 32}
        update_in(d, [1], add10)
        self.assertEqual(d, {1: 42})

        d = {1: {2: {3: {4: 32}}}}
        update_in(d, [1, 2, 3, 4], add10)
        self.assertEqual(d, {1: {2: {3: {4: 42}}}})

        d = {1: {2: {3: {4: 32}, 'x': 5}}}
        update_in(d, [1, 2, 3, 4], add10)
        self.assertEqual(d, {1: {2: {3: {4: 42}, 'x': 5}}})

        d1 = {1: 32}
        d2 = {1: 32}
        update_in(d1, [1], add10)
        update_in(d2, [1], addn, 10)
        self.assertEqual(d1, d2)

        d = {1: {2: ['foo']}}
        update_in(d, [1, 2], lambda v, x: v + x, ['bar'])
        self.assertEqual(d, {1: {2: ['foo', 'bar']}})

        # invalid update func
        d = {1: {2: {3: 'anything but original'}, 'x': 5}}
        self.assertRaisesRegexp(
          TypeError, "cannot concatenate 'str' and 'int' objects",
          update_in, d, [1,2,3,4], add10)
        # key in path doesn't exist
        d = {1: {2: {3: {}}, 'x': 5}}
        self.assertRaisesRegexp(KeyError, "4",
                                update_in, d, [1,2,3,4], add10)
        # empty ks
        self.assertRaisesRegexp(KeyError, "Empty keys iterable", 
                                update_in, d, [], add10)

        # this will happily update lists
        d = {1: {2: [1, 2, 3, 4]}}
        d[1][2][3] = add10(d[1][2][3])
        self.assertEqual(d, {1: {2: [1, 2, 3, 14]}})
        # so we should, too
        d = {1: {2: [1, 2, 3, 4]}}
        update_in(d, [1, 2, 3], add10)
        self.assertEqual(d, {1: {2: [1, 2, 3, 14]}})

## haskell
    #union is like merge
    #def test_union(self): #union(d1, d2)
    #    self.assertTrue(False)

    def test_intersection(self): #intersection(d1, d2)
        d1 = {1: 2, 3: 4, 5: 6}
        d2 = {1: 1, 3: 3, 7: 8}
        #favor keys from the first arg
        self.assertEqual(intersection(d1, d2), {1: 2, 3: 4})
        self.assertEqual(intersection(d2, d1), {1: 1, 3: 3})
        self.assertEqual(intersection(d1, d1), d1)
        self.assertEqual(intersection({}, d1), {})
        self.assertEqual(intersection(d1, {}), {})

    def test_difference(self):
        d1 = {1: 2, 3: 4, 5: 6}
        d2 = {1: 1, 3: 3, 7: 8}
        #favor keys from the first arg
        self.assertEqual(difference(d1, d2), {5: 6})
        self.assertEqual(difference(d2, d1), {7: 8})
        self.assertEqual(difference(d1, d1), {})
        self.assertEqual(difference({}, d1), {})
        self.assertEqual(difference(d1, {}), d1)

    def test_map_values(self):
        f = lambda v: 2*v
        d = {1: 1, 2: 2, 3: 3}
        self.assertEqual(map_values(f, d), {1: 2, 2: 4, 3: 6})
        self.assertEqual(map_values(f, {}), {})

    def test_map_keys(self):
        f = lambda k: 2*k
        d1 = {1: 10, 2: 20, 3: 30}
        self.assertEqual(map_keys(f, d1), {2: 10, 4: 20, 6: 30})
        g = lambda k: 0  #all keys map to same result key
        d2 = {1: 1, 2: 2, 3: 3}  # ambiguous case
        self.assertIn(map_keys(g, d2),
                [{0: 1}, {0: 2}, {0: 3}])
        self.assertEqual(map_keys(f, {}), {})

    def test_partition_on_value(self):
        pred = lambda v: (v % 2 == 0)
        d = {1: 1, 2: 3, 3: 6, 4: 8}
        self.assertEqual(partition_on_value(pred, d),
                ({3: 6,4: 8}, {1: 1, 2: 3}))
        pred = lambda v: (v > 0)
        self.assertEqual(partition_on_value(pred, d), (d, {}))
        pred = lambda v: (v < 0)
        self.assertEqual(partition_on_value(pred, d), ({}, d))
        self.assertEqual(partition_on_value(pred, {}), ({}, {}))

    def test_partition_on_key(self):
        pred = lambda k: (k % 2 == 0)
        d = {1: 1, 2: 3, 3: 6, 4: 8}
        self.assertEqual(partition_on_key(pred, d),
                ({2: 3, 4: 8}, {1: 1, 3: 6}))
        pred = lambda k: (k > 0)
        self.assertEqual(partition_on_key(pred, d), (d, {}))
        pred = lambda k: (k < 0)
        self.assertEqual(partition_on_key(pred, d), ({}, d))
        self.assertEqual(partition_on_key(pred, {}), ({}, {}))

    def test_issubdict(self):
        d1 = {1:2, 3: 4}
        d2 = {1:2, 3: 4, 5:6}
        self.assertTrue(issubdict(d1, d2))
        self.assertFalse(issubdict(d2, d1))
        self.assertTrue(issubdict({}, d1))
        self.assertTrue(issubdict({}, d2))
        self.assertFalse(issubdict(d1, {}))
        self.assertFalse(issubdict(d2, {}))

    def test_key_set(self):
        d = {1: 2, 3: 4, 5: 6}
        self.assertEqual(key_set(d), set([1, 3, 5]))
        d = {1: 2, 3: 4}
        self.assertEqual(key_set(d), set([1, 3]))
        d = {}
        self.assertEqual(key_set(d), set())

    def test_value_set(self):
        d = {1: 2, 3: 4, 5: 6}
        self.assertEqual(value_set(d), set([2, 4, 6]))
        d = {1: 0, 3: 0, 5: 0}
        self.assertEqual(value_set(d), set([0]))
        d = {}
        self.assertEqual(value_set(d), set())

    ## sql
    def test_group_by(self):
        f = lambda k: k % 2
        d = {1: 2, 2: 3, 3: 4, 4: 5}

        self.assertEqual(group_by(f, {}), {})

        grps = group_by(f, d)
        for k in grps:
            grps[k].sort()
        self.assertEqual(grps, {0: [3, 5], 1: [2, 4]})

        self.assertEqual(group_by(f, d, reverse=True),
                         {0: [5, 3], 1: [4, 2]})

        d = {1: (1, 2, 3), 2: (1, 3, 2), 3: (3, 2, 1)}
        second_third = lambda x: (x[1], x[2])
        cmp_third = lambda x, y: cmp(x[2], y[2])
        self.assertEqual(group_by(bool, d, reverse=False),
                         {True: [(1, 2, 3), (1, 3, 2), (3, 2, 1)]})
        self.assertEqual(group_by(bool, d, reverse=True),
                         {True: [(3, 2, 1), (1, 3, 2), (1, 2, 3)]})
        self.assertEqual(group_by(bool, d, key=second_third),
                         {True: [(3, 2, 1), (1, 2, 3), (1, 3, 2)]})
        self.assertEqual(group_by(bool, d, key=second_third, reverse=True),
                         {True: [(1, 3, 2), (1, 2, 3), (3, 2, 1)]})
        self.assertEqual(group_by(bool, d, cmp=cmp_third),
                         {True: [(3, 2, 1), (1, 3, 2), (1, 2, 3)]})
        self.assertEqual(group_by(bool, d, cmp=cmp_third, reverse=True),
                         {True: [(1, 2, 3), (1, 3, 2), (3, 2, 1)]})

    def test_index(self):
        self.assertEqual(index({1: 'foo bar', 2: 'foo baz'}, str.split),
            {'foo': set([1, 2]), 'bar': set([1]), 'baz': set([2])})
        import re
        tokenize = lambda s: re.split(r'\s*,\s*', s)
        self.assertEqual(index({1: 'foo, bar,baz', 2: 'foo,baz'}, tokenize),
            {'foo': set([1, 2]), 'bar': set([1]), 'baz': set([1, 2])})
        upto = lambda n: xrange(n)  # works with generators
        self.assertEqual(index({1: 3, 2: 2}, upto),
            {0: set([1, 2]), 1: set([1, 2]), 2: set([1])})
        self.assertEqual(
                index({1: {'name': 'arthur'}, 2: {'name': 'arthur'},
                       3: {'name': 'robin'}, 4: {'no': 'name'}},
                       lambda d: [d.get('name')]),  # need iterable
            {'arthur': set([1, 2]), 'robin': set([3]), None: set([4])})

    def test_project(self):
        d = {1: 'one', 2: 'two', 'knights': 'ni'}
        self.assertEqual(project(d, [1, 2]), {1: 'one', 2: 'two'})
        self.assertEqual(project(d, [1]), {1: 'one'})
        self.assertEqual(project(d, [2, 'knights']),
                         {2: 'two', 'knights': 'ni'})
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
        pred = lambda k, v: k < v
        self.assertEqual(where(pred, d), {1: 2, 3: 4})
        pred = lambda k, v: k > v
        self.assertEqual(where(pred, d), {2: 1})
        pred = lambda k, v: k == v
        self.assertEqual(where(pred, d), {4: 4})
        pred = lambda k, v: False
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
        pred = lambda k, v: k < v
        del_if(pred, d)
        self.assertEqual(d, {2: 1, 4: 4})

        d = {1: 2, 2: 1, 3: 4, 4: 4}
        pred = lambda k, v: True
        del_if(pred, d)
        self.assertEqual(d, {})

        old_d = {1: 2, 2: 1, 3: 4, 4: 4}
        d = {1: 2, 2: 1, 3: 4, 4: 4}
        pred = lambda k, v: False
        del_if(pred, d)
        self.assertEqual(d, old_d)

    def test_isempty(self):
        self.assertTrue(isempty({}))
        self.assertFalse(isempty({1:2}))
        self.assertFalse(isempty({1:2, 3:4}))
        self.assertFalse(isempty({1:2, 3:4, 5:6}))

    #TODO: flatten ?

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
        self.assertIn(rassoc(d, 2), [(1, 2), (3, 2)])
        self.assertIs(rassoc({}, 1), None)
        self.assertIs(rassoc({}, None), None)

    # same as 'where' above (but faster?!)
    # make an iterator?
    def test_select(self): #select(pred, d)
        d = {1: 2, 2: 1, 3: 4, 4: 4}
        pred = lambda k, v: k < v
        self.assertEqual(select(pred, d), {1: 2, 3: 4})
        pred = lambda k, v: k > v
        self.assertEqual(select(pred, d), {2: 1})
        pred = lambda k, v: k == v
        self.assertEqual(select(pred, d), {4: 4})
        pred = lambda k, v: False
        self.assertEqual(select(pred, d), {})

# has_value
# values_at

if __name__ == '__main__':
    unittest.main()
