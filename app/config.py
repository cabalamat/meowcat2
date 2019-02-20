# config.py = configuration data 

#---------------------------------------------------------------------

APP_DATE_FORMAT = "%Y-%b-%d"

# port we are running on
PORT=7340

# title on web pages
APP_TITLE = "Meowcat"
APP_LOGO = "<i class='fa fa-commenting-o'></i> "

# unique identifier for the app, typically the same as its directory 
# in ~/sproj/ .
# Usually also used for MongoDB database name
APP_NAME = "meowcat2"
DB_NAME = "meowcat"

# Bozen admin site (scaffolding)
CREATE_ADMIN_SITE = True

#---------------------------------------------------------------------

# protocol (either http of https)
SITE_PROTOCOL = "http"

# DNS address of site
SITE_LOCATION = "127.0.0.1"

SITE_STUB =  SITE_PROTOCOL + "://" + SITE_LOCATION 

#---------------------------------------------------------------------


#end
