"""
Toolkit setup

This file is run on importing anything within this directory.
Its purpose is only to help with the Gamera GUI shell,
and may be omitted if you are not concerned with that.
"""

from gamera import toolkit
import wx
from gamera.toolkits.gamera_mei import main


# Let's import all our plugins here so that when this toolkit
# is imported using the "Toolkit" menu in the Gamera GUI
# everything works.

# from gamera.toolkits.gamera_mei.plugins import clear

# You can inherit from toolkit.CustomMenu to create a menu
# for your toolkit.  Create a list of menu option in the
# member _items, and a series of callback functions that
# correspond to them.  The name of the callback function
# should be the same as the menu item, prefixed by '_On'
# and with all spaces converted to underscores.
# class Gamera_meiMenu(toolkit.CustomMenu):
#     _items = ["Gamera_mei Toolkit",
#               "Gamera_mei Toolkit 2"]
#     def _OnGamera_mei_Toolkit(self, event):
#         wx.MessageDialog(None, "You clicked on Gamera_mei Toolkit!").ShowModal()
#         main.main()
#     def _OnGamera_mei_Toolkit_2(self, event):
#         wx.MessageDialog(None, "You clicked on Gamera_mei Toolkit 2!").ShowModal()
#         main.main()
# gamera_mei_menu = Gamera_meiMenu()

# [staff_number, c.offset_x, c.offset_y, note, line_number, 
#   glyph_kind, actual_glyph, glyph_char, uod, c.ncols, c.nrows]
#
# [1, 18, 142, '', 3, 'clef', 'c', [''], '', 14, 40]
# [1, 612, 203, 'F', 7, 'neume', 'virga', [''], 'D', 13, 44]
#