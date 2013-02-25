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

import urllib2, bs4, re, pygame
import utils
from sprites import MySprite
from constants import *
#import lxml

TEXT_CROPX = -2
TEXT_CROPY = -3

BULLET = 0x2022   # Unicode character

HTML404 = """<HTML><HEAD><TITLE>ERROR: The requested URL could not be retrieved</TITLE> </HEAD> <BODY><H2>ERROR</H2> <H2>The requested URL could not be retrieved</H2> <P>While trying to retrieve the URL:<A HREF="{0}">{0}</A> </P> <P>The following error was encountered: <STRONG>Connection to Wikipedia Failed</STRONG> </P> <P>The system returned: <I>(101) Network is unreachable</I> </P> <P>The remote host or network may be down.  Please try the request again.</P> <P>Your cache administrator is DEAD.</P> </BODY> </HTML>"""

def fontCheck(attr):
    if Word.WIKIFONT[attr] == None:
        if attr == REGULAR:
            Word.WIKI_REGULAR = [pygame.font.Font("fonts\\arial.ttf",
                                                  SMALL_FONT_SIZE),
                                 pygame.font.Font("fonts\\arial.ttf",
                                                  MEDIUM_FONT_SIZE),
                                 pygame.font.Font("fonts\\arial.ttf",
                                                  LARGE_FONT_SIZE)]
        elif attr == BOLD:
            Word.WIKI_BOLD = [pygame.font.Font("fonts\\arialbd.ttf",
                                               SMALL_FONT_SIZE),
                              pygame.font.Font("fonts\\arialbd.ttf",
                                               MEDIUM_FONT_SIZE),
                              pygame.font.Font("fonts\\arialbd.ttf",
                                               LARGE_FONT_SIZE)]
        elif attr == ITALIC:
            Word.WIKI_ITALIC = [pygame.font.Font("fonts\\ariali.ttf",
                                                 SMALL_FONT_SIZE),
                                pygame.font.Font("fonts\\ariali.ttf",
                                                 MEDIUM_FONT_SIZE),
                                pygame.font.Font("fonts\\ariali.ttf",
                                                 LARGE_FONT_SIZE)]
        elif attr == BOLDITAL:
            Word.WIKI_BOLDITAL = [pygame.font.Font("fonts\\arialbi.ttf",
                                                   SMALL_FONT_SIZE),
                                  pygame.font.Font("fonts\\arialbi.ttf",
                                                   MEDIUM_FONT_SIZE),
                                  pygame.font.Font("fonts\\arialbi.ttf",
                                                   LARGE_FONT_SIZE)]
        Word.WIKIFONT = {REGULAR : Word.WIKI_REGULAR,
                         BOLD : Word.WIKI_BOLD,
                         ITALIC : Word.WIKI_ITALIC,
                         BOLDITAL : Word.WIKI_BOLDITAL}

def getHTML(addr):
    """Return html for webpage 'addr', or error page on failed connection."""
    try:
        req = urllib2.Request(addr, headers={"User-Agent" : "Magic Browser"})
        f = urllib2.urlopen( req )
        s = f.read()
        f.close()
        return s
    except urllib2.URLError:
        return HTML404.format(addr)

def getWords(html_doc):
    """Return all `Word's in an HTML string, with formatting."""
    # Get rid of tags that won't be used
    pattern = re.compile('<table.*?</table>', re.DOTALL)
    html_doc = pattern.sub('', html_doc)
    pattern = re.compile('<sup.*?</sup>', re.DOTALL)
    html_doc = pattern.sub('', html_doc)
    # Preformat so we don't get floating punctuation, etc.
    repl = lambda m: m.group(2) + m.group(1)
    pattern = re.compile('([[(]+)(<.+?>)', re.DOTALL)
    html_doc = pattern.sub(repl, html_doc)
    pattern = re.compile('(</\S+>)([.,;)\]]+)')
    html_doc = pattern.sub(repl, html_doc)

    soup = bs4.BeautifulSoup(html_doc, from_encoding="utf-8")
    #soup = bs4.BeautifulSoup(html_doc, "lxml", from_encoding="utf-8")
    y = 0
    # Start by getting title
    words, _, _ = strToWords(getStr(soup.title), y, size=2)
    # Find relevant text-containing elements
    for tag in soup.body.find_all(['h2', 'dt', 'p', 'ul']):
        new_words = []
        y = words[-1].bottom - PARSPACE
        if tag.name == u'h2':
            new_words, _, _ = strToWords(getStr(tag), y, size=1)
        elif tag.name == u'dt':
            new_words, _, _ = strToWords(getStr(tag), y + PARSPACE / 2, attr=BOLD)
        elif tag.name == u'p':
            new_words, _, _ = getParWords(tag, y)
        elif tag.name == u'ul':
            new_words, _, _ = getParWords(tag, y + PARSPACE)
        words.extend(new_words)
        if tag.name == u'h2' and words[-1].text == u'References':
            break # That's as far down as we go
    return words

