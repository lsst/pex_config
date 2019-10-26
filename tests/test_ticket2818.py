# This file is part of pex_config.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.

import os
import sys
import io
import unittest

# Extend path to find the helper code for this test relative to the test file
sys.path = [os.path.join(os.path.abspath(os.path.dirname(__file__)), "ticket2818helper")] + sys.path

from ticket2818helper.define import BaseConfig  # noqa E402 module level import not at top of file


class ImportTest(unittest.TestCase):
    def test(self):
        from ticket2818helper.another import AnotherConfigurable  # noqa F401 imported but unused
        config = BaseConfig()
        config.loadFromStream("""from ticket2818helper.another import AnotherConfigurable
config.test.retarget(AnotherConfigurable)
""")
        stream = io.StringIO()
        config.saveToStream(stream)
        values = stream.getvalue()
        print(values)
        self.assertIn("import ticket2818helper.another", values)


if __name__ == "__main__":
    unittest.main()
