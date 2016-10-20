#encoding=utf-8
from bs4 import BeautifulSoup
import socket
import urllib2
import re
import zlib

 class MyCrawler:
     def __init__(self,seeds):
         #Initial current breadth
         self.current_deepth = 1
         #Initial url queue
         self.linkQuence=linkQuence()
         if isinstance(seeds,str):
             self.linkQuence.addUnvisitedUrl(seeds)
         if isinstance(seeds,list):
             for i in seeds:
                 self.linkQuence.addUnvisitedUrl(i)
         print "Add the seeds url \"%s\" to the unvisited url list"%str(self.linkQuence.unVisited)
     #Capture main function
     def crawling(self,seeds,crawl_deepth):
         #If the breadth is less or equal to crawl_deepth
         while self.current_deepth <= crawl_deepth:
             #If the link queue is not empty
             while not self.linkQuence.unVisitedUrlsEnmpy():
                 #Pop front url
                 visitUrl=self.linkQuence.unVisitedUrlDeQuence()
                 print "Pop out one url \"%s\" from unvisited url list"%visitUrl
                 if visitUrl is None or visitUrl=="":
                     continue
                 #Get the link
                 links=self.getHyperLinks(visitUrl)
                 print "Get %d new links"%len(links)
                 #Push to visited url queue
                 self.linkQuence.addVisitedUrl(visitUrl)
                 print "Visited url count: "+str(self.linkQuence.getVisitedUrlCount())
                 print "Visited deepth: "+str(self.current_deepth)
             #Push unvisited url
             for link in links:
                 self.linkQuence.addUnvisitedUrl(link)
             print "%d unvisited links:"%len(self.linkQuence.getUnvisitedUrl())
             self.current_deepth += 1

     #Get the link of source code
     def getHyperLinks(self,url):
         links=[]
         data=self.getPageSource(url)
         if data[0]=="200":
             soup=BeautifulSoup(data[1])
             a=soup.findAll("a",{"href":re.compile('^http|^/')})
             for i in a:
                 if i["href"].find("http://")!=-1:
                     links.append(i["href"])
         return links

     #Get source code
     def getPageSource(self,url,timeout=100,coding=None):
         try:
             socket.setdefaulttimeout(timeout)
             req = urllib2.Request(url)
             req.add_header('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')
             response = urllib2.urlopen(req)
             page = ''
             if response.headers.get('Content-Encoding') == 'gzip':
                 page = zlib.decompress(page, 16+zlib.MAX_WBITS)

             if coding is None:
                 coding= response.headers.getparam("charset")
             if coding is None:
                 page=response.read()
        　　#decode to utf-8
             else:
                 page=response.read()
                 page=page.decode(coding).encode('utf-8')
             return ["200",page]
         except Exception,e:
             print str(e)
             return [str(e),None]

 class linkQuence:
     def __init__(self):
         #visited url
         self.visted=[]
         #unvisited url
         self.unVisited=[]
     #Get the queue of visited queue
     def getVisitedUrl(self):
         return self.visted
     #Get the queue of unvisited queue
     def getUnvisitedUrl(self):
         return self.unVisited
     #Add to visited queue
     def addVisitedUrl(self,url):
         self.visted.append(url)
     #Remove visited url
     def removeVisitedUrl(self,url):
         self.visted.remove(url)
     #Pop unvisited url
     def unVisitedUrlDeQuence(self):
         try:
             return self.unVisited.pop()
         except:
             return None
     #Make sure every url only be visited once
     def addUnvisitedUrl(self,url):
         if url!="" and url not in self.visted and url not in self.unVisited:
             self.unVisited.insert(0,url)
     #Get the number of visited url
     def getVisitedUrlCount(self):
         return len(self.visted)
     #Get the number of unvisited url
     def getUnvistedUrlCount(self):
         return len(self.unVisited)
     #If queue is empty or not
     def unVisitedUrlsEnmpy(self):
         return len(self.unVisited)==0

 def main(seeds,crawl_deepth):
     craw=MyCrawler(seeds)
     craw.crawling(seeds,crawl_deepth)

 if __name__=="__main__":
     main(["http://www.baidu.com", "http://www.google.com.hk", "http://www.sina.com.cn"],10)