def getStr(tag):
    """Strips away `div' and `span' tags obscuring text."""
    for c in tag.children:
        if isinstance(c, bs4.element.NavigableString):
            if not c.isspace():   # <span> tags are the worst.
                return unicode(c)
        # ignore 'edit' link
        elif c.name in (u'span', u'div') and not c['class'] == [u'editsection']:
            end = getStr(c)
            if end is not None:
                return end
    return None

def getParWords(tag, y, x=0, attr=REGULAR, link = ""):
    """Return all `Word's in an HTML paragraph, with formatting."""
    words = []
    for c in tag.children:
        new_words = []
        if isinstance(c, bs4.element.NavigableString):
            new_words, x, y = strToWords(unicode(c), y, x=x,
                    attr=attr, link=link)
        elif c.name in (u'b', u'strong'):
            new_attr = BOLD
            if attr == ITALIC:
                new_attr = BOLDITAL
            new_words, x, y = getParWords(c, y, x, new_attr, link)
        elif c.name in (u'i', u'em'):
            new_attr = ITALIC
            if attr == BOLD:
                new_attr = BOLDITAL
            new_words, x, y = getParWords(c, y, x, new_attr, link)
        elif c.name == u'a':
            hl = c['href']
            if hl[:6] == "/wiki/":
                hl = "http://en.wikipedia.org" + hl
            else:
                hl = link
            new_words, x, y = getParWords(c, y, x, attr, hl)
        elif c.name == u'li':
            c.insert(0, unichr(BULLET))
            new_words, x, y = getParWords(c, y - 1.5 * VSPACE, INDENT,
                                          attr, link)
        elif c.name in (u'span', u'div'):
            new_words, x, y = getParWords(c, y, x, attr, link)
        words.extend(new_words)
    return (words, x, y)

def strToWords(s, y, x=0, attr=REGULAR, size=0, link=""):
    """Return string of words as `Word's, with correct locations."""
    if s is None:
        return ([], x, y)
    words = []
    for word in s.split():
        w = Word(word, (x, y), attr, size, link)
        if w.right >= PAGEWIDTH:
            w.left = 0
            w.y -= (w.top - w.bottom) + VSPACE
        x = w.right + HSPACE * (size + 1)
        y = w.bottom
        words.append(w)
    return (words, x, y)


class Word(MySprite):
    """Words are static obstacles generally used as platforms, except
    those that are hyperlinks, which can be also be "followed".

    Constructors:
        'text' : The character string of the Word.
        'pos'  : The starting position
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

    def __init__(self, text, pos, attr=REGULAR, size = 0, link=""):
        fontCheck(attr)
        self.ff = FRICTION_FACTOR
        self.text = text
        self.hyperlink = link
        if link == "": color = BLACK
        else: color = BLUE
        image = Word.WIKIFONT[attr][size].render(text, True, color)
        rect = image.get_rect()
        cropped_image = image.subsurface(rect.inflate(TEXT_CROPX * (size + 1),
                                                      TEXT_CROPY * (size + 1)))
        # Initialize sprite
        left, bottom = pos
        right = left + cropped_image.get_width()
        top = bottom + cropped_image.get_height()
        MySprite.__init__(self, texture=utils.getTexture(cropped_image),
                shape=[left, top, right, bottom])

    def isLink(self):
        return not (self.hyperlink == "")


class Page:
    def __init__(self, url):
        self.url = url
        self.words = getWords(getHTML(url))

