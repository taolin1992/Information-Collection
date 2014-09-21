# -*- encoding=utf-8 -*-
#__author__ = 'Tao Lin'
#!/user/bin/python2.7
# Filename : helloword.py

import urllib
import os
import re
import socket
import msvcrt
import time
import datetime
import priscommon
import sys   
reload(sys)   
sys.setdefaultencoding('utf8') 

print 'Hello word'

#Time out for if urllib.down() doesn't work for 400 seconds
socket.setdefaulttimeout(400)



def filename(a1,tag=0):
    if tag==0:
        return "lib.mlpla.htm"
    if tag==1:
        return "mlpla_detail.htm"
    if tag==2:
        return "mlpla_marc.htm"


#Generator Expression to strip the part between "<" and ">"
def stripTags(s):
    intag = [False]
    def chk(c):
        if intag[0]:
            intag[0] = (c != '>')
            return False
        elif c == '<':
            intag[0] = True
            return False
        return True
    return ''.join(c for c in s if chk(c))


#Write the recording files
def writefile(sn,sss,num,p,i):
    #write file
    f=file("_"+sn+".txt","a")
    #print sss
    f.write (str(num)+","+str(p)+","+str(i)+"\r\n")
    f.write(sss)
    f.write ("\r\n")
    f.close


#Write the xbr.txt
def writexbfile(sn,p,i):
    #write file
    f=file("xbr.txt","w")
    #print sss
    f.write (sn+" "+str(p)+" "+str(i))
    f.close


