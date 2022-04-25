# A very simple Flask Hello World app for you to get started with...
import time
import sqlite3
from datetime import datetime
from flask import Flask, request, redirect

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

'''
guestbookTableKey6={'tag':6,'displayName':'message','render':1,'inputTypeTag':6}
arrayGuestbookTableKey
'''

# from dwellingsouls - announcement table details
#tableObj0a=['row_id','publishStatusTag','epochTime','addedDate','lastEditedDate','content']
#tableObj0b=[7,12,7,7,7,22]
#tableObj0c=[None,[{'tag':0,'displayName':'Draft'},{'tag':1,'displayName':'Publish'}],int(time.time()),datetime.today().strftime('%Y%m%d'),datetime.today().strftime('%Y%m%d'),None]
#tableObj0={'tag':0,'tablename':'announcements','columns':tableObj0a,'formInputType':tableObj0b,'valuesArray':tableObj0c}

dbTableObj0a=['row_id','publishStatusTag','dateAdded','sender','category','others','message','epochTime']
dbTableObj0b={0:{'label':'family','symbol':'👪'},1:{'label':'primary school','symbol':'🎒'},2:{'label':'secondary school','symbol':'🏫'},3:{'label':'college','symbol':'📚'},4:{'label':'university','symbol':'🎓'},5:{'label':'workplace','symbol':'👔'},6:{'label':'acquaintance','symbol':'😀'},7:{'label':'socials','symbol':'🍷'},8:{'label':'others','symbol':'⭐'},9:{'label':'rather not say','symbol':'🥔'}}
dbTableObject0={'tag':0,'tableName':'guestbook','columns':dbTableObj0a,'grouping':dbTableObj0b,'sortBy':'epochTime','sortBy1':'category','sortBy1Order':'ASC','sortByOrder':'DESC'}

dbTableObj1a=['row_id','publishStatusTag','dateAdded','category','displayOrder','file','title','link','skills','media','epochTime']
dbTableObj1b={0:{'tag':0,'label':'Introduction'},2:{'tag':2,'label':'Embedded Systems'},1:{'tag':1,'label':'Software Development'},3:{'tag':3,'label':'Hardware Programming'}}
dbTableObject1={'tag':1,'tableName':'projects','columns':dbTableObj1a,'grouping':dbTableObj1b,'sortBy':'category','sortBy1':'displayOrder','sortBy1Order':'ASC','sortByOrder':'ASC'}

dbTableObj2a=['row_id','publishStatusTag','dateAdded','category','displayOrder','file','title','duration','position','link','media','epochTime']
dbTableObj2b={0:{'tag':0,'label':'Introduction'},3:{'tag':3,'label':'Primary/Secondary Education'},2:{'tag':2,'label':'Tertiary Education'},1:{'tag':1,'label':'Professional Experience'}}
dbTableObject2={'tag':2,'tableName':'about','columns':dbTableObj2a,'grouping':dbTableObj2b,'sortBy':'category','sortBy1':'displayOrder','sortBy1Order':'ASC','sortByOrder':'ASC'}

dbTableArray=[dbTableObject0,dbTableObject1,dbTableObject2]

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
    twoColumns=True

    if (page==None):
        page='landing'
        contentObj=landing()
    elif (page=='about'):
        if subpage==None:
            subpage=9
        contentObj=about(subpage)
    elif (page=='projects'):
        if subpage==None:
            subpage=8
        contentObj=projects(subpage)
    elif (page=='reviewEntry'):
        contentObj=reviewEntry()
        twoColumns=False
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
    if twoColumns:
        temp=renderHtml('pageTwoColumns').format(panel0=panel0,panel1=panel1)
    else:
        temp=renderHtml('pageOneColumn').format(panel0=panel0)
    page=renderHtml('page').format(wrapper=page,pageName=pageName,header=panelHeader,content=temp,footer=panelFooter)
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
        if (page==None):
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
def about(subpage=None):
    folder='about'
    errorCode=True
    errorMessage=None
    pageName='About'
    panel0=panel1=''

    try:
        if subpage:
            panel0=listEntries('about',0,1,subpage)
        else:
            panel0=renderHtml('about',folder)
        panel1=listEntries('about',0,0,subpage)
        errorCode=False
    except Exception as e:
        errorMessage=str(e)

    return {'panel0':panel1,'panel1':panel0,'pageName':pageName,'errorCode':errorCode,'errorMessage':errorMessage}

# function type: render page
def projects(subpage=None):
    folder='projects'
    errorCode=True
    errorMessage=None
    pageName='Projects'
    panel0=panel1=''
    try:
        if subpage:
            panel0=listEntries('projects',0,1,subpage)
        else:
            panel0=renderHtml('projects',folder)
        panel1=listEntries('projects',0,0,subpage)
    except Exception as e:
        #errorMessage=str(e)
        panel0='fail -'+str(e)
    return {'panel0':panel1,'panel1':panel0,'pageName':pageName,'errorCode':errorCode,'errorMessage':errorMessage}

