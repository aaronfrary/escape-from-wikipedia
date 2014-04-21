"""Functions and classes for generating `Word' and `Page' objects from the web.

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

import pygame, os, re, wikipedia, math, glutils
from sprites import MySprite
from constants import *
# lxml is not necessary, as parsing is not currently a bottleneck.
# XXX are we sure?
#import lxml

def fontCheck(attr):
    """Load font files only when needed, and only once each."""
    if Word.WIKIFONT[attr] == None:
        if attr == REGULAR:
            Word.WIKI_REGULAR = [pygame.font.Font(os.path.join('fonts', 'arial.ttf'),
                                                  SMALL_FONT_SIZE),
                                 pygame.font.Font(os.path.join('fonts', 'arial.ttf'),
                                                  MEDIUM_FONT_SIZE),
                                 pygame.font.Font(os.path.join('fonts', 'arial.ttf'),
                                                  LARGE_FONT_SIZE)]
        elif attr == BOLD:
            Word.WIKI_BOLD = [pygame.font.Font(os.path.join('fonts', 'arialbd.ttf'),
                                               SMALL_FONT_SIZE),
                              pygame.font.Font(os.path.join('fonts', 'arialbd.ttf'),
                                               MEDIUM_FONT_SIZE),
                              pygame.font.Font(os.path.join('fonts', 'arialbd.ttf'),
                                               LARGE_FONT_SIZE)]
        elif attr == ITALIC:
            Word.WIKI_ITALIC = [pygame.font.Font(os.path.join('fonts', 'ariali.ttf'),
                                                 SMALL_FONT_SIZE),
                                pygame.font.Font(os.path.join('fonts', 'ariali.ttf'),
                                                 MEDIUM_FONT_SIZE),
                                pygame.font.Font(os.path.join('fonts', 'ariali.ttf'),
                                                 LARGE_FONT_SIZE)]
        elif attr == BOLDITAL:
            Word.WIKI_BOLDITAL = [pygame.font.Font(os.path.join('fonts', 'arialbi.ttf'),
                                                   SMALL_FONT_SIZE),
                                  pygame.font.Font(os.path.join('fonts', 'arialbi.ttf'),
                                                   MEDIUM_FONT_SIZE),
                                  pygame.font.Font(os.path.join('fonts', 'arialbi.ttf'),
                                                   LARGE_FONT_SIZE)]
        Word.WIKIFONT = {REGULAR : Word.WIKI_REGULAR,
                         BOLD : Word.WIKI_BOLD,
                         ITALIC : Word.WIKI_ITALIC,
                         BOLDITAL : Word.WIKI_BOLDITAL}



class Line(MySprite):
    """Sprite for horizontal line across width of screen."""
    def __init__(self, y):
        MySprite.__init__(self, texture=os.path.join('images', 'graypxl.png'))
        self.top = y
        self.left = 0
        self.scale_x = PAGEWIDTH


class Word(MySprite):
    """Static sprites used as platforms and that may have followable hyperlinks.

    Constructors:
        'text'   : The character string of the Word.
        'pos'    : The starting position of the bottom-left corner.
        'attr'   : 'bold', 'italic', 'bold-italic', or "" for regular.
        'size'   : 0 for small font, 1 for medium, or 2 for large.
        'link'   : Address of hyperlink, if any.
        'color'  : Overrides plain text color.
        'hlcolor : Overrides hyperlink color.
    """
    WIKI_REGULAR = None
    WIKI_BOLD = None
    WIKI_ITALIC = None
    WIKI_BOLDITAL = None
    # Font dictionary WIKIFONT: for font size 'sz' in (0,1,2) with attribute
    # 'attr', usage is: 'WIKIFONT[attr][sz]'
    WIKIFONT = {REGULAR : WIKI_REGULAR, BOLD : WIKI_BOLD, ITALIC : WIKI_ITALIC,
            BOLDITAL : WIKI_BOLDITAL}

    def __init__(self, text, pos, attr=REGULAR, size=0, link="", color=BLACK, hlcolor=BLUE):
        fontCheck(attr)
        self.text = text
        self.hyperlink = link
        if not link == "":
            color = hlcolor
        self.ff = FRICTION_FACTOR
        if text.lower() in STICKY_WORDS or (
                text.lower() + 's') in STICKY_WORDS:
            self.ff = STICKY
        if text.lower() in SLIPPERY_WORDS or (
                text.lower() + 's') in SLIPPERY_WORDS:
            self.ff = SLIPPERY
        image = Word.WIKIFONT[attr][size].render(text, True, color)
        # Initialize sprite
        left, bottom = pos
        right = left + image.get_width()
        top = bottom + image.get_height()
        MySprite.__init__(self, texture=glutils.getTexture(image),
                shape=[left, top, right, bottom])

    def isLink(self):
        return not (self.hyperlink == "")


class Page:
    """Represents a Wikipedia page as a title and a collection of Words.
    
    The `segments' attribute divides the list of words into managable chunks,
    so that the main loop can choose to display only words near the player's
    location.
    """
    def __init__(self, title):
        wikipage = wikipedia.page(title)
        self.links = wikipage.links
        link_matcher = re.compile("|".join(self.links), re.IGNORECASE)
        def linkMarker(match):
            s = match.group(0)
            # End with two delimeters to mark "no link"
            return (" " + LINK_DELIM + s.replace(" ", "_") + LINK_DELIM
                    + " " + s + " " + LINK_DELIM + LINK_DELIM + " ")
        self.title = title
        self.wc = 0 # Wordcount
        self.words = []
        self.segments = [0]
        # Variables used only in initialization
        self._y = 0
        self._segment_y = -HALF_WINHEIGHT
        self._link = ""
        # Helper function (apologies for the abuse of scoping)
        def strToWords(s, attr=REGULAR, size=0, color=BLACK, hlcolor=BLUE):
            """Return string of words as `Word's, with correct locations."""
            if s is None:
                return
            x = 0
            for word in s.split():
                if len(word) < 1:
                    continue
                if word[0] == LINK_DELIM:
                    self._link = word[1:-1].replace("_", " ")
                    print self._link
                    continue
                # Punctuation is sometimes treated as a separate word
                if not word[0] in PUNCTUATION:
                    x += HSPACE * math.sqrt(size + 1)
                w = Word(word, (x, self._y), attr, size, self._link, color, hlcolor)
                # Place word
                if w.right >= PAGEWIDTH:
                    w.left = 0
                    w.y -= (w.top - w.bottom) + VSPACE
                x = w.right
                self._y = w.bottom
                # Segmenting
                if self._segment_y - self._y > WINHEIGHT:
                    self.segments.append(self.wc)
                    self._segment_y -= WINHEIGHT
                self.words.append(w)
                self.wc += 1

        # BEGIN INITIALIZATION
        # Title line
        strToWords(title, size=2)
        lines = [self._y - LINE_PADDING]
        self._y -= VSPACE
        strToWords("From Wikipedia, the free encyclopedia", color=GRAY)
        self._y -= PARSPACE
        # Sections
        for section in wikipage.sections:
            text = link_matcher.sub( linkMarker, wikipage.section(section) )
            # Section header
            strToWords(section, size=1)
            lines.append(self._y - LINE_PADDING)
            self._y -= VSPACE
            # Section body
            strToWords(text)
            self._y -= PARSPACE
        # Finalize state
        self.lines = [Line(y) for y in lines]
        self.lines[0].scale_y = 2   # bar under title
        self.visible_words = self.words[:self.segments[1]]


