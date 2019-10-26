# This file is part of pex_config.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.

from _testLib import *
import lsst.pex.config
import sys
module = sys.modules[__name__]
InnerConfigObject = lsst.pex.config.makeConfigClass(InnerControlObject, module=module)
OuterConfigObject = lsst.pex.config.makeConfigClass(OuterControlObject, module=module)
ConfigObject = lsst.pex.config.makeConfigClass(ControlObject, module=module)
