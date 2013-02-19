
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

def unitVec(start, end):
    """Helper function, return unit vector between two points."""
    x0, y0 = start
    x1, y1 = end
    x = x1 - x0
    y = y1 - y0
    norm = math.sqrt(x ** 2 + y ** 2)
    return (x / norm, y / norm)

def getTexture(surf):
    """Helper function, create texture to display `text' and return id."""
    # Open unused texture id
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    # Take pixel data in byte order
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    # Ensure sane defaults are set for parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    # Ignore lighting and effects
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    # Upload image data to texture
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, surf.get_width(),
            surf.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE,
            pygame.image.tostring(surf, "RGBA", 1))
    return tex_id

