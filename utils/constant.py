import os




appPackage ="app.varlorg.unote"
appActivity = 'jacoco.MainActivity'

basedir = os.getcwd()+'/data/'+appPackage
configs = {
    'ANDROID_SCREENSHOT_DIR': "/sdcard/Download/uitest/picture",
    'ANDROID_XML_DIR': "/sdcard/Download/uitest/xml" ,
    'DEVICE': 'AJNJ9X5205G00923'
}


logfilePath = basedir + '/log.json'
pagePath = basedir+ '/pages.json'
transitionPath = basedir+ '/transitions.json'
script = basedir+ '/script.json'
savedir = basedir +'/assets/'
info = os.getcwd()+'/data/'+ appPackage+'.txt'
api_key = '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'

