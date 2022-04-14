# A very simple Flask Hello World app for you to get started with...
import sqlite3
import time
from flask import Flask, request, redirect
from datetime import datetime

import os

app = Flask(__name__)

srcPath='/home/arimaysari/irasyamira-flask/src/'
dbPath='/home/arimaysari/irasyamira-flask/db/irasyamira-flask.db'

headerObject0={'tag':'home','link':'/'}
headerObject1={'tag':'about','link':'/about'}
headerObject2={'tag':'cv','link':'/cv'}
headerObject3={'tag':'guestbook','link':'/guestbook'}
headerObject4={'tag':'posts','link':'/posts'}
headerObject5={'tag':'projects','link':'/projects'}
arrayHeaderObject=[headerObject0,headerObject1,headerObject5]

guestCategory0={'tag':0,'label':'family','symbol':'👪'}
guestCategory1={'tag':1,'label':'primary school','symbol':'🎒'}
guestCategory2={'tag':2,'label':'secondary school','symbol':'🏫'}
guestCategory3={'tag':3,'label':'college','symbol':'📚'}
guestCategory4={'tag':4,'label':'university','symbol':'🎓'}
guestCategory5={'tag':5,'label':'workplace','symbol':'👔'}
guestCategory6={'tag':6,'label':'acquaintance','symbol':'😀'}
guestCategory7={'tag':7,'label':'socials','symbol':'🍷'}
guestCategory8={'tag':8,'label':'others','symbol':'⭐'}
guestCategory9={'tag':9,'label':'rather not say','symbol':'🥔'}
arrayGuestCategory=[guestCategory0,guestCategory1,guestCategory2,guestCategory3,guestCategory4,guestCategory5,guestCategory6,guestCategory7,guestCategory8,guestCategory9]

'''
guestbookTableKey0={'tag':0,'displayName':'row_id','render':0,'inputTypeTag':1}
guestbookTableKey1={'tag':1,'displayName':'publishStatusTag','render':0,'inputTypeTag':3}
guestbookTableKey2={'tag':2,'displayName':'dateAdded','render':0,'inputTypeTag':1}
guestbookTableKey3={'tag':3,'displayName':'sender','render':1,'inputTypeTag':6}
guestbookTableKey4={'tag':4,'displayName':'category','render':1,'inputTypeTag':3}
guestbookTableKey5={'tag':5,'displayName':'others','render':1,'inputTypeTag':6}
guestbookTableKey6={'tag':6,'displayName':'message','render':1,'inputTypeTag':6}
'''
guestbookTableKey0={'tag':0,'displayName':'row_id','render':0,'inputTypeTag':'hidden'}
guestbookTableKey1={'tag':1,'displayName':'publishStatusTag','render':0,'inputTypeTag':'radio'}
guestbookTableKey2={'tag':2,'displayName':'dateAdded','render':0,'inputTypeTag':'hidden'}
guestbookTableKey3={'tag':3,'displayName':'sender','render':1,'inputTypeTag':'text'}
guestbookTableKey4={'tag':4,'displayName':'category','render':1,'inputTypeTag':'radio'}
guestbookTableKey5={'tag':5,'displayName':'others','render':1,'inputTypeTag':'text'}
guestbookTableKey6={'tag':6,'displayName':'message','render':1,'inputTypeTag':'text'}
arrayGuestbookTableKey=[guestbookTableKey0,guestbookTableKey1,guestbookTableKey2,guestbookTableKey3,guestbookTableKey4,guestbookTableKey5,guestbookTableKey6]

inputTypeTag0={'tag':0,'inputType':'button'}
inputTypeTag1={'tag':1,'inputType':'hidden'}
inputTypeTag2={'tag':2,'inputType':'password'}
inputTypeTag3={'tag':3,'inputType':'radio'}
inputTypeTag4={'tag':4,'inputType':'search'}
inputTypeTag5={'tag':5,'inputType':'submit'}
inputTypeTag6={'tag':6,'inputType':'text'}
arrayRenderType=[inputTypeTag0,inputTypeTag1,inputTypeTag2,inputTypeTag3,inputTypeTag4,inputTypeTag5,inputTypeTag6]

