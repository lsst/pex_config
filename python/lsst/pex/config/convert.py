# This file is part of pex_config.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.

__all__ = ('makePropertySet', 'makePolicy')

from deprecated.sphinx import deprecated

try:
    import lsst.pex.policy as pexPolicy
except ImportError:
    pexPolicy = None

try:
    import lsst.daf.base as dafBase
except ImportError:
    dafBase = None


def makePropertySet(config):
    """Convert a configuration into a `lsst.daf.base.PropertySet`.

    Parameters
    ----------
    config : `lsst.pex.config.Config`
        Configuration instance.

    Returns
    -------
    propertySet : `lsst.daf.base.PropertySet`
        A `~lsst.daf.base.PropertySet` that is equivalent to the ``config``
        instance. If ``config`` is `None` then this return value is also
        `None`.

    See also
    --------
    makePolicy
    lsst.daf.base.PropertySet
    """
    if dafBase is None:
        raise RuntimeError("lsst.daf.base is not available")

    def _helper(ps, prefix, dict_):
        for k, v in dict_.items():
            name = prefix + "." + k if prefix is not None else k
            if isinstance(v, dict):
                _helper(ps, name, v)
            elif v is not None:
                ps.set(name, v)

    if config is not None:
        ps = dafBase.PropertySet()
        _helper(ps, None, config.toDict())
        return ps
    else:
        return None


@deprecated("pex_policy is deprecated, prefer makePropertySet (will be removed after v19)",
            category=FutureWarning)
def makePolicy(config):
    """Convert a configuration into a `lsst.pex.policy.Policy`.

    Parameters
    ----------
    config : `lsst.pex.config.Config`
        Configuration instance.

    Returns
    -------
    policy : `lsst.pex.policy.Policy`
        A `~lsst.pex.policy.Policy` that is equivalent to the ``config``
        instance. If ``config`` is `None` then return value is also `None`.

    See also
    --------
    makePropertySet
    lsst.pex.policy.Policy
    """
    if pexPolicy is None:
        raise RuntimeError("lsst.pex.policy is not available")

    def _helper(dict_):
        p = pexPolicy.Policy()
        for k, v in dict_.items():
            if isinstance(v, dict):
                p.set(k, _helper(v))
            elif isinstance(v, list):
                for vi in v:
                    p.add(k, vi)
            elif v is not None:
                p.set(k, v)
        return p
    if config:
        return _helper(config.toDict())
    else:
        return None