# function type: render object
def guestbook(alert=None):
    folder='guestbook'
    errorMessage=None
    errorCode=True
    content=alertMessage=''
    pageName='Guestbook'
    panel0=panel1=''

    allEntries=listEntries('guestbook',0,0)

    try:
        #newEntry=''
        if (alert!=None):
            if (alert):
                alertMessage='<body onLoad="myFunction(false);">'
            else:
                alertMessage='<body onLoad="myFunction(true);">'
        content+=renderHtml('guestbook',folder).format(alert=alertMessage,allEntries=allEntries)
        errorCode=False
    except Exception as e:
        errorMessage=str(e)
        content='fail -'+str(e)
    panel0=content
    return {'panel0':panel0,'panel1':panel1,'pageName':pageName,'errorCode':errorCode,'errorMessage':errorMessage}

# function type: operational
def convertArrayToObject(obj,table):
    for dbTableObject in dbTableArray:
        if table==dbTableObject['tableName']:
            arrayColumns=dbTableObject['columns']

    return dict(zip(arrayColumns,obj))

# function type: operational
def listEntries(table,sortBy=0,mode=0,subpage=None):
    '''
    mode=0 panel 0 (render both sidebar and content columns)
    mode=1 panel 1 (render only sidebar)
    '''
    folder=table
    dbObj=initDatabase()
    db1=dbObj['cursor']
    content=contentMobile=temp=''
    obj={}

    #get dbTableObject based on tableName
    for dbTableObject in dbTableArray:
        if table==dbTableObject['tableName']:
            tableName=dbTableObject['tableName']
            grouping=dbTableObject['grouping']
            sortBy=dbTableObject['sortBy']
            sortBy1=dbTableObject['sortBy1']
            sortByOrder=dbTableObject['sortByOrder']
            sortBy1Order=dbTableObject['sortBy1Order']

    db1.execute('SELECT * FROM {} WHERE publishStatusTag = {} ORDER BY {} {}, {} {} LIMIT 0, 49999;'.format(tableName,1,sortBy,sortByOrder,sortBy1,sortBy1Order))
    ll=db1.fetchall()

    try:
        for l in ll:
            obj=convertArrayToObject(l,tableName)
            row_id=obj['row_id']
            category=obj['category']
            temp0=grouping[category]
            temp1=temp0['label']
            if tableName=='guestbook':
                folder='entries'
                sender=obj['sender']
                symbol=temp0['symbol']
                dateAdded=str(obj['dateAdded'])
                displayDateAdded=renderHtml('displayDateAdded',folder).format(year=dateAdded[0:4],month=dateAdded[4:6],day=dateAdded[6:8])
                message=obj['message']
                content+=renderHtml('entry',folder).format(symbol=symbol,sender=sender,dateAdded=displayDateAdded,message=message)
            elif tableName=='about':
                if mode==0:
                    if temp!=category:
                        temp=category
                        content+=renderHtml('sidebarHeadingObject','sidenav').format(temp1)
                        contentMobile+=renderHtml('sidebarHeadingObjectMobile','sidenav').format(temp1)
                    if str(subpage)==str(row_id):
                        content+=renderHtml('sidebarObjectActive','sidenav').format(str(obj['row_id']),obj['title'])
                        contentMobile+=renderHtml('sidebarObjectActiveMobile','sidenav').format(str(obj['row_id']),obj['title'])
                    else:
                        content+=renderHtml('sidebarObject','sidenav').format(str(obj['row_id']),obj['title'])
                        contentMobile+=renderHtml('sidebarObjectMobile','sidenav').format(str(obj['row_id']),obj['title'])
                else:
                    if str(subpage)==str(row_id):
                        content+=renderHtml('contentObject',folder).format(obj['title'],renderHtml('content',folder+'/'+obj['file']))
            else: #projects
                if mode==0:
                    if temp!=category:
                        temp=category
                        content+=renderHtml('sidebarHeadingObject','sidenav').format(temp1)
                        contentMobile+=renderHtml('sidebarHeadingObjectMobile','sidenav').format(temp1)
                    if str(subpage)==str(row_id):
                        content+=renderHtml('sidebarObjectActive','sidenav').format(str(obj['row_id']),obj['title'])
                        contentMobile+=renderHtml('sidebarObjectActiveMobile','sidenav').format(str(obj['row_id']),obj['title'])
                    else:
                        content+=renderHtml('sidebarObject','sidenav').format(str(obj['row_id']),obj['title'])
                        contentMobile+=renderHtml('sidebarObjectMobile','sidenav').format(str(obj['row_id']),obj['title'])
                else:
                    if str(subpage)==str(row_id):
                        content+=renderHtml('contentObject',folder).format(obj['title'],renderHtml('content',folder+'/'+obj['file']))
    except Exception as e:
        errorMessage=e
        content+=str(errorMessage)

    if mode==0 and table!='guestbook':
        output=renderHtml('sidebar','sidenav').format(content,contentMobile)
    else:
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
        category=int(request.form['category'])
        temp=dbTableObj0b[category]
        symbol=temp['symbol']
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
def initDatabase():
    guestbookDb=sqlite3.connect(dbPath, check_same_thread=False)
    db1=guestbookDb.cursor()
    return {'cursor':db1,'database':guestbookDb}

# function type: operational
def renderHtml(filename,path=None):
    if (path==None):
        fullFilename=srcPath+filename+'.html'
    else:
        fullFilename=srcPath+path+'/'+filename+'.html'
    file=open(fullFilename,'r')
    content=file.read()
    return content