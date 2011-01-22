
        
    
  #include "gameramodule.hpp"
  #include "knnmodule.hpp"

        #include "clear.hpp"
  
    #include <string>
  #include <stdexcept>
  #include "Python.h"
  #include <list>

  using namespace Gamera;
  
        
      extern "C" {
#ifndef _MSC_VER
    void init_clear(void);
#endif
                  static PyObject* call_clear(PyObject* self, PyObject* args);
            }

          static PyMethodDef _clear_methods[] = {
                  { CHAR_PTR_CAST "clear",
          call_clear, METH_VARARGS,
          CHAR_PTR_CAST "**clear** ()\n\nFills the entire image with white."        },
              { NULL }
  };

                static PyObject* call_clear(PyObject* self, PyObject* args) {
            
      PyErr_Clear();
                                                                          Image* self_arg;
PyObject* self_pyarg;
      
                                      if (PyArg_ParseTuple(args, CHAR_PTR_CAST "O:clear"
                        ,
             &self_pyarg                      ) <= 0)
           return 0;
               
              if (!is_ImageObject(self_pyarg)) {
          PyErr_SetString(PyExc_TypeError, "Argument 'self' must be an image");
          return 0;
        }
        self_arg = ((Image*)((RectObject*)self_pyarg)->m_x);
        image_get_fv(self_pyarg, &self_arg->features, &self_arg->features_len);
              
              try {
                      switch(get_image_combination(self_pyarg)) {
case ONEBITIMAGEVIEW:
clear(*((OneBitImageView*)self_arg));
break;
case CC:
clear(*((Cc*)self_arg));
break;
case ONEBITRLEIMAGEVIEW:
clear(*((OneBitRleImageView*)self_arg));
break;
case RLECC:
clear(*((RleCc*)self_arg));
break;
case MLCC:
clear(*((MlCc*)self_arg));
break;
case GREYSCALEIMAGEVIEW:
clear(*((GreyScaleImageView*)self_arg));
break;
case GREY16IMAGEVIEW:
clear(*((Grey16ImageView*)self_arg));
break;
case RGBIMAGEVIEW:
clear(*((RGBImageView*)self_arg));
break;
case FLOATIMAGEVIEW:
clear(*((FloatImageView*)self_arg));
break;
default:
PyErr_Format(PyExc_TypeError,"The 'self' argument of 'clear' can not have pixel type '%s'. Acceptable values are ONEBIT, ONEBIT, ONEBIT, ONEBIT, ONEBIT, GREYSCALE, GREY16, RGB, and FLOAT.", get_pixel_type_name(self_pyarg));
return 0;
}
                  } catch (std::exception& e) {
          PyErr_SetString(PyExc_RuntimeError, e.what());
          return 0;
        }
      
                                Py_INCREF(Py_None);
          return Py_None;
                    }
      
  DL_EXPORT(void) init_clear(void) {
    Py_InitModule(CHAR_PTR_CAST "_clear", _clear_methods);
  }
  

