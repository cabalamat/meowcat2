# admin.py = create admin website

""" Bozen admin site

The admin site allows you to view and edit all the collections 
in the dictionary.

It is intended as scaffolding useful in constructing the website.
"""

from flask import request, redirect

from .butil import *
from butil import form, htmlEsc, attrEsc
from .bztypes import *
from . import paginate

from . import mongo
from . import mondoc

#---------------------------------------------------------------------
"""
Instance variables
~~~~~~~~~~~~~~~~~~

colKV = the collections we will be administering
colKV::[(
   colName::str = name of collection in database
   colCls::class = MonDoc subclass for collection
)]

colDict::{str:class} = the same information in (colKV) but in
    a class

colFields::{
   colName::str = a collection name
   fields::[str] = fields to show
} = which fields to show in /admin/col/{colName}

"""

class AdminSite(object):

    def __init__(self, 
        collections:Union[List[str],None]=None, 
        stub:str="admin"):
        if stub[:1] != "/": stub = "/" + stub
        self.stub = stub

        if collections==None:
            collections = mondoc.monDocSubclassDict.values()
            colKV = [(getColName(cls),cls)
                     for cls in collections
                     if cls is not mondoc.MonDoc]
            colKV.sort(key=lambda x: x[0])
        else:
            colKV = [(getColName(cls),cls) for cls in collections]
        self.colKV = colKV
        self.colDict = dict(self.colKV)
        self.colFields = {}
        self.sortSpecs = {}

    def showFields(self, colClass: Type[mondoc.MonDoc], 
                   fieldNames: List[str]):
        """ Say which fields to show in the /col/ page for a collection.
        :param colClass: the collection class
        :param fieldNames: fields to show for that class
        """
        colName = getColName(colClass)
        self.colFields[colName] = fieldNames

    def sortFields(self, colClass: Type[mondoc.MonDoc], sortSpec: SortSpec):
        """ say how we are to sort by in the /col/page.
        :param colClass: the collection class
        :type colClass: class
        :param sortSpec: a sort specification, in the same format used by
             MonDoc.find()
        """
        colName = getColName(colClass)
        self.sortSpecs[colName] = sortSpec

    def runFlask(self, flaskApp, jinjaEnv):
        """
        Start accepting requests for the admin site. Sets up hooks
        for Flask links, see <http://flask.pocoo.org/docs/0.10/api/#api>
        :param flaskApp: the flask application that will be sending us
            requests.
        :param jinjaEnv: Jinja2 environment, for getting admin_*.html templates
        """
        self.flaskApp = flaskApp
        self.jinjaEnv = jinjaEnv

        # URL rule for /admin
        self.flaskApp.add_url_rule(self.stub, 'admin')
        self.flaskApp.view_functions['admin'] = self.adminEp

        self.flaskApp.add_url_rule(self.stub+"/col/<colName>", 'adminColEp')
        self.flaskApp.view_functions['adminColEp'] = self.adminColEp

        self.flaskApp.add_url_rule(self.stub+"/doc/<colName>/<id>",
            'adminDocEp',
            methods=['POST', 'GET'])
        self.flaskApp.view_functions['adminDocEp'] = self.adminDocEp

    #========== /admin ==========
    # endpoints end in ...Ep

    def adminEp(self) -> HtmlStr:
        """ The /admin endpoint
        """
        tem = self.jinjaEnv.get_template("admin_front_page.html")
        h = tem.render(
            adminStub = self.stub,
            adminPagesLis = self.adminPagesLisH(),
            colTable = self.colTableH(),
        )
        #prvars("tem h")
        return h

    def colTableH(self) -> HtmlStr:
        """ An html table of the collections with a count of
        how many documents in each
        """
        h = """<table class='bz-report-table'>
<tr>
    <th>#</th>
    <th>Collection</th>
    <th>Count</th>
</tr>"""
        ix = 1
        for colName, colClass in self.colKV:
            count = colClass.count()
            h += form("""<tr>
    <td>{ix}</td>
    <td><a href='{stub}/col/{colName}'>{logo}{colName}</a></td>
    <td>{count}</td>
</tr>""",
                ix = ix,
                logo = colClass.classLogo(),
                stub = self.stub,
                colName = htmlEsc(colName),
                count = count,
            )
            ix += 1
        #//for

        h += "</table>\n"
        return h

    #========== /admin/col/{colName} ==========

    def adminColEp(self, colName: str) -> HtmlStr:
        """ The /admin/col/<colName> endpoint
        """
        colClass = self.colDict[colName]
        tem = self.jinjaEnv.get_template("admin_col.html")
        count = colClass.count()
        pag = paginate.Paginator(count)
        h = tem.render(
            adminStub = self.stub,
            adminPagesLis = self.adminPagesLisH(),
            colClass = colClass,
            colName = colName,
            docTable = self.docTableH(colClass, pag),
            count = count, pag = pag,
        )
        return h

    def docTableH(self, colClass: str, pag: paginate.Paginator) -> HtmlStr:
        """ An html table of the documents in a collection
        :return html
        :rtype str
        """
        colName = getColName(colClass)
        useFields = self.getUseFields(colClass)
        useFnFi = [(fn, colClass.getFieldInfo(fn))
                   for fn in useFields]
        h = form("""<table class='bz-report-table'>
<tr>
    <th>_id</th>
    <th>getName()</th>
    {others}
    <th>View</th>
</tr>""",
            others = "\n".join(form("<th>{}</th>", fi.title)
                               for _,fi in useFnFi))
        for doc in colClass.find(
            skip=pag.skip,
            limit=pag.numShow,
            sort=self.sortSpecs.get(colName, useFields[0])):
            others = ""
            for fn, fi in useFnFi:
                others += form("    <td>{}</td>\n", doc.asReadableH(fn))
            #//for
            docUrl = attrEsc(form("{stub}/doc/{colName}/{id}",
                stub = self.stub,
                colName = colName,
                id = doc.id()))
            h += form("""<tr>
    <td class='idvalue'>{id}</td>
    <td><a href='{url}'>{getName}</a></td>
    {others}
    <td><a href='{url}'>
        <i class='fa fa-eye'></i> View</a></td>
</tr>""",
                getName = htmlEsc(doc.getName()),
                id = doc.id(),
                url = docUrl,
                others = others)
        #//for doc
        h += "</table>\n"
        return h

    #========== /admin/doc/{colName}/{id} ==========

    def adminDocEp(self, colName: str, id: str) -> HtmlStr:
        """ The /admin/doc/<colName>/<id> endpoint
        :return
        :rtype str
        """
        colClass = self.colDict[colName]
        tem = self.jinjaEnv.get_template("admin_doc.html")
        if id=="NEW":
            doc = colClass()
            #prvars("doc")
        else:
            doc = colClass.getDoc(id)
            #prvars("doc")
        fwem = "" # form-wide error messages

        if request.method=='POST':
            #prvars("doc")
            doc = doc.populateFromRequest(request)
            #prvars("doc")

            if request.form['delete'] == u"1":
                # delete this record
                #pr("about to remove id=%r", id)
                doc.remove()
                return redirect(self.colUrl(colClass), code=302)
            elif doc.isValid():
                # update this record
                #pr("update doc=%r", doc)
                doc.save()
                return redirect(self.colUrl(colClass), code=302)
            else:
                # (doc) is not valid, so re-display form
                #pr("!!!!!~~~~~ doc is not valid ~~~~~!!!!!\n%r", doc)
                fwem = doc.formWideErrorMessageH()
                pass
        #//if

        h = tem.render(
            adminStub = self.stub,
            adminPagesLis = self.adminPagesLisH(),
            colName = colName,
            id = id,
            doc = doc,
            fwem = fwem,
            readOnly = False,
        )
        return h

    #==========

    def adminPagesLisH(self) -> HtmlStr:
        h = ""
        for n,colClass in self.colKV:
            h += form("""<li><a href="{stub}/col/{colName}">
                {logo}{colName}</a></li>""",
                stub = self.stub,
                logo = colClass.classLogo(),
                colName = n)
        #//for

        # add dummy at end so firefox displays it:
        h += "<li><a href="">&nbsp;</a></li>"
        #h += "<li><a href="">&nbsp;</a></li>"
        return h

    def getUseFields(self, colClass) -> List[str]:
        """ get which fields to use in a class  """
        colName = getColName(colClass)
        fields = self.colFields.get(colName, None)
        if fields != None: return fields

        fields = list(colClass.classInfo.fieldNameTuple[:5])
        self.colFields[colName] = fields
        return fields

    def colUrl(self, colClass) -> str:
        """
        Get the url for the adminCol endpoint for a collection
        :rtype str
        """
        colName = getColName(colClass)
        url = form("{stub}/col/{colName}",
            stub = self.stub,
            colName = getColName(colClass))
        return url



def getColName(clsName: Union[Type[mondoc.MonDoc],str]) -> str:
    """
    Get a collection name from a class name
    """
    if isinstance(clsName, type):
        clsName = clsName.__name__
    return clsName



#---------------------------------------------------------------------



#end
