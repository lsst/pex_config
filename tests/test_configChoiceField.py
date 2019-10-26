# This file is part of pex_config.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.

import os
import unittest
import lsst.pex.config as pexConfig


class Config1(pexConfig.Config):
    f = pexConfig.Field(doc="Config1.f", dtype=int, default=4)

    def validate(self):
        pexConfig.Config.validate(self)
        if self.f <= 0:
            raise pexConfig.FieldValidationError(Config1.f, self, "f should be > 0")


class Config2(pexConfig.Config):
    f = pexConfig.Field(doc="Config2.f", dtype=float, default=0.5, check=lambda x: x > 0)


TYPEMAP = {"AAA": Config1, "BBB": Config2, "CCC": Config1}


class Config3(pexConfig.Config):
    a = pexConfig.ConfigChoiceField(doc="single non-optional",
                                    typemap=TYPEMAP,
                                    default="AAA", multi=False, optional=False)
    b = pexConfig.ConfigChoiceField(doc="single optional",
                                    typemap=TYPEMAP,
                                    default="AAA", multi=False, optional=True)
    c = pexConfig.ConfigChoiceField(doc="multi non-optional",
                                    typemap=TYPEMAP,
                                    default=["AAA"], multi=True, optional=False)
    d = pexConfig.ConfigChoiceField(doc="multi optional",
                                    typemap=TYPEMAP,
                                    default=["AAA"], multi=True, optional=True)


class ConfigChoiceFieldTest(unittest.TestCase):
    def setUp(self):
        self.config = Config3()

    def tearDown(self):
        del self.config

    def testInit(self):
        self.assertEqual(self.config.a.name, "AAA")
        self.assertEqual(self.config.a.active.f, 4)
        self.assertEqual(self.config.a["AAA"].f, 4)
        self.assertEqual(self.config.a["BBB"].f, 0.5)

    def testSave(self):
        self.config.a["AAA"].f = 1
        self.config.a["BBB"].f = 1.0
        self.config.a = "BBB"
        path = "choiceFieldTest.config"
        self.config.save(path)
        roundtrip = Config3()
        roundtrip.load(path)
        os.remove(path)

        self.assertEqual(self.config.a.name, roundtrip.a.name)
        self.assertEqual(self.config.a["AAA"].f, roundtrip.a["AAA"].f)
        self.assertEqual(self.config.a["BBB"].f, roundtrip.a["BBB"].f)

    def testValidate(self):
        self.config.validate()
        self.config.a = "AAA"
        self.config.a["AAA"].f = 0

        self.assertRaises(pexConfig.FieldValidationError, self.config.validate)

        self.config.a = "BBB"
        self.config.validate()

        self.config.a = None
        self.assertRaises(pexConfig.FieldValidationError, self.config.validate)

    def testFreeze(self):
        self.config.freeze()
        self.assertRaises(pexConfig.FieldValidationError, setattr, self.config.a, "name", "AAA")
        self.assertRaises(pexConfig.FieldValidationError, setattr, self.config.a["AAA"], "f", "1")

    def testNoArbitraryAttributes(self):
        self.assertRaises(pexConfig.FieldValidationError, setattr, self.config.a, "should", "fail")

    def testSelectionSet(self):
        # test in place modification
        self.config.c.names.add("BBB")
        self.assertEqual(set(self.config.c.names), set(["AAA", "BBB"]))
        self.config.c.names.remove("AAA")
        self.assertEqual(set(self.config.c.names), set(["BBB"]))
        self.assertRaises(KeyError, self.config.c.names.remove, "AAA")
        self.config.c.names.discard("AAA")

        # test bad assignment
        self.assertRaises(pexConfig.FieldValidationError,
                          setattr, self.config.c, "names", "AAA")
        self.config.c.names = ["AAA"]

    def testNoneValue(self):
        self.config.a = None
        self.assertRaises(pexConfig.FieldValidationError, self.config.validate)
        self.config.a = "AAA"
        self.config.b = None
        self.config.validate()
        self.config.c = None
        self.assertRaises(pexConfig.FieldValidationError, self.config.validate)
        self.config.c = ["AAA"]
        self.config.d = None
        self.config.validate()


if __name__ == "__main__":
    unittest.main()
