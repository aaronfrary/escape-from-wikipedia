"""Copyright 2013 Aaron Graham-Horowitz

This file is part of Escape from Wikipedia.

Escape from Wikipedia is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or any later version.

Escape from Wikipedia is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import math, pygame, rabbyt
import utils
from constants import *


class MySprite(rabbyt.sprites.Sprite):
    def __init__(self, texture=None, shape=None, tex_shape=(0,1,1,0)):
        if isinstance(texture, basestring):
            image = pygame.image.load(texture)
            texture = utils.getTexture(image)
            shape = [0, image.get_height(), image.get_width(), 0]
        rabbyt.sprites.Sprite.__init__(self, texture=texture, shape=shape,
                          tex_shape=tex_shape)


class Jumper(MySprite):
    def __init__(self, speed=1, jumpSpeed=1, grav=1,
                 texture=None, shape=None, tex_shape=(0,1,1,0)):
        MySprite.__init__(self, texture=texture, shape=shape,
                          tex_shape=tex_shape)
        self.gaccel = grav * G_ACCEL
        self.jumpSpeed = jumpSpeed * BASE_JUMPSPEED
        self.plat = None
        self.speed = speed * BASE_SPEED
        self.goingLeft = False
        self.goingRight = False
        self.velocity = [0.0, 0.0]

    def update(self):
        assert(not (self.goingLeft and self.goingRight))
        a = [0.0, 0.0]   # Acceleration.

        if self.plat is None:
            ff = 1   # No friction.
            a[1] = self.gaccel
        else:
            ff = self.plat.ff   # Friction factor of surface

        rff = 1 - ff ** 4       # Reverse ff: effect of friction
                                # on acceleration.
        if self.goingLeft:
            a[0] = -self.speed * rff
        if self.goingRight:
            a[0] = self.speed * rff

        self.velocity[0] *= ff
        self.velocity[1] *= ff

        self.velocity[0] += a[0]
        self.velocity[1] += a[1]

        self.x += self.velocity[0]
        self.y += self.velocity[1]
        
        # Detect walk off platform
        if self.plat is not None:
            if self.left > self.plat.right or self.right < self.plat.left:
                self.plat = None

    def jump(self):
        if self.plat is not None:
            self.plat = None
            self.velocity[1] += self.jumpSpeed

    def jumpStop(self):
        pass


class Player(Jumper):
    def __init__(self, pos):
        Jumper.__init__(self, texture="images\\player.png")
        self.scale = PLAYER_SCALE
        self.xy = pos

