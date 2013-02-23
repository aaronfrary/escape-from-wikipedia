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

import sys, random, pygame, rabbyt
from pygame.locals import *
from constants import *
import utils, globalvars
from sprites import Player
from scrape_wiki import Page

# Make sure we can use our .png and other images
assert(pygame.image.get_extended() > 0)

LEFT_KEYS = (K_LEFT, K_a)
RIGHT_KEYS = (K_RIGHT, K_d)
UP_KEYS = (K_UP, K_w)
DOWN_KEYS = (K_DOWN, K_s)
QUIT_KEYS = (K_ESCAPE, )

TIME_FACTOR = 1000.0   # Helps rabbyt read pygame ticks


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
    pygame.display.set_caption('Escape from Wikipedia')
    utils.glEnable(utils.GL_TEXTURE_2D)

    while True:
        runGame()       # Allows restarts

def runGame():
    """Initialize new game."""
    globalvars.camx = 0
    globalvars.camy = 0

    page = Page("http://en.wikipedia.org/wiki/Solariellidae")
    player = Player(PLAYER_START)

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
                elif event.key in DOWN_KEYS and player.plat is not None:
                    # Enter hyperlink
                    if not player.plat.hyperlink == "":
                        print player.plat.hyperlink
                        page = Page(player.plat.hyperlink)
                        player.xy = PLAYER_START
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
        collisions = rabbyt.collisions.aabb_collide_single(player, page.words)
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
        if globalvars.camx - player.x > CAMERASLACK:
            globalvars.camx = player.x + CAMERASLACK
        elif player.x - globalvars.camx > CAMERASLACK:
            globalvars.camx = player.x - CAMERASLACK
        if globalvars.camy - player.y > CAMERASLACK:
            globalvars.camy = player.y + CAMERASLACK
        elif player.y - globalvars.camy > CAMERASLACK:
            globalvars.camy = player.y - CAMERASLACK

        # Draw screen
        rabbyt.clear(WHITE)
        # Need to tell Rabbyt what time it is every frame
        rabbyt.set_time(pygame.time.get_ticks() / TIME_FACTOR)

        rabbyt.render_unsorted(page.words)
        player.render()

        pygame.display.flip()


if __name__ == '__main__':
    main()

