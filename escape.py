#!/usr/bin/env python
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
# This version uses pygame and rabbyt, which works great, except that rabbyt
# sprites only take image files or GL texture ids, so for our word sprites
# we make rabbyt sprites without images and use pygame to paint their images
# onto one static background.


import sys, math, random, pygame, rabbyt
from pygame.locals import *

# Make sure we can use our .png and other images
assert(pygame.image.get_extended() > 0)

LEFT_KEYS = (K_LEFT, K_a)
RIGHT_KEYS = (K_RIGHT, K_d)
UP_KEYS = (K_UP, K_w)
DOWN_KEYS = (K_DOWN, K_s)
QUIT_KEYS = (K_ESCAPE, )

TIME_FACTOR = 1000.0   # Helps rabbyt read pygame ticks
WINWIDTH = 640         # Width of the program's window, in pixels.
WINHEIGHT = 480        # Height in pixels.
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)

PAGEWIDTH = 4 * WINWIDTH
PAGEHEIGHT = 8 * WINHEIGHT # won't be necessary once we actually scrape text

BLACK    = (  0,   0,   0)
WHITE    = (255, 255, 255)
BLUE     = (  0,   0, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 128,   0)
PURPLE   = (128,   0, 128)

# Font flags
REGULAR = 0
BOLD = 1
ITALIC = 2
BOLDITAL = 3

SMALL_FONT_SIZE = 20
MEDIUM_FONT_SIZE = 42
LARGE_FONT_SIZE = 48

CAMERASLACK = 80       # How far from the center the player moves before
                       # moving the camera.
G_ACCEL = -0.1         # General strength of gravity.
BASE_SPEED = 0.45      # Horizontal acceleration rate for average creature.
BASE_JUMPSPEED = 5     # Vertical speed (not accel) of average creature's jump.
#GRAPPLE_TIME = 0.1       # Inverse speed of grappling hook: how long it takes
                       # to move 1 unit.

MAXHEALTH = 3          # How much health the player starts with.

def unit_vec(start, end):
    """Helper function, return unit vector between two points."""
    x0, y0 = start
    x1, y1 = end
    x = x1 - x0
    y = y1 - y0
    norm = math.sqrt(x ** 2 + y ** 2)
    return (x / norm, y / norm)

def font_check(attr):
    if Word.WIKIFONT[attr] == None:
        if attr == REGULAR:
            Word.WIKI_REGULAR = [pygame.font.Font("fonts/arial.ttf",
                                                  SMALL_FONT_SIZE),
                                 pygame.font.Font("fonts/arial.ttf",
                                                  MEDIUM_FONT_SIZE),
                                 pygame.font.Font("fonts/arial.ttf",
                                                  LARGE_FONT_SIZE)]
        elif attr == BOLD:
            Word.WIKI_BOLD = [pygame.font.Font("fonts/arialbd.ttf",
                                               SMALL_FONT_SIZE),
                              pygame.font.Font("fonts/arialbd.ttf",
                                               MEDIUM_FONT_SIZE),
                              pygame.font.Font("fonts/arialbd.ttf",
                                               LARGE_FONT_SIZE)]
        elif attr == ITALIC:
            Word.WIKI_ITALIC = [pygame.font.Font("fonts/ariali.ttf",
                                                 SMALL_FONT_SIZE),
                                pygame.font.Font("fonts/ariali.ttf",
                                                 MEDIUM_FONT_SIZE),
                                pygame.font.Font("fonts/ariali.ttf",
                                                 LARGE_FONT_SIZE)]
        elif attr == BOLDITAL:
            Word.WIKI_BOLDITAL = [pygame.font.Font("fonts/arialbi.ttf",
                                                   SMALL_FONT_SIZE),
                                  pygame.font.Font("fonts/arialbi.ttf",
                                                   MEDIUM_FONT_SIZE),
                                  pygame.font.Font("fonts/arialbi.ttf",
                                                   LARGE_FONT_SIZE)]
        Word.WIKIFONT = {REGULAR : Word.WIKI_REGULAR,
                         BOLD : Word.WIKI_BOLD,
                         ITALIC : Word.WIKI_ITALIC,
                         BOLDITAL : Word.WIKI_BOLDITAL}


class MySprite(rabbyt.sprites.Sprite):
    def render(self):
        #TODO: reimplement transforming OpenGL modelview matrix directly.
        global camerax, cameray
        self.x -= camerax
        self.y -= cameray
        rabbyt.sprites.Sprite.render(self)
        self.x += camerax
        self.y += cameray


class Page:
    def __init__(self, url):
        self.url = url
        #TODO: Finish


