import unittest
import sys
sys.path.append('..')
from server.resource_map import MDS, NMDS, PM1, PM2
import numpy as np


class TestAlgorithms(unittest.TestCase):
    def test_mds_running(self):
        a = np.random.randint(100000, size=30).reshape(-1, 3)
        print('test data shape', a.shape)
        mds = MDS()
        print('fit data shape', mds.fit(a).shape)
        print('=' * 20)

    def test_nmds_running(self):
        a = np.random.randint(100000, size=30).reshape(-1, 3)
        print('test data shape', a.shape)
        nmds = NMDS()
        print('fit data shape', nmds.fit(a).shape)
        print('=' * 20)

    def test_pm1_running(self):
        a = np.random.randint(100000, size=30).reshape(-1, 3)
        print('test data shape', a.shape)
        pm1 = PM1()
        print('fit data shape', pm1.fit(a).shape)
        print('=' * 20)

    def test_pm2_running(self):
        a = np.random.randint(100000, size=30).reshape(-1, 3)
        print('test data shape', a.shape)
        pm2 = PM2()
        print('fit data shape', pm2.fit(a).shape)
        print('=' * 20)
