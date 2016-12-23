from unittest import TestCase

import argparse
import ghtool

class TestGHTool(TestCase):
    def test_is_parser(self):
        parser = ghtool.create_parser()
        self.assertTrue(isinstance(parser, argparse.ArgumentParser))
