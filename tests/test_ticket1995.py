# This file is part of pex_config.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.

import math
import tempfile
import unittest
import lsst.pex.config as pexConf


class PexTestConfig(pexConf.Config):
    list1 = pexConf.ListField(dtype=int, default=[1, 2], doc="list1")
    f1 = pexConf.Field(dtype=float, doc="f1")
    f2 = pexConf.Field(dtype=float, doc="f2")


class EqualityTest(unittest.TestCase):
    def test(self):
        c1 = PexTestConfig()
        c2 = PexTestConfig()
        self.assertEqual(c1, c2)
        c1.list1 = [1, 2, 3, 4, 5]
        self.assertNotEqual(c1, c2)
        c2.list1 = c1.list1
        self.assertEqual(c1, c2)


class LoadSpecialTest(unittest.TestCase):
    def test(self):
        c1 = PexTestConfig()
        c2 = PexTestConfig()
        c1.list1 = None
        c1.f1 = float('nan')
        c2.f2 = float('inf')
        with tempfile.NamedTemporaryFile(mode="w") as f:
            c1.saveToStream(f.file)
            f.file.close()
            c2.load(f.name)
        self.assertEqual(c1.list1, c2.list1)
        self.assertEqual(c1.f2, c2.f2)
        self.assertTrue(math.isnan(c2.f1))


if __name__ == "__main__":
    unittest.main()
