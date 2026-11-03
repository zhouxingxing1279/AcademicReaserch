import unittest
from fractions import Fraction as Q
from check_template_caps import replay, noise_support, raw_clip_counterexamples


class TemplateCapTests(unittest.TestCase):
    def test_shared_noise_support(self):
        self.assertEqual(noise_support((Q(1),Q(1)),1),Q(1,10))
        self.assertEqual(noise_support((Q(0),-Q(1,2)),1),Q(3,40))

    def test_coarse_or_missing_queries_retain_feasibility(self):
        for inflation in (Q(0),Q(1,20),Q(1),None):
            r=replay(inflation)
            self.assertEqual(r['steps'],1024)
            self.assertEqual(r['violations'],0)

    def test_unprotected_missing_queries_can_lose_candidate(self):
        self.assertGreater(replay(None)['uncapped_candidate_rejections'],0)

    def test_invalid_clips_are_counterexamples(self):
        r=raw_clip_counterexamples()
        self.assertLess(r['arbitrary_cap'],r['true_endpoint'])
        self.assertLess(r['cap_from_inflated_noise'],r['valid_initial_support'])


if __name__=='__main__':unittest.main()
