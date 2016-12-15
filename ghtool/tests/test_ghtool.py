from unittest import TestCase

import argparse
import ghtool

class TestGHTool(TestCase):
    def test_is_parser(self):
        parser = ghtool.init_parser()
        self.assertTrue(isinstance(parser, argparse.ArgumentParser))
