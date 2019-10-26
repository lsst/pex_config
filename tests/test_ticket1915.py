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


class Config2(pexConf.Config):
    c = pexConf.ConfigField("Config2.c", Config1)


class Config3(pexConf.Config):
    r = pexConf.ConfigChoiceField("Config3.r", {"c1": Config1, "c2": Config2}, default="c1")


class HistoryMergeTest(unittest.TestCase):
    def test(self):
        a = Config2()
        b = Config2()
        b.c.f = 3
        b.c.f = 5
        a.c = b.c

        self.assertEqual([h[0] for h in a.c.history["f"]], [4, 5])

        c = Config3()
        c.r["c1"] = b.c
        c.r["c2"] = a

        self.assertEqual([h[0] for h in c.r["c1"].history["f"]], [4, 5])
        self.assertEqual([h[0] for h in c.r["c2"].c.history["f"]], [4, 5])


if __name__ == "__main__":
    unittest.main()
