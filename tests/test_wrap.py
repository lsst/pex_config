# This file is part of pex_config.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.

import unittest

import testLib
import pickle


class WrapTest(unittest.TestCase):

    def testMakeControl(self):
        """Test making a C++ Control object from a Config object."""
        config = testLib.ConfigObject()
        config.foo = 2
        config.bar.append("baz")
        control = config.makeControl()
        self.assertTrue(testLib.checkControl(control, config.foo, config.bar.list()))

    def testReadControl(self):
        """Test reading the values from a C++ Control object into a Config object."""
        control = testLib.ControlObject()
        control.foo = 3
        control.bar = ["zot", "yox"]
        config = testLib.ConfigObject()
        config.readControl(control)
        self.assertTrue(testLib.checkControl(control, config.foo, config.bar.list()))

    def testDefaults(self):
        """Test that C++ Control object defaults are correctly used as defaults for Config objects."""
        config = testLib.ConfigObject()
        control = testLib.ControlObject()
        self.assertTrue(testLib.checkControl(control, config.foo, config.bar.list()))

    def testPickle(self):
        """Test that C++ Control object pickles correctly"""
        config = testLib.ConfigObject()
        new = pickle.loads(pickle.dumps(config))
        self.assertTrue(config.compare(new))
        self.assertTrue(new.compare(config))


class NestedWrapTest(unittest.TestCase):

    def testMakeControl(self):
        """Test making a C++ Control object from a Config object."""
        config = testLib.OuterConfigObject()
        self.assertIsInstance(config.a, testLib.InnerConfigObject)
        config.a.p = 5.0
        config.a.q = 7
        config.b = 2
        control = config.makeControl()
        self.assertTrue(testLib.checkNestedControl(control, config.a.p, config.a.q, config.b))

    def testReadControl(self):
        """Test reading the values from a C++ Control object into a Config object."""
        control = testLib.OuterControlObject()
        control.a.p = 6.0
        control.a.q = 4
        control.b = 3
        config = testLib.OuterConfigObject()
        config.readControl(control)
        self.assertTrue(testLib.checkNestedControl(control, config.a.p, config.a.q, config.b))

    def testDefaults(self):
        """Test that C++ Control object defaults are correctly used as defaults for Config objects."""
        config = testLib.OuterConfigObject()
        control = testLib.OuterControlObject()
        self.assertTrue(testLib.checkNestedControl(control, config.a.p, config.a.q, config.b))

    def testInt64(self):
        """Test that we can wrap C++ Control objects with int64 members."""
        config = testLib.OuterConfigObject()
        control = testLib.OuterControlObject()
        self.assertTrue(testLib.checkNestedControl(control, config.a.p, config.a.q, config.b))
        self.assertGreater(config.a.q, 1 << 30)
        self.assertGreater(control.a.q, 1 << 30)


if __name__ == "__main__":
    unittest.main()
