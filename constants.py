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
# Some constants that are used in multiple parts of the program

WINWIDTH = 780         # Width of the program's window, in pixels.
WINHEIGHT = 620         # Height in pixels.
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)

PAGEWIDTH = 5 * HALF_WINWIDTH
HSPACE = 40
VSPACE = 80
PARSPACE = 150
INDENT = 60

PLAYER_START = (100, 200)
PLAYER_SCALE = 0.75

CAMERASLACK = 80      # How far from the center the player moves before
                      # moving the camera.
G_ACCEL = -1.25          # General strength of gravity.
BASE_SPEED = 3.7         # Horizontal acceleration rate for average creature.
BASE_JUMPSPEED = 17.0    # Vertical speed (not accel) of average creature's jump.
MAX_VELOCITY = 22.0
FRICTION_FACTOR = 0.75      # Default friction for words (higher is more slippery).
HL_FRICTION_FACTOR = 0.92   # Friction for hyperlinks
NUMBER_JUMPS = 2            # Allow double jumps?

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

SMALL_FONT_SIZE = 36
MEDIUM_FONT_SIZE = 48
LARGE_FONT_SIZE = 92

