# This file is part of pex_config.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.

import unittest
import lsst.pex.config


class TicketDM7337Test(unittest.TestCase):

    def testStrChoice(self):
        """Test that ChoiceField converts "str" types to be compatible
        with string literals.
        """
        choices = lsst.pex.config.ChoiceField(
            doc="A description",
            dtype=str,
            allowed={
                'measure': 'Measure clipped mean and variance from the whole image',
                'meta': 'Mean = 0, variance = the "BGMEAN" metadata entry',
                'variance': "Mean = 0, variance = the image's variance",
            },
            default='measure', optional=False
        )
        self.assertIsInstance(choices, lsst.pex.config.ChoiceField)


if __name__ == "__main__":
    unittest.main()
