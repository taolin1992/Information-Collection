# -*- encoding=utf8 -*-
#__author__ = 'Tao Lin'
#!/user/bin/python2.7
# Filename : helloword.py
from xml.dom import minidom
import types  
import time
import urllib
import sys
reload(sys)   

#argv[0] = 'dlut.py', argv[1] = '*', argv[2] = 'r1.txt', argv[3] = storestatus = 'r2.txt', argv[4] = 'opac.lib.dlut.edu.cn'
global storestatus
storestatus = sys.argv[3]



#Record system parameters at the beginning of every new call number, write into r2.txt
def addcreatestatusfile():
    #store=sys.argv[3]
    fobj = open(storestatus,"w")
    order = 'python '+sys.argv[0]+' '+sys.argv[1]+' '+sys.argv[2]+' '+sys.argv[3]+' '+sys.argv[4]
    content=order+"\n"
    fobj.write(content)
    fobj.close()


#Append call numbers
def createstatusfile(n):
    #store=sys.argv[3]
    fobj = open(storestatus,"a")
    if type(n) is types.IntType:
        content=str(n)+"\n\n"
    else:
        content=n+"\n\n"
    fobj.write(content)
    fobj.close()


#Change "\n" of the 3rd line into "-(n)\n"
def failestatusfilep(n):
    fobj = open(storestatus,"r")
    content=fobj.readlines()
    #print content
    k=len(content)
    #print k
    fobj = open(storestatus,"w")
    for i in range(k):
        if i == 2:
            fobj = open(storestatus,"a")
            newline = content[i].replace('\n','')+ "-(" + str(n)+")\n"
            #print str(i)+":"+content[i]
            fobj.write(newline)
        else:
            fobj = open(storestatus,"a")
            #print str(i)+":"+content[i]
            fobj.write(content[i])

    fobj.close()


#Add a "done" at the end of r2.txt
def finishstatusfile():
    fobj = open(storestatus,"r")
    content=fobj.readlines()
    k=len(content)
    #print k
    if content[k-1]==' ':
        fobj = open(storestatus,"w")
        content[k-1]="done"
        for i in range(k):
            fobj.write(content[i])
    else:
        fobj = open(storestatus,"a")
        fobj.write("\ndone")
    fobj.close()



#No book to collect
def zerostatus():
    fobj = open(storestatus,"a")
    fobj.write("0\n\n\ndone")
    fobj.close


#sys.exit()
def WriteError(errornumber):
    x=''
    error = {
      1: lambda x: 'error:1:file opening error',
      2: lambda x: 'error:2:link error',
      3: lambda x: 'error:3:interrupted error'
    }[errornumber](x)

    fobj=open(storestatus,"a")
    fobj.write(error)
    fobj.close
    sys.exit()


#Fetch contents of "filename", return a string
def GetInfoFromFile(filename):
    a=0
    try:
        finfo = file(filename,"r")
        a = 1
    except Exception, e:
        print e
    info = ' '
    if a:
        for line in finfo:
            line = line.replace('\r',' ')
            line = line.replace('\n',' ')
            info +=  line
    return info


def down(url,newname):
    #print ' Downloading ' ,url
    try:
        urllib.urlretrieve(url,newname)
        return 1
    except:
        print (url+" failed.")
        return 0


#Download the files of "url" to "newname"
def url_down(url,newname):
    a=0
    i=1
    while not a:
        while(i>0):
            a=down(url,newname)
            if(a):
                #print url+' download ok'
                info=GetInfoFromFile(newname)
                return info
            else:
                print 'try again '+str(i)
                time.sleep(30)
                i=i+1
        #else:
            #print url+' download error'
            #return 0


#limited times version of "url_down" 
def url_down_limit(url,newname):
    a=0
    i=0
    while not a:
        while(i<20):
            a=down(url,newname)
            if(a):
                print url+' download ok'
                info=GetInfoFromFile(newname)
                return info
            else:
                print 'try again '+str(i)
                time.sleep(30)
                i=i+1
        if i>=20:
            print url+' download error'
            return 0

