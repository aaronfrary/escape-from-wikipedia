
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

import urllib2
from bs4 import BeautifulSoup
#import lxml

def get_html(addr):
    """Return html for webpage 'addr', or "" on failed connection."""
    try:
        req = urllib2.Request(addr, headers={"User-Agent" : "Magic Browser"})
        f = urllib2.urlopen( req )
        s = f.read()
        f.close()
        return s
    except URLError:
        return ""

def get_words(html_doc):
    """This will do something...""" #FIXME
    soup = BeautifulSoup(html_doc, "lxml", from_encoding="utf-8")
    #TODO
    return []
