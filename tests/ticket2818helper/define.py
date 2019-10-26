# This file is part of pex_config.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.

from lsst.pex.config import Config, ConfigurableField


class TestConfig(Config):
    pass


class TestConfigurable:
    ConfigClass = TestConfig

    def __init__(self, config):
        self.config = config

    def what(self):
        return self.__class__.__name__


class BaseConfig(Config):
    test = ConfigurableField(target=TestConfigurable, doc="")
