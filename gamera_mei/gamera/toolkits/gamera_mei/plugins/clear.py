from gamera.plugin import *

class clear(PluginFunction):
    """Fills the entire image with white."""
    category = "Draw"
    self_type = ImageType([ONEBIT, GREYSCALE, GREY16, FLOAT, RGB])

class ClearModule(PluginModule):
    cpp_headers=["clear.hpp"]
    cpp_namespace=["Gamera"]
    category = "Gamera_mei"
    functions = [clear]
    author = "Your name here"
    url = "Your URL here"
module = ClearModule()
