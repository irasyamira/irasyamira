# A very simple Flask Hello World app for you to get started with...
from flask import Flask
app = Flask(__name__)

htmlFolderPath='/home/arimaysari/irasyamira/src/'

headerObject0={'tag':'home','link':'/home'}
headerObject1={'tag':'about','link':'/about'}
headerObject2={'tag':'contact','link':'/contact'}
headerObject3={'tag':'cv','link':'/cv'}
arrayHeaderObject=[headerObject0,headerObject1,headerObject2,headerObject3]

@app.route('/')
def hello_world():
    page=renderHeader()
    page+='Hello from Flask!'
    return page

def renderHeader():
    folder='header'
    output=headerObjects=''
    for obj in arrayHeaderObject:
        objectName=obj['tag']
        link=obj['link']
        headerObjects+=renderHtml('headerObject',folder).format(link=link,pageName=objectName.upper())
    output=renderHtml('header',folder).format(headerObjects=headerObjects)
    return output

# name      : ()
# function  : ?
# input     : ?
# output    : ?
def renderHtml(filename,path=None):
    if (path==None):
        fullFilename=htmlFolderPath+filename+'.html'
    else:
        fullFilename=htmlFolderPath+path+'/'+filename+'.html'
    file=open(fullFilename,'r')
    content=file.read()
    return content