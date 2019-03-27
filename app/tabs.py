# tabs.py = tab line on some pages

from bozen.butil import form

#---------------------------------------------------------------------

def makeTabLine3(tabTypesNames, curTabType, urlTemplate, fillerH=None):
    """ Make HTML for a tab line at the top of the screen.
    @param tabTypesNames::[(str,str)] = a list of tab information,
        for each one:
        - as it is in URLs (the "tab type")
        - as it is displayed (the "tab name")
    @param curTabType::str = the current tab type (one of tabTypes)
    @param urlStub::str = the url with '{TAB}' for whatever will be
            in tabTypes for a tab
    @param fillerH:str|None = if this contains a string, it is the string
        that goes between each tab item. If it is None, the default filler string
        is used.
    @return::str containing html
    """
    divClass = "tabs3" # <div> containing all tabs
    spanClass = "tab3" # one tab
    fillerClass = "tab3-filler" # filler between tabs
    tabSelectedClass = "selected"

    h = "<div class='%s'>\n" % (divClass,)
    if fillerH is None:
        # use default filler
        filler = form("<span class='{fillerClass}'> </span>",
            fillerClass = fillerClass)
    else:
        filler = fillerH
    first = True
    for tabType, tabName in tabTypesNames:
        if not first:
            h += filler
        if tabType==curTabType:
            h += form("<span class='tab3-selected'>"
                "{tabName}</span>",
                spanClass = spanClass,
                selectedClass = tabSelectedClass,
                tabName = tabName)
        else:
            url = urlTemplate.replace("{TAB}", tabType)
            h += form("<span class='tab3-not-selected'>"
                "<a href='{url}'>{tabName}</a></span>",
                spanClass = spanClass,
                url = url,
                tabName = tabName)
        first = False
    #//for
    #h += "<hr class='tab3-filler-end-line'/>"
    #h += "<span class='tab3-filler-end-line'> </span>"
    #h += "<span class='tab3-filler'> </span>"
    h += "</div>\n"
    return h

#---------------------------------------------------------------------


#end
