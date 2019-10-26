# This file is part of pex_config.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.

from ticket2818helper.define import TestConfig, TestConfigurable


class AnotherConfig(TestConfig):
    pass


class AnotherConfigurable(TestConfigurable):
    ConfigClass = AnotherConfig