#dn = 'opac.lib.dlut.edu.cn'
def RunCrawler(sn, dn, pagenumber, itemnumber):
    priscommon.addcreatestatusfile()
    preface='http://'+dn+'/opac/'#preface='http://opac.lib.dlut.edu.cn/opac/'
    #http://opac.lib.dlut.edu.cn/opac/
    #             openlink.php?strSearchType=callno&match_flag=forward&historyCount=1&strText=T              &doctype=ALL&displaypg=20&showmode=list&sort=CATA_DATE&orderby=desc&dept=ALL
    url1=preface+'openlink.php?strSearchType=callno&match_flag=forward&historyCount=1&strText='+sn+'&doctype=01&displaypg=20&showmode=list&sort=CATA_DATE&orderby=desc&dept=ALL'
    fn1=filename(url1)  #fn1='lib.dlut.htm'
    b=priscommon.url_down(url1,fn1)#To obtain the number of books of call number T
    if(b):
        reg1='检索到 <strong.*?>(.*?)</strong>'
        p1 = re.compile(reg1)
        m1 = p1.findall(b)
        booknumber = 0
        if m1:
            count=int(m1[0])
            booknumber = count
            writebooknumber(sn,booknumber)
            print 'book number: '+str(count)
            page=int(count/20)#pages in total
            if count%20 != 0:
                page=page+1
            priscommon.createstatusfile(str(count))
            num=0   #current number of items
            pnum=0  #current number of pages
            for i in range(page):#page loop
                pnum=pnum+1
                i = i+1
                if (i<int(pagenumber)):
                    continue
                pagenumber = 0
                #url1 points to the page xbr.txt records
                url1=preface+'openlink.php?dept=ALL&callno='+sn+'&doctype=01&lang_code=ALL&match_flag=forward&displaypg=20&showmode=list&orderby=DESC&sort=CATA_DATE&onlylendable=no&count='+str(count)+'&with_ebook=&page='+str(i)        
                fn1 = filename(url1)
                print str(i)+': get list page.'
                c = priscommon.url_down(url1,fn1)
                if c:
                    #c=c.encode("gbk",'ignore')
                    reg1='<h3><span>.*?</span><a\shref="(.*?)"\s+>\d+.(.*?)</a>\s*(.*?)</h3>.*?</span>\s*(.*?)<br\s/>\s*(.*?)&nbsp;(.*?)\s*<br />'
                    p1 = re.compile(reg1)
                    m = p1.findall(c)#m is the 20 items on one page
                    if m:
                        jishu=0
                        for g in m:#item loop of 20 items
                            url2=g[0]
                            print 'detail page url: '+url2
                            url=preface+url2 # url = 'http://opac.lib.dlut.edu.cn/opac/item.php?marc_no=2014004965'pointing to the detailed page of the first book
                            jishu=jishu+1
                            if (jishu < int(itemnumber)):
                                continue
                            itemnumber = 0 #return to zero
                            writexbfile(sn, pnum, jishu)
                            fn = filename(url,1)#fn = 'dlut_detail.htm'
                            #get detail page.
                            num = num+1
                            info = priscommon.url_down(url,fn)
                            
                            marcurl=''
                            if info:
                                regC='<a\shref="([a-zA-Z0-9._?=]*?)"\stitle="marc_format">'
                                pC=re.compile(regC)
                                nC=pC.findall(info)
                                if nC:
                                    for gC in nC:
                                        marcurl=gC #marcurl = 'show_format_marc.php?marc_no=52315564573702315530013555320166033b0367' pointing to the mar address of the first book
                                        break
                            if marcurl!='':
                                print "All:"+str(booknumber)+","+"Cur:"+str((pnum-1)*20+jishu)+","+str(num)+",p("+str(pnum)+"),i("+str(jishu)+") marc url: "+marcurl
                                info = priscommon.url_down(preface + marcurl,filename(url,2))
                                                            
                                if info:#obtain the detailed information
                                    #info = info.decode()
                                    #print info
                                    marc = info[info.find("(MARC)")+6:]                                    
                                    #writefile(marc,1)                                                                        
                                                                        
                                    marc = marc.replace('</li>',chr(30))#chr(30) is blank space
                                    marc = " ".join(stripTags(marc).split())#a.split() removes all the blank spaces in "a"
                                    #print marc
                                    #writefile(marc,2)                                                                        
                                    #marc=priscommon.changecode(marc)   
                                    p=marc.replace(';','')
                                    k = p.replace('&#x','\u')
                                    #print k
                                    k1 = k.decode('unicode-escape')
                                                                                                     
                                    writefile(sn, k1, num, pnum, jishu)
                                    #print k1
                                    
                                    #priscommon.SaveContent(title,author,press,year,ISBN,CNumber,num,'0')
                            else:
                                priscommon.WriteError(3)
                            time.sleep(3)
                        if pnum != page and jishu != 20:#record the page
                            priscommon.failestatusfilep(pnum)
                else:
                    priscommon.WriteError(3)
            if pnum==page:
                priscommon.finishstatusfile()
        else:
            print "no books."
            priscommon.zerostatus()#no books to collect
            writebooknumber(sn,0)
    else:
        priscommon.WriteError(2)
   
#Write down the book number
def writebooknumber(sn,booknumber):
    f=file("booknum.csv","a")
    f.write(sn+","+str(booknumber)+"\r\n")
    f.close()
    

def GetAllSequence():
    arr = []
    i = 0
    while i<10:
       cn=chr(ord('0')+i)
       arr.append(cn)
       i = i + 1
    i = 0
    while i<26:
       cn=chr(ord('A')+i)
       arr.append(cn)
       i = i + 1
    return arr


def main():
    domain_name='opac.lib.dlut.edu.cn'
    # 'sn page itemofpage'
    lines='0 1 1'
    try:
        f=file("xbr.txt","r")
        lines1 = f.readlines(1)
        lines = lines1[0]
        f.close()
    except:
        print 'xbr.txt read error.'
    
    number = lines.split(' ')
    sn = number[0]
    pagenumber = number [1]
    itemnumber = number [2]
    print "SN:"+sn+" Pagenumber:"+pagenumber+" Itemnumber:"+itemnumber
    
    arr = GetAllSequence()
    
    for i in arr:
        print "sn:"+i
        if (i<sn):
            continue
        RunCrawler(i, domain_name, pagenumber, itemnumber)

main()
