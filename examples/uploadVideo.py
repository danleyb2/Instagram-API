import InstagramAPI

# /////// CONFIG ///////
username = ''
password = ''
debug = False

video = ''  # path to the video
caption = ''  # caption
# //////////////////////

i = InstagramAPI.Instagram(username, password, debug)

try:
    i.login()
except Exception as e:
    e.message
    exit()

try:
    i.uploadVideo(video, caption)
except Exception as e:
    print e.message