@app.route('/', methods=['GET','POST'])
@app.route('/<page>', methods=['GET','POST'])
@app.route('/<page>/', methods=['GET','POST'])
@app.route('/<page>/<subpage>', methods=['GET','POST'])
def hello_world(page=None,subpage=None):

    panel0=panel1=''

    if (page==None):
        contentObj=landing()
    elif (page=='about'):
        contentObj=about()
    elif (page=='guestbook'):
        contentObj=guestbook()
    elif (page=='projects'):
        contentObj=projects()
    elif (page=='posts'):
        if (subpage!=None):
            contentObj=posts(subpage)
        else:
            contentObj=posts()
    elif (page=='reviewEntry'):
        contentObj=reviewEntry()
    elif (page=='editDatabase'):
        contentObj=landing(editDatabase())
    elif (page=='home'):
        return redirect("/")
    else:
        contentObj=landing()

    panel0=contentObj['panel0']
    panel1=contentObj['panel1']
    pageName=contentObj['pageName']
    panelHeader=header(page)
    panelFooter=footer()
    page=renderHtml('page').format(pageName=pageName,header=panelHeader,panel0=panel0,panel1=panel1,footer=panelFooter)
    return page

# function type: render object
def footer():
    folder='footer'
    output=''
    try:
        output=renderHtml('footer',folder)
    except Exception as e:
        #errorMessage=str(e)
        output='fail -'+str(e)
    return output

# function type: render object
def header(page=None):
    folder='header'
    output=headerObjects=''
    for obj in arrayHeaderObject:
        objectName=obj['tag']
        link=obj['link']
        if (str(page)==str(None)):
            page='home'
        if (page==objectName):
            headerObjects+=renderHtml('headerObjectActive',folder).format(link=link,pageName=objectName.upper())
        else:
            headerObjects+=renderHtml('headerObject',folder).format(link=link,pageName=objectName.upper())
        #headerObjects+='current page: ' + str(page)
    output=renderHtml('header',folder).format(headerObjects=headerObjects)
    return output

# function type: render page
def landing(alert=None):
    folder='landing'
    errorCode=True
    errorMessage=None
    pageName='Home'
    panel0=panel1=''
    try:
        panel0=renderHtml('welcomeMessage',folder)
        temp=guestbook(alert)
        panel1=temp['panel0']
    except Exception as e:
        errorMessage=str(e)
        panel0='fail -'+str(e)
    return {'panel0':panel0,'panel1':panel1,'pageName':pageName,'errorCode':errorCode,'errorMessage':errorMessage}

# function type: render page
def projects():
    folder='projects'
    errorCode=True
    errorMessage=None
    pageName='Projects'
    panel0=panel1=''
    try:
        panel0=renderHtml('projects',folder)
    except Exception as e:
        #errorMessage=str(e)
        panel0='fail -'+str(e)
    return {'panel0':panel0,'panel1':panel1,'pageName':pageName,'errorCode':errorCode,'errorMessage':errorMessage}

'''
guestbookTableKey6={'tag':6,'displayName':'message','render':1,'inputTypeTag':6}
arrayGuestbookTableKey
'''

# function type: render object
def guestbook(alert=None):
    folder='guestbook'
    errorMessage=None
    errorCode=True
    content=alertMessage=''
    pageName='Guestbook'
    panel0=panel1=''

    allEntries=listEntries('guestbook',0)

    try:
        #newEntry=''
        if (alert!=None):
            if (alert):
                alertMessage='<body onLoad="myFunction(false);">'
            else:
                alertMessage='<body onLoad="myFunction(true);">'
        #content+='alert: ' + str(not alert)
        #content+=renderHtml('guestbook',folder).format(alert=alertMessage,allEntries=allEntries,newEntry=newEntry)
        content+=renderHtml('guestbook',folder).format(alert=alertMessage,allEntries=allEntries)
        errorCode=False
    except Exception as e:
        errorMessage=str(e)
        content='fail -'+str(e)
    panel0=content
    return {'panel0':panel0,'panel1':panel1,'pageName':pageName,'errorCode':errorCode,'errorMessage':errorMessage}

