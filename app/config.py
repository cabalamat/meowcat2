# config.py = configuration data 

#---------------------------------------------------------------------

APP_DATE_FORMAT = "%Y-%b-%d"

# port we are running on
PORT=7340

# title on web pages
APP_TITLE = "MeowCat"
APP_LOGO = "<i class='fa fa-commenting-o'></i> "

# unique identifier for the app, typically the same as its directory 
# in ~/sproj/ .
APP_NAME = "meowcat2"

# MongoDB database name (often the same as APP_NAME)
DB_NAME = "meowcat"

# Bozen admin site (scaffolding)
CREATE_ADMIN_SITE = True
ADMIN_SITE_PREFIX="db"

#---------------------------------------------------------------------
# about this MeowCat instance

# Site name
SITE_NAME = "Development MeowCat"

# protocol (either http of https)
SITE_PROTOCOL = "http"

# DNS address of site
SITE_LOCATION = "127.0.0.1"

SITE_STUB =  SITE_PROTOCOL + "://" + SITE_LOCATION 


#---------------------------------------------------------------------


#end
