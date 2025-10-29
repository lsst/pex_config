"""Sphinx configuration file for an LSST stack package.

This configuration only affects single-package Sphinx documenation builds.
"""

from documenteer.conf.pipelinespkg import *  # noqa: F403, import *

project = "pex_config"
html_theme_options["logotext"] = project  # noqa: F405, unknown name
html_title = project
html_short_title = project
doxylink = {}
exclude_patterns = ["changes/*"]

# Add pipelines.lsst.io to the intersphinx configuration.
# NOTE: we might want to be more sophisticated about mapping corresponding
# versions of the Pipelines and astro_metadata_translator. This technique will
# mostly work if the Pipelines and astro_metadata_translator are developed
# concurrently.
intersphinx_mapping["lsst"] = ("https://pipelines.lsst.io/v/daily/", None)  # noqa

# As a temporary hack until we move to documenteer 2 delete scipy
# (since it no longer works)
try:
    del intersphinx_mapping["scipy"]  # noqa: F405
except KeyError:
    pass

nitpick_ignore = [
    ("py:obj", "lsst.daf.base.PropertySet"),
    ("py:obj", "lsst.pex.config.Field.doc"),  # Cannot make the doc field property appear in docs.
    ("py:obj", "lsst.pex.config.List"),  # Private class.
    ("py:obj", "RegistryInstanceDict"),  # Private class.
    ("py:class", "lsst.pex.config.dictField.Dict"),
    ("py:class", "lsst.pex.config.listField.List"),
    ("py:class", "ActionTypeVar"),
]
nitpick_ignore_regex = [
    ("py:class", "a set-like.*"),  # collections.abc.Mapping inheritance.
    ("py:class", r"D\[k\] if k .*"),  # collections.abc.Mapping inheritance.
    ("py:class", "an object providing.*"),  # collections.abc.Mapping inheritance.
    ("py:(obj|class)", "lsst.pex.config..*TypeVar"),  # Sphinx does not like TypeVar.
    ("py:obj", "ConfigField.(item|dict)Check"),  # Cannot make the check properties appear in docs.
    ("py:(obj|class)", ".*ConfigInstanceDict"),  # Private class.
]
