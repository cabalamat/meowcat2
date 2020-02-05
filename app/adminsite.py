# adminsite.py = create Bozen admin site

import bozen

import config
import allpages

#---------------------------------------------------------------------
# admin site

def createAdminSite():
    """ create admin site """
    import userdb
    import models
    import wikidb
    
    adminSite = bozen.AdminSite(stub=config.ADMIN_SITE_PREFIX)
    adminSite.showFields(userdb.User, ['userName'])
    adminSite.sortFields(userdb.User, 'userName')
    adminSite.showFields(models.Message, ['title','source','published'])
    adminSite.sortFields(models.Message, 'published')
    adminSite.showFields(wikidb.WikiPage,
        ['owner_id', 'pageName', 
         'published', 'source'])
    adminSite.sortFields(wikidb.WikiPage, 'pageName')
    adminSite.runFlask(allpages.app, allpages.jinjaEnv)

if config.CREATE_ADMIN_SITE:
    createAdminSite()

#---------------------------------------------------------------------

#end
