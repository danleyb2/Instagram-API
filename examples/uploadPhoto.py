import InstagramAPI
from InstagramAPI import InstagramException

# /////// CONFIG ///////
username = ''
password = ''
debug = False

photo = ''      # path to the photo
caption = ''    # caption
# //////////////////////

i = InstagramAPI.Instagram(username, password, debug)

try:
    i.login()
except InstagramException as e:
    e.message
    exit()

try:
    i.uploadPhoto(photo, caption)
except Exception as e:
    print e.message
