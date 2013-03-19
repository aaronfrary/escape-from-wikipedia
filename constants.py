"""Constants that are used in multiple files. Use `from constants import *'.
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

# TODO: Come up with more STICKY and SLIPPERY words.
# TODO: Come up with more attribute for words, perhaps linking them to a
# scoring system.

WINWIDTH  = 780         # Width of the program's window, in pixels.
WINHEIGHT = 620         # Height in pixels.
HALF_WINWIDTH  = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)

PAGEWIDTH = 5 * HALF_WINWIDTH
HSPACE    = 40
VSPACE    = 75
PARSPACE  = 150
INDENT    = 60
LINE_PADDING = 6

PLAYER_START = (100, 200)
PLAYER_SCALE = 0.75

CAMERASLACK = 80      # How far from the center the player moves before
                      # moving the camera.
G_ACCEL = -0.20          # General strength of gravity.
BASE_SPEED = 1.25        # Horizontal acceleration rate for average creature.
BASE_JUMPSPEED = 6.2     # Vertical speed (not accel) of average creature's jump.
MAX_VELOCITY = 15.0
TIMEOUT = 12            # Time before special opportunities "time out"
NUMBER_JUMPS = 2            # Allow double jumps?
DOUBLE_JUMP_PENALTY = 0.9   # First jump is always best
HLBOOST = 1.5               # Boost for jumping off a hyperlink
FRICTION_FACTOR = 0.85      # Default friction for words (higher is more slippery).
STICKY = 0.0
SLIPPERY = 0.99

STICKY_WORDS = ('sticky', 'stuck', 'glue', 'glued', 'tar', 'tarred', 'web',
'net', 'netted', 'netting', 'trap', 'trapped', 'trapping', 'honey')
SLIPPERY_WORDS = ('ice', 'icy', 'slip', 'slippery', 'slipped', 'oil', 'oily',
'oiled', 'soap', 'soaped', 'soapy', 'grease', 'greased', 'greasy', 'olive',
'greece', 'greek')

BLACK    = (  0,   0,   0)
WHITE    = (255, 255, 255)
GRAY     = (150, 150, 150)
BLUE     = (  0,   0, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 128,   0)
PURPLE   = (128,   0, 128)

# Font flags
REGULAR  = 0
BOLD     = 1
ITALIC   = 2
BOLDITAL = 3

SMALL_FONT_SIZE  = 36
MEDIUM_FONT_SIZE = 48
LARGE_FONT_SIZE  = 92

