#ifndef gamera_mei_fill_white
#define gamera_mei_fill_white

#include "gamera.hpp"

namespace Gamera {

  /* This is a very simple plugin that simply fills the image with white

     See the Gamera plugin documentation for more information on how to
     write Gamera plugins.
   */
  template<class T>
  void clear(T& image) {
    std::fill(image.vec_begin(), image.vec_end(), white(image));
  }
}

#endif
