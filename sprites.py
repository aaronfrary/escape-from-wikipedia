"""Custom sprite classes built off of rabbyt.sprite.Sprite.
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

import math, pygame, rabbyt, random, os
import glutils
from constants import *

class Counter:
    """Simple counter class. Call objects to retrieve or set value."""
    def __init__(self, startval=0):
        self.val = startval
    def __call__(self, update=None):
        if update is not None:
            self.val = update
        return self.val
    def inc(self):
        self.val += 1
    def dec(self):
        self.val -= 1


class MySprite(rabbyt.sprites.Sprite):
    """rabbyt sprite that always uses OpenGL textures."""
    def __init__(self, texture=None, shape=None, tex_shape=(0,1,1,0)):
        if isinstance(texture, basestring):
            image = pygame.image.load(texture).convert_alpha()
            texture = glutils.getTexture(image)
            shape = [0, image.get_height(), image.get_width(), 0]
        rabbyt.sprites.Sprite.__init__(self, texture=texture, shape=shape,
                          tex_shape=tex_shape)


class Jumper(MySprite):
    """Generic sprite affected by gravity and obstacles. Can move and jump."""
    def __init__(self, speed=1, jumpspeed=1, grav=1,
                 texture=None, shape=None, tex_shape=(0,1,1,0)):
        MySprite.__init__(self, texture=texture, shape=shape,
                          tex_shape=tex_shape)
        self.gaccel = grav * G_ACCEL
        self.jumpspeed = jumpspeed * BASE_JUMPSPEED
        self.plat = None
        self.jumps = 1
        self.max_jumps = 1
        self.speed = speed * BASE_SPEED
        self.goingleft = False
        self.goingright = False
        self.velocity = [0.0, 0.0]

    def update(self):
        assert(not (self.goingleft and self.goingright))
        a = [0.0, 0.0]   # Acceleration.

        if self.plat is None:
            ff = 0.98   # Almost no friction.
            a[1] = self.gaccel
        else:
            ff = self.plat.ff   # Friction factor of surface

        rff = 1 - ff ** 4       # Reverse ff: effect of friction
                                # on acceleration.
        if self.goingleft:
            a[0] = -self.speed * rff
        if self.goingright:
            a[0] = self.speed * rff

        self.velocity[0] *= ff

        self.velocity[0] += a[0]
        self.velocity[1] += a[1]

        if abs(self.velocity[0]) > MAX_VELOCITY:
            self.velocity[0] = math.copysign(MAX_VELOCITY, self.velocity[0])
        if abs(self.velocity[1]) > MAX_VELOCITY:
            self.velocity[1] = math.copysign(MAX_VELOCITY, self.velocity[1])

        self.x += self.velocity[0]
        self.y += self.velocity[1]
        
        # Detect walk off platform
        if self.plat is not None:
            if self.left > self.plat.right or self.right < self.plat.left:
                self.plat = None
                self.jumps += 1

    def jump(self):
        if self.jumps < self.max_jumps:
            js = self.jumpspeed
            if self.plat is not None and self.hl_landed() > 0:
                js *= HLBOOST
            if self.jumps > 0:
                js *= DOUBLE_JUMP_PENALTY
            self.plat = None
            self.jumps += 1
            self.velocity[1] = js


class Player(Jumper):
    """Player-controlled sprite, with afterimage."""
    def __init__(self, pos):
        Jumper.__init__(self, texture=os.path.join('images', 'player.png'))
        self.scale = PLAYER_SCALE
        self.xy = pos
        self.max_jumps = NUMBER_JUMPS
        # Create shadow
        self.shadow = MySprite(os.path.join('images',
            'shadow' + str(random.randrange(4,6)) + ".png"))
        # Create enlarged image
        self.image = MySprite(texture=os.path.join('images', 'player.png'))
        self.image.x = self.attrgetter('x') - 4
        self.image.y = self.attrgetter('y') - 5
        # Set counters
        self.hl_landed = Counter()
        self.counters = [self.hl_landed]

    def update(self):
        self.shadow.xy = self.image.xy
        self.shadow.tex_shape = self.image.tex_shape
        # Decrement counters
        for c in self.counters:
            if c() > 0:
                c.dec()
        Jumper.update(self)

    def render(self):
        self.shadow.render()
        self.image.render()

    def reset(self, page=None):
        if page is None:
            self.xy = PLAYER_START
        else:
            w = random.sample(page.words, 1)[0]
            self.bottom = w.top + 1
            self.x = (w.left + w.right) / 2
        self.velocity = [0.0, 0.0]
        self.plat = None

