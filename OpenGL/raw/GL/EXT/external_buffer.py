'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_EXT_external_buffer'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_EXT_external_buffer',error_checker=_errors._error_checker)

@_f
@_p.types(None,_cs.GLenum,_cs.GLintptr,_cs.GLsizeiptr,_cs.GLeglClientBufferEXT,_cs.GLbitfield)
def glBufferStorageExternalEXT(target,offset,size,clientBuffer,flags):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLintptr,_cs.GLsizeiptr,_cs.GLeglClientBufferEXT,_cs.GLbitfield)
def glNamedBufferStorageExternalEXT(buffer,offset,size,clientBuffer,flags):pass
