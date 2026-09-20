import unittest
from fractions import Fraction as Q
from check_anytime_set_learning import cell_interval, cover_interval, atomic_split, dual_upper


class AnytimeContractTests(unittest.TestCase):
    def test_exact_relaxation_values(self):
        expected = [(Q(8,7),Q(12,5)), (Q(4,3),Q(20,9)),
                    (Q(44,31),Q(36,17)), (Q(92,63),Q(68,33))]
        for n, want in zip((1,2,4,8), expected):
            leaves = [(1+Q(i,n),1+Q(i+1,n)) for i in range(n)]
            self.assertEqual(cover_interval(leaves), want)
            self.assertLessEqual(want[0], Q(3,2))
            self.assertGreaterEqual(want[1], Q(2))

    def test_unfinished_split_retains_parent(self):
        root = [(Q(1),Q(2))]
        self.assertEqual(atomic_split(root,0,completed_children=1), root)
        children = atomic_split(root,0,completed_children=2)
        self.assertEqual(cover_interval(children), (Q(4,3),Q(20,9)))

    def test_dropping_unvisited_cell_excludes_valid_truth(self):
        bad = cover_interval([(Q(1),Q(5,4))])
        self.assertGreater(bad[0], Q(3,2))
        # True point theta=3/2, x=2, z=3 must remain possible.

    def test_dual_rounding_residual_is_not_ignored(self):
        # max x, x<=1, x in [0,2], rounded multiplier 9/10.
        self.assertEqual(dual_upper([1], [[1]], [1], [Q(9,10)], [(0,2)]), Q(11,10))
        self.assertEqual(dual_upper([1], [[1]], [1], [0], [(0,2)]), Q(2))
        with self.assertRaises(ValueError):
            dual_upper([1], [[1]], [1], [-1], [(0,2)])

    def test_refinement_is_nested(self):
        leaves = [(Q(1),Q(2))]
        previous = cover_interval(leaves)
        for j in range(15):
            leaves = atomic_split(leaves,j % len(leaves),completed_children=2)
            current = cover_interval(leaves)
            self.assertTrue(previous[0] <= current[0] <= Q(3,2))
            self.assertTrue(Q(2) <= current[1] <= previous[1])
            previous = current

    def test_closed_form_budget_error(self):
        # Compare analytic endpoint formula to independent vertex enumeration.
        for n in range(1,25):
            leaves = [(1+Q(i,n),1+Q(i+1,n)) for i in range(n)]
            actual = cover_interval(leaves)
            self.assertEqual(actual, (Q(12*n-4,8*n-1),Q(8*n+4,4*n+1)))
            distance = max(Q(3,2)-actual[0],actual[1]-2)
            self.assertEqual(distance,Q(2,4*n+1))


if __name__ == '__main__':
    unittest.main()