# function type: operational
def listEntries(table='guestbook',sortBy=0,mode=None):
    folder='entries'
    dbObj=initDatabase()
    db1=dbObj['cursor']
    content=''
    obj={}

    db1.execute('SELECT * FROM {} ORDER BY epochTime DESC LIMIT 0, 49999;'.format(table))
    ll=db1.fetchall()

    try:
        for l in ll:
            obj=getObjectFromTable(l,table)
            sender=obj['sender']
            category=obj['category']
            for guestCategory in arrayGuestCategory:
                if category==guestCategory['tag']:
                    symbol=guestCategory['symbol']
            dateAdded=str(obj['dateAdded'])
            displayDateAdded=renderHtml('displayDateAdded',folder).format(year=dateAdded[0:4],month=dateAdded[4:6],day=dateAdded[6:8])
            message=obj['message']
            content+=renderHtml('entry',folder).format(symbol=symbol,sender=sender,dateAdded=displayDateAdded,message=message)
    except Exception as e:
        errorMessage=e
        content=str(errorMessage)

    output=content
    return output

# function type: operational
def reviewEntry():
    folder='entries'
    errorMessage=None
    errorCode=True
    content=''
    pageName='Review Entry'
    panel0=panel1=''

    try:
        sender=request.form['name']
        message=request.form['message']
        category=request.form['category']
        for guestCategory in arrayGuestCategory:
            if int(category)==guestCategory['tag']:
                symbol=guestCategory['symbol']
        displayDateAdded=datetime.today().strftime('%Y%m%d')
        content+=renderHtml('reviewEntry',folder).format(symbol=symbol,sender=sender,displayDateAdded=displayDateAdded,message=message,publishStatusTag=1,dateAdded=displayDateAdded,category=category,others=None)
        errorCode=False
    except Exception as e:
        errorMessage=str(e)
        content='fail -'+str(e)
    panel0=content
    return {'panel0':panel0,'panel1':panel1,'pageName':pageName,'errorCode':errorCode,'errorMessage':errorMessage}

# function type: operational
def editDatabase(table='guestbook',newEntry=False):
    dbObj=initDatabase()
    db1=dbObj['cursor']
    guestbookDb=dbObj['database']
    #errorMessage=None
    errorCode=True
    content=''

    try:
        content+='sender'
        sender=request.form['sender']
        content+='publishStatusTag'
        publishStatusTag=request.form['publishStatusTag']
        content+='dateAdded'
        dateAdded=request.form['dateAdded']
        content+='category'
        category=request.form['category']
        content+='others'
        others=request.form['others']
        content+='message'
        message=request.form['message']
        epochTime=time.time()
        try:
            db1.execute('INSERT INTO {table} (sender,publishStatusTag,dateAdded,category,others,message,epochTime) VALUES (?,?,?,?,?,?,?);'.format(table=table), (sender,publishStatusTag,dateAdded,category,others,message,epochTime,))
            guestbookDb.commit()
            errorCode=False
            content='success!'
        except Exception as e:
            #errorMessage=str(e)
            content='fail to commit to db -'+str(e)

    except Exception as e:
        #errorMessage=str(e)
        content+='fail to retrieve params -'+str(e)

    return errorCode

# function type: operational
def getObjectFromTable(obj,table='guestbook'):
    [row_id,publishStatusTag,dateAdded,sender,category,others,message,epochTime]=obj
    return {'row_id':row_id,'sender':sender,'message':message,'dateAdded':dateAdded,'publishStatusTag':publishStatusTag,'category':category,'others':others,'epochTime':epochTime}

# function type: operational
def initDatabase():
    guestbookDb=sqlite3.connect(dbPath, check_same_thread=False)
    db1=guestbookDb.cursor()
    return {'cursor':db1,'database':guestbookDb}

