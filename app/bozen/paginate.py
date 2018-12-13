# paginate.py = does pagination

from flask import request
from flask_paginate import Pagination

#---------------------------------------------------------------------
"""
In the following:

perPage = number of items per page
total = total number of items
page = current page number (starts at 1)
showSinglePage = show pagination HTML on single page

output values are:

maxPage = the maximum page number
skip = number of items to skip
fromIx = display row from (starting at 1)
toIx = display row to (starting at 1)
numShow = number of rows to display
info = text to display on current page
links() = html containing urls for other pages
"""

DEFAULT_PER_PAGE = 20


class Paginator:
    def __init__(self, total, perPage=DEFAULT_PER_PAGE, showSinglePage=False):
        self.perPage = perPage
        self.total = total
        self.page = int(request.args.get('page', 1))
        self.showSinglePage = showSinglePage
        self.calc()

    def calc(self):
        """ calculate values for skip, etc. """
        self.maxPage = int((self.total + self.perPage - 1)/self.perPage)
        if self.maxPage < 1: self.maxPage = 1
        if self.page < 1: self.page = 1
        if self.page > self.maxPage: self.page = self.maxPage

        self.skip = (self.page-1)*self.perPage
        self.fromIx = self.skip + 1
        self.toIx = self.skip + self.perPage
        if self.toIx > self.total: self.toIx = self.total
        self.numShow = self.toIx - self.fromIx + 1

        self.info = "Displaying rows %d-%d of %d." % (
            self.fromIx, self.toIx, self.total)

        self.flaskPag = Pagination(
            page=self.page,
            css_framework="bootstrap3",
            link_size=self.perPage,
            show_single_page=self.showSinglePage,
            per_page=self.perPage,
            total=self.total)
        self.links = self.flaskPag.links


#---------------------------------------------------------------------


#end