class Word(MySprite):
    """Words are static obstacles generally used as platforms, except
    those that are hyperlinks, which can be also be "followed".

    Constructors:
        'text' : The character string of the Word.
        'pos'  : The starting position (in the page coordinate system)
                 of the bottom-left corner.
        'attr' : 'bold', 'italic', 'bold-italic', or "" for regular.
        'size' : 0 for small font, 1 for medium, or 2 for large.
        'link' : Address of hyperlink, if any.
    """
    WIKI_REGULAR = None
    WIKI_BOLD = None
    WIKI_ITALIC = None
    WIKI_BOLDITAL = None
    # Font dictionary WIKIFONT: for font size 'sz' in (0,1,2) with attribute
    # 'attr', usage is: 'WIKIFONT[attr][sz]'
    WIKIFONT = {REGULAR : WIKI_REGULAR, BOLD : WIKI_BOLD, ITALIC : WIKI_ITALIC,
            BOLDITAL : WIKI_BOLDITAL}

    def __init__(self, text, page, pos, attr=REGULAR, size = 0, link=""):
        font_check(attr)
        self.ff = 0.9
        self.text = text
        self.hyperlink = link
        if link == "": color = BLACK
        else: color = BLUE
        image = Word.WIKIFONT[attr][size].render(text, True, color)
        rect = self.image.get_rect(bottomleft=pos)
        # Initialize blank sprite with correct shape
        MySprite.__init__(shape=(rect.left, rect.top, rect.right, rect.bottom))
        # Paste image to background
        page.surf.blit(image, rect)


    def is_link(self):
        return not (self.hyperlink == "")


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

        rff = 1 - ff ** 4   # Reverse ff: effect of friction
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
        Jumper.__init__(self, texture="images/player.png")
        self.xy = pos



def terminate():
    """Quit and clean up"""
    pygame.quit()
    sys.exit()

def main():
    """Start and setup"""
    pygame.init()
    pygame.display.set_mode( (WINWIDTH, WINHEIGHT),
                             pygame.OPENGL | pygame.DOUBLEBUF )
    # (0,0) is center point of screen
    rabbyt.set_viewport( (WINWIDTH, WINHEIGHT) )
    rabbyt.set_default_attribs()
    #pygame.display.set_icon(pygame.image.load("images.gameicon.png"))
    pygame.display.set_caption('<ENTER TITLE HERE>')
    gl.glEnable(GL_TEXTURE_2D)

    while True:
        runGame()       # Allows restarts

def runGame():
    """Initialize new game."""
    global camerax, cameray
    camerax = 0
    cameray = 0

    platforms = []      # Stores all platforms (static, solid objects)
    monsters = []       # Stores all monsters (mobile, harmful objects)

    for i in range(144):
        plat = MySprite("images/platform1.png")
        plat.xy = (random.randint(-2 * WINWIDTH, 2 * WINWIDTH),
                   random.randint(-2 * WINHEIGHT, 2 * WINHEIGHT))
        plat.ff = 0.9
        platforms.append(plat)

    player = Player((0,0))

    # Main loop
    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key in QUIT_KEYS:
                    terminate()
                elif event.key in LEFT_KEYS:
                    player.goingLeft = True
                    player.goingRight = False
                elif event.key in RIGHT_KEYS:
                    player.goingRight = True
                    player.goingLeft = False
                elif event.key in UP_KEYS:
                    player.jump()
            elif event.type == KEYUP:
                if event.key in LEFT_KEYS:
                    player.goingLeft = False
                elif event.key in RIGHT_KEYS:
                    player.goingRight = False
                elif event.key in UP_KEYS:
                    player.jumpStop()

        # Update positions
        player.update()

        # Check for player-platform collisions
        collisions = rabbyt.collisions.aabb_collide_single(player, platforms)
        # Player forced out of platforms by most direct route, more or less;
        # by checking platform top first, player gains "stair climbing"
        # ability for stairs up to 1/3 player height.
        for plat in collisions:
            if (2 * player.bottom / 3 + player.top / 3 > plat.top
            and player.velocity[1] < 0):
                player.bottom = plat.top + 1
                player.plat = plat
            elif (2 * player.right / 3 + player.left / 3 < plat.left
            and player.velocity[0] > 0):
                player.right = plat.left - 1
            elif (2 * player.left / 3 + player.right / 3 > plat.right
            and player.velocity[0] < 0):
                player.left = plat.right + 1
            elif (2 * player.top / 3 + player.bottom / 3 < plat.bottom
            and player.velocity[1] > 0):
                player.top = plat.bottom - 1

        # adjust camerax and cameray if beyond the "camera slack"
        # TODO: Reimplement using Anims
        if camerax - player.x > CAMERASLACK:
            camerax = player.x + CAMERASLACK
        elif player.x - camerax > CAMERASLACK:
            camerax = player.x - CAMERASLACK
        if cameray - player.y > CAMERASLACK:
            cameray = player.y + CAMERASLACK
        elif player.y - cameray > CAMERASLACK:
            cameray = player.y - CAMERASLACK

        # Draw screen TODO: blit page instead
        rabbyt.clear(WHITE)
        # Need to tell Rabbyt what time it is every frame
        rabbyt.set_time(pygame.time.get_ticks() / TIME_FACTOR)

        rabbyt.render_unsorted(platforms)
        player.render()

        pygame.display.flip()


if __name__ == '__main__':
    main()
