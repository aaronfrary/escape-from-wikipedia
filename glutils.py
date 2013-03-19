"""Helper functions and wrappers into OpenGL.
"""
# Copyright 2013 Aaron Graham-Horowitz
# 
# This file is part of Escape from Wikipedia.
# 
# Escape from Wikipedia is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or any later version.
# 
# Escape from Wikipedia is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
# 
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

import pygame
from OpenGL.GL import *
from ctypes import *
from constants import *

def getTexture(surf):
    """Helper function, create texture to display `text' and return id."""
    # Open unused texture id
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    # Take pixel data in byte order
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    # Ensure sane defaults are set for parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    # Upload image data to texture
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, surf.get_width(),
            surf.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE,
            pygame.image.tostring(surf, "RGBA", 1))
    return tex_id

def scroll(x, y):
    """Wrapper for glTranslatef, in 2-D with reversed coordinates."""
    glTranslatef(-x, -y, 0)

