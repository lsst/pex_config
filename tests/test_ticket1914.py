# This file is part of pex_config.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.

import os.path
import unittest
import lsst.pex.config as pexConf


class Config1(pexConf.Config):
    f = pexConf.Field("Config1.f", float, default=4)


class Config2(pexConf.Config):
    r = pexConf.ConfigChoiceField("Config2.r", {"c1": Config1}, default="c1")


class Config3(pexConf.Config):
    c = pexConf.ConfigField("Config3.c", Config2)


class FieldNameReportingTest(unittest.TestCase):
    def test(self):
        c3 = Config3()
        test_dir = os.path.dirname(os.path.abspath(__file__))
        c3.load(os.path.join(test_dir, "config/ticket1914.py"))


if __name__ == "__main__":
    unittest.main()
