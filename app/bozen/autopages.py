# autopages.py = automatically-generated BREAD pages


from flask import request, redirect, render_template
import jinja2

from . import butil
from .butil import *
from . import ht
from . import paginate

#---------------------------------------------------------------------

flaskEnv = butil.Struct()

def notifyFlaskForAutopages(app, jinjaEnv):
    global flaskEnv
    flaskEnv.app = app
    flaskEnv.jinjaEnv = jinjaEnv


#---------------------------------------------------------------------

def http403(msg=""):
    """ Default forbidden message
    @param msg::str = contains text as an optional error message.
    return a response containing an HTTP 403 (forbidden) message
    """
    tem = flaskEnv.jinjaEnv.get_template("403.html")
    h = tem.render(
        msg = html.errorBox(msg),
    )
    return (h, 403)

class Autopage(object):
    def __init__(self, monDocCls: Type['MonDoc'], caps: str, **kwargs):
        self.colClass = monDocCls

        self.canBrowse = 'B' in caps
        self.canRead = 'R' in caps
        self.canEdit  = 'E' in caps
        self.canAdd = 'A' in caps
        if self.canAdd: self.canEdit = True
        self.canDelete = 'D' in caps
        if self.canDelete or self.canAdd or self.canEdit:
            self.canRead = True

        #>>>>> unpack kwargs
        self.useFields = kwargs.get('showFields',
            self.colClass.classInfo.fieldNameTuple[:5])
        self.sortCriteria = kwargs.get('sort',
            (list(self.useFields)
             + list(self.colClass.classInfo.fieldNameTuple))[0])
        self.permissionF = kwargs.get('permissionF', lambda: True)
        self.http403 = kwargs.get('http403', http403)

        #self.colName = self.colClass.__name__
        n = self.colClass.__name__
        self.colStub = n[:1].lower() + n[1:]
        self.runFlask()

    def runFlask(self):
        if 'app' not in flaskEnv.__dict__:
            raise RuntimeError("No flask environment has been defined for "
                "autopages. Did you call notifyFlaskForAutopages()?")
        self.flaskApp = flaskEnv.app
        self.jinjaEnv = flaskEnv.jinjaEnv

        #----- rule for /{foo}s
        if self.canBrowse:
            stub = self.colStub + "s"
            url = "/" + stub
            self.flaskApp.add_url_rule(url, stub)
            self.flaskApp.view_functions[stub] = self.colStubBrowseEp

        try:
            self.browseTem = self.jinjaEnv.get_template(self.colStub + "s.html")
        except jinja2.exceptions.TemplateNotFound:
            try:
                self.browseTem = self.jinjaEnv.get_template("autopage_list.html")
            except jinja2.exceptions.TemplateNotFound:
                raise RuntimeError(form("Cannot produce Browse page for "
                    "{}, because "
                    "templates '{}s.html' and 'autopage_list.html' both "
                    "do not exist",
                    self.colClass.__name__, self.colStub))

        #----- rule for /{foo}/{id}
        if self.canRead:
            stub = self.colStub
            url = form("/{}/<id>", self.colStub)
            self.flaskApp.add_url_rule(url, stub,
                methods=['POST', 'GET'])
            self.flaskApp.view_functions[stub] = self.colStubDocEp

        try:
            self.readTem = self.jinjaEnv.get_template(self.colStub + ".html")
        except jinja2.exceptions.TemplateNotFound:
            try:
                self.readTem = self.jinjaEnv.get_template("autopage_doc.html")
            except jinja2.exceptions.TemplateNotFound:
                raise RuntimeError(form("Cannot produce Read page for "
                    "{}, because "
                    "templates '{}.html' and 'autopage_read.html' both "
                    "do not exist",
                    self.colClass.__name__, self.colStub))


    #========== /{colStub}s ==========

    def colStubBrowseEp(self) -> str:
        """ This is the Flask endpoint for browsing a list of
        documents in a collection. If the collection class is Foo,
        this endpoint will have the url /foo
        """
        # permission:
        if not self.permissionF(): return self.http403()
        
        count = self.colClass.count()
        pag = paginate.Paginator(count)

        h = self.browseTem.render(
            colClass = self.colClass,
            count = count, pag = pag,
            table = self.browseTableH(pag),
            addButton = self.addButtonH(),
        )
        return h

    def browseTableH(self, pag: paginate.Paginator) -> str:
        """ An html table of the documents in a collection
        :return html for table
        :rtype str
        """
        useFnFi = [(fn, self.colClass.getFieldInfo(fn))
                   for fn in self.useFields]
        h = form("""<table class='bz-report-table'>
<tr>
    {others}
    <th>View</th>
</tr>""",
            others = "\n".join(form("<th>{}</th>", fi.columnTitle)
                               for _,fi in useFnFi))

        for doc in self.colClass.find(
            skip=pag.skip, # skip this number of docs before returning some
            limit=pag.numShow, # max number of docs to return
            sort=self.sortCriteria):
            others = ""
            for fn, fi in useFnFi:
                others += form("    <td>{}</td>\n", doc.asReadableH(fn))
            #//for
            docUrl = attrEsc(form("/{colStub}/{id}",
                colStub = self.colStub,
                id = doc.id()))
            h += form("""<tr>
    {others}
    <td><a href='{url}'>
        <i class='fa fa-eye'></i> View</a></td>
</tr>""",
                id = doc.id(),
                url = docUrl,
                others = others)
        #//for doc
        h += "</table>"
        return h

    def addButtonH(self) -> str:
        if not self.canAdd: return ""
        h = form("""<p><a class="btn btn-success" href="/{colStub}/NEW">
<i class="fa fa-plus"></i>
Create new {classTitle}</a></p>""",
            colStub = self.colStub,
            classTitle = self.colClass.classTitle())
        return h


    #========== /{colStub}/{id} ==========

    def colStubDocEp(self, id: str) -> str:
        """ This is the Flask endpoint for viewing a document in a
        collection. If the collection class is Foo,
        this endpoint will have the url /foo/<id>
        """
        # permission:
        if not self.permissionF(): return self.http403()
    
        if id=="NEW":
            if self.canAdd:
                doc = self.colClass()
                dpr("doc=%r", doc)
            else:
                return http403()
        else:
            doc = self.colClass.getDoc(id)
            dpr("doc=%r", doc)
        fwem = "" # form-wide error messages
        msg = ""

        if request.method=='POST':
            dpr("doc=%r:%s", doc, type(doc))
            doc = doc.populateFromRequest(request)
            dpr("after populate, doc=%r:%s", doc, type(doc))

            if request.form.get('delete', "") == u"1":
                # delete this record
                dpr("about to remove id=%r", id)
                doc.remove()
                return redirect(form("/{}s", self.colStub), code=302)
            elif doc.isValid():
                # update this record
                dpr("about to save doc=%r", doc)
                doc.save()
                msg = "Document saved."
                if id=="NEW":
                    newUrl = doc.url()
                    return redirect(newUrl, code=302)
            else:
                # (doc) is not valid, so re-display form
                dpr("!!!!!~~~~~ doc is not valid ~~~~~!!!!!\n%r", doc)
                fwem = doc.formWideErrorMessageH()
                pass
        #//if
        if self.canEdit:
            buildForm = doc.buildForm()
        else:
            buildForm = doc.buildForm(readOnly=True)

        h = self.readTem.render(
            id = id,
            doc = doc,
            buildForm = buildForm,
            fwem = fwem,
            msg = ht.goodMessageBox(msg),
            autopage = self,
        )
        return h

#---------------------------------------------------------------------

autopageList = []

def addAutopage(monDocCls: Type['MonDoc'], pages: str, **kwargs):
    """ Set up autopages on a collection class.
    @param pages = a string with one ofr more of the letters "BREAD" in it,
        for Browse Read Edit Add Delete
    """
    ap = Autopage(monDocCls, pages, **kwargs)
    autopageList.append(ap)

#---------------------------------------------------------------------


#end
