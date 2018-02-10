# pylint: disable=W,C,R
#!/usr/bin/env python
from __future__ import print_function

from ctypes import *

lib = CDLL('libxcb.so.1')
