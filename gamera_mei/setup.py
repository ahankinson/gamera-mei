#!/usr/bin/env python

from distutils.core import setup, Extension
from gamera import gamera_setup

# This constant should be the name of the toolkit
TOOLKIT_NAME = "gamera_mei"

# ----------------------------------------------------------------------------
# You should not usually have to edit anything below, but it is
# implemented here and not in the Gamera core so that you can edit it
# if you need to do something more complicated (for example, building
# and linking to a third- party library).
# ----------------------------------------------------------------------------

PLUGIN_PATH = 'gamera/toolkits/%s/plugins/' % TOOLKIT_NAME
PACKAGE = 'gamera.toolkits.%s' % TOOLKIT_NAME
PLUGIN_PACKAGE = PACKAGE + ".plugins"
plugins = gamera_setup.get_plugin_filenames(PLUGIN_PATH)
plugin_extensions = gamera_setup.generate_plugins(plugins, PLUGIN_PACKAGE)

# This is a standard distutils setup initializer.  If you need to do
# anything more complex here, refer to the Python distutils documentation.
setup(name=TOOLKIT_NAME, version="2.2.0pre2",
      ext_modules = plugin_extensions,
      packages = [PACKAGE, PLUGIN_PACKAGE],
      scripts = ['scripts/gamera_mei'])
