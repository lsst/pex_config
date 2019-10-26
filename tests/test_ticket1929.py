# This file is part of pex_config.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.

import unittest
import lsst.pex.config as pexConf


class Config1(pexConf.Config):
    f = pexConf.Field("Config1.f", float, default=4)


class Config2(Config1):
    def setDefaults(self):
        self.f = 5


class Config3(Config1):

    def __init__(self, **kw):
        self.f = 6


class SquashingDefaultsTest(unittest.TestCase):
    def test(self):
        c1 = Config1()
        self.assertEqual(c1.f, 4)
        c1 = Config1(f=9)
        self.assertEqual(c1.f, 9)

        c2 = Config2()
        self.assertEqual(c2.f, 5)
        c2 = Config2(f=10)
        self.assertEqual(c2.f, 10)

        c3 = Config3()
        self.assertEqual(c3.f, 6)
        c3 = Config3(f=11)
        self.assertEqual(c3.f, 6)


if __name__ == "__main__":
    unittest.main()
