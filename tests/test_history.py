# This file is part of pex_config.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.

import unittest
import lsst.pex.config as pexConfig
import lsst.pex.config.history as pexConfigHistory


class PexTestConfig(pexConfig.Config):
    a = pexConfig.Field('Parameter A', float, default=1.0)


class HistoryTest(unittest.TestCase):
    def testHistory(self):
        b = PexTestConfig()
        b.update(a=4.0)
        pexConfigHistory.Color.colorize(False)
        output = b.formatHistory("a", writeSourceLine=False)

        # The history differs depending on how the tests are executed and might
        # depend on pytest internals. We therefore test the output for the presence
        # of strings that we know should be there.

        # For reference, this is the output from running with unittest.main()
        """a
1.0 unittest.main()
    self.runTests()
    self.result = testRunner.run(self.test)
    test(result)
    return self.run(*args, **kwds)
    test(result)
    return self.run(*args, **kwds)
    testMethod()
    b = PexTestConfig()
    a = pexConfig.Field('Parameter A', float, default=1.0)
4.0 unittest.main()
    self.runTests()
    self.result = testRunner.run(self.test)
    test(result)
    return self.run(*args, **kwds)
    test(result)
    return self.run(*args, **kwds)
    testMethod()
    b.update(a=4.0)"""

        self.assertTrue(output.startswith("a\n1.0"))
        self.assertIn("""return self.run(*args, **kwds)
    testMethod()
    b = PexTestConfig()
    a = pexConfig.Field('Parameter A', float, default=1.0)
4.0""", output)

        self.assertIn("""    return self.run(*args, **kwds)
    testMethod()
    b.update(a=4.0)""", output)


if __name__ == "__main__":
    unittest.main()