# function type: render page
def posts(subpage=None):
    folder='posts'
    errorCode=True
    errorMessage=''
    pageName='Posts'
    ttt=content=sidenav=slide=''
    panel0=panel1=''

    tt=[{'title':'Making of this website','content':'intel','dateAdded':'20210706','link':7},
	{'title':'My experience in Intel PSG','content':'intel','dateAdded':'20210705','link':0},
    {'title':'My experience in Awantec','content':'awantec','dateAdded':'20210705','link':3},
    {'title':'My experience in University of Auckland','content':'uoa','dateAdded':'20210705','link':1},
    {'title':'My experience in Kolej Mara Banting','content':'kmb','dateAdded':'20210704','link':4},
    {'title':'My experience in Universiti Malaya','content':'um','dateAdded':'20210703','link':6},
    {'title':'My experience in Sekolah Seri Puteri','content':'ssp','dateAdded':'20210703','link':2},
    {'title':'My experience in Sekolah Kebangsaan Putrajaya Presint 9 (1)','content':'skpj2','dateAdded':'20210703','link':5}]
    try:
        if (subpage!=None):
            found=False
            for t in tt:
                link=t['link']
                if (int(subpage)==link):
                    path=os.getcwd()+'/src/posts/'+str(link)+'/img/'
                    count=0
                    f=ff=''
                    for file in os.listdir(path):
                        count+=1
                        f+=renderHtml('img',folder).format(link=link,img=file) #,img1=img1,img2=img2)
                        ff+=renderHtml('imgCount',folder).format(count=str(count)) #,img1=img1,img2=img2)

                    slide=renderHtml('slide',folder).format(slides=f,count=ff)
                    found=True
                    pageName=title=t['title']

                    path='/posts/{}'.format(str(link))
                    entry=renderHtml('entry',path)

                    dateAdded=t['dateAdded']
                    ttt+=renderHtml('entry',folder).format(slide=slide,title=title,year=dateAdded[0:4],month=dateAdded[4:6],day=dateAdded[6:8],entry=entry)
                    break
            if (found==False):
                ttt='post does not exist'
        else:
            for t in tt:
                title=t['title']
                link=t['link']
                #content=os.getcwd()+'/src/posts/'+str(link)+'/entry'
                path='/posts/{}'.format(str(link))
                entry=renderHtml('entry',path)

                path=os.getcwd()+'/src/posts/'+str(link)+'/img/'
                count=0
                for file in os.listdir(path):
                    try:
                        img='/src/posts/'+str(link)+'/img/{}'.format(file)
                        break
                    except Exception as e:
                        errorMessage+=str(e)
                        continue
                preview=entry[0:80]
                dateAdded=t['dateAdded']
                ttt+=renderHtml('preview',folder).format(img=img,title=title,year=dateAdded[0:4],month=dateAdded[4:6],day=dateAdded[6:8],preview=preview,link=link)
        #render sidenav
        for t in tt:
            title=t['title']
            link=t['link']
            sidenav+=renderHtml('sidenavObj',folder).format(title=title,link=link)


        content=renderHtml('posts',folder).format(sidenav=sidenav,posts=ttt)
        errorCode=False
    except Exception as e:
        errorMessage+=str(e)
        content+=errorMessage

    panel0=content
    return {'panel0':panel0,'panel1':panel1,'pageName':pageName,'errorCode':errorCode,'errorMessage':errorMessage}

# function type: render page
def about():
    folder='about'
    errorCode=True
    errorMessage=None
    pageName='About'
    panel0=panel1=''

    try:
        content=renderHtml('about',folder)
        errorCode=False
    except Exception as e:
        errorMessage=str(e)

    panel0=content
    return {'panel0':panel0,'panel1':panel1,'pageName':pageName,'errorCode':errorCode,'errorMessage':errorMessage}

# function type: operational
def renderHtml(filename,path=None):
    if (path==None):
        fullFilename=srcPath+filename+'.html'
    else:
        fullFilename=srcPath+path+'/'+filename+'.html'
    file=open(fullFilename,'r')
    content=file.read()
    return content