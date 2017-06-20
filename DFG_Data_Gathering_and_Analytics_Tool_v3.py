import gnp
import codecs
import json
from pprint import pprint
import csv
import PyPDF2
import argparse
#To get the latest development version you can download the source code running:
#   git clone https://github.com/reingart/pyfpdf.git
#   cd pyfpdf
#   python setup.py install
#You can also install PyFPDF from PyPI, with easyinstall or from Windows installers. For example, using pip:
#   pip install fpdf
import fpdf
import textwrap
import feedparser
from bs4 import BeautifulSoup
from tabulate import tabulate
import datetime
from twitter import *
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
#-----------------------------------------------------------------------
# load your Twitter API credentials 
#-----------------------------------------------------------------------
config = {"access_key":"113701493-Pwv4zT3EiIvcU0b9JPmVczNCUS0CYTmkCBfo3Tup","access_secret":"e5WI3wq3P1HA8B8WNofl68hozcAThgtye9mtPExdyEY8S",
"consumer_key":"4OuVn79LRAi77XKegbMsWBtHx","consumer_secret":"Rc0gexwmJlClkJpiKvn4GGhFzjXPj8dX9LqO4tTikr0l8wme2G"}
twitter = Twitter(auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))
#-----------------------------------------------------------------------
# Set Youtube DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyBf9l972dS9ezI3S3uD6AdneIrFsFUhLW0"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def RSSFeed(options):
        feedparse = feedparser.parse('http://news.google.co.in/?output=rss')
        length = len(feedparse.entries)
        keyword = options.q.lower()
        count = 0
        rssfeed=[]
        dictionary={}
        for num in range(0,length):
                if keyword in feedparse.entries[num].title.lower():
                        dictionary["Title"] = feedparse.entries[num].title
                        dictionary["Link"] = feedparse.entries[num].link
                        dictionary["Time and Date"] = feedparse.entries[num].published
                        dictionary["Description"] = BeautifulSoup(feedparse.entries[num].description,'lxml').get_text()
                        dictionary["News ID"] = feedparse.entries[num].id
                        count = count + 1
                        rssfeed.append(dictionary)
        if count == 0:
                dictionary["Title"]='No News Found'
                rssfeed.append(dictionary)
        return rssfeed

def RSSPdf(data):
        pdf = fpdf.FPDF(format='letter')
        pdf.add_page()
        pdf.set_font("Arial", size=8)
        separator = 200*'-'
        for i in range(len(data)):
                feed=data.pop()
                for key, value in feed.iteritems():
                        meta = key.upper()+' - '+value
                        pdf.cell(0, 10, txt=meta, ln=1, align="L")
                pdf.cell(0, 10, txt=separator, ln=1, align="C")
        print "Created Output File: ",Keyword+'_'+"RSSnews.pdf"
        pdf.output(Keyword+'_'+"RSSnews.pdf")

def GNcreatepdf(data):
        pdf = fpdf.FPDF(format='letter')
        pdf.add_page()
        pdf.set_font("Arial", size=8)
        separator = 200*'-'
        for i in range(len(data)):
                for key, value in data[i].iteritems():
                        meta = key.upper()+' - '+value
                        pdf.cell(0, 10, txt=meta, ln=1, align="L")
                pdf.cell(0, 10, txt=separator, ln=1, align="C")
        print "Created Output File: ",Keyword+'_'+"Googlenews.pdf"
        pdf.output(Keyword+'_'+"Googlenews.pdf")

def google_news(options):
        c = gnp.get_google_news_query(q = options.q)
        category = c['meta']
        stories = c['stories']
        return stories #Return dictionary

                
def twitter_search(options):
        query = twitter.search.tweets(q = options.q)
        return query

def YTcreatepdf(data):
        pdf = fpdf.FPDF(format='letter')
        pdf.add_page()
        pdf.set_font("Arial", size=8)
        separator = 200*'-'
        for i in data:
                for j in range(len(i)):
                        for key, value in i[j].iteritems():
                                try:
                                        meta = key.upper()+"-"+str(value).encode("iso-8859-15", "xmlcharrefreplace")
                                except UnicodeEncodeError:
                                        meta = key.upper() + " - " + value.encode("iso-8859-15", "ignore")
                                pdf.cell(0, 10, txt=meta, ln=1, align="L")
                        pdf.cell(0, 10, txt=separator, ln=1, align="C")
                pdf.cell(0, 10, txt=200*'*', ln=1, align="C")
        print "Created Output File: ", Keyword+'_'+"YouTubeData.pdf"
        pdf.output(Keyword+'_'+"YouTubeData.pdf")


def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)
  search_response = youtube.search().list(q=options.q,part="id,snippet",maxResults=options.max_results).execute()
  videos = {}
  videolist = []
  channels = {}
  channellist=[]
  playlists = {}
  playlistlist=[]
  alldata=[]
  for search_result in search_response.get("items", []):
    comment_count =  0
    view_count = 0
    fav_count = 0
    disliket_count = 0
    like_count = 0
    if search_result["id"]["kind"] == "youtube#video":
      Video_stat=youtube.videos().list(id=search_result["id"]["videoId"],part="id,statistics").execute()
      if len(Video_stat["items"][0])>0:
        s = Video_stat["items"][0]["statistics"].keys()
        for i in s:
            if i == "commentCount": comment_count = Video_stat["items"][0]["statistics"][i]
            if i == "viewCount": view_count = Video_stat["items"][0]["statistics"][i]  
            if i == "favoriteCount": fav_count = Video_stat["items"][0]["statistics"][i]
            if i == "dislikeCount": disliket_count = Video_stat["items"][0]["statistics"][i]
            if i == "likeCount":  like_count = Video_stat["items"][0]["statistics"][i] 
        videos["Title"] = search_result["snippet"]["title"]
        videos["Video_ID"] = search_result["id"]["videoId"]
        videos["Publication Date"] = search_result["snippet"]["publishedAt"]
        videos["Channel Title"] = search_result["snippet"]["channelTitle"]
        videos["Channel ID"] = search_result["snippet"]["channelId"]
        videos["Description"] = search_result["snippet"]["description"]
        videos["Live Broadcasting"] = search_result["snippet"]["liveBroadcastContent"]
        videos["Comment Count"] = comment_count
        videos["View Count"] = view_count
        videos["Favourite Count"] = fav_count
        videos["Dislikes"] = disliket_count
        videos["Likes"] = like_count
        videolist.append(videos)
      videos={}
    elif search_result["id"]["kind"] == "youtube#channel":
      Video_stat=youtube.videos().list(id=search_result["id"]["channelId"],part="id,statistics").execute()
      channels["Title"] = search_result["snippet"]["title"]
      channels["Channel ID"] = search_result["id"]["channelId"]
      channels["Published At"] = search_result["snippet"]["publishedAt"]
      channels["Channel Title"] = search_result["snippet"]["channelTitle"]
      channels["Decription"] = search_result["snippet"]["description"]
      channels["Live Broadcasting"] = search_result["snippet"]["liveBroadcastContent"]
      channellist.append(channels)
      channels={}
    elif search_result["id"]["kind"] == "youtube#playlist":
      Video_stat=youtube.videos().list(id=search_result["id"]["playlistId"],part="id,statistics").execute()
      playlists["Title"] = search_result["snippet"]["title"]
      playlists["Playlist ID"] = search_result["id"]["playlistId"]
      playlists["Published At"] = search_result["snippet"]["publishedAt"]
      playlists["Channel Title"] = search_result["snippet"]["channelTitle"]
      playlists["Channel ID"] = search_result["snippet"]["channelId"]
      playlists["Decription"] = search_result["snippet"]["description"]
      playlists["Live Broadcasting"] = search_result["snippet"]["liveBroadcastContent"]
      playlistlist.append(playlists)
      playlists={}
  alldata.append(videolist)
  alldata.append(channellist)
  alldata.append(playlistlist)
  return alldata



def twitterPDF(data,pdf):
      global TwitterList
      ignore = [None,False,'0','',[],'none','',True,"profile_sidebar_fill_color","profile_sidebar_border_color",'indices',"profile_sidebar_background_color","profile_background_color","profile_link_color",'resize','fit','w','h','profile_text_color']
      for k, v in data.iteritems():
                if k not in ignore:
                        try:
                                if isinstance(v, list) and v != [] and v!=None:
                                        for i in range(len(v)):
                                                twitterPDF(v.pop(),pdf)
                        except:
                                if k not in ignore:
                                        try:
                                                meta = k.upper()+"-"+str(v).encode("iso-8859-15", "xmlcharrefreplace")
                                        except UnicodeEncodeError:
                                                try:
                                                        meta = k.upper() + " - " + v.encode("iso-8859-15", "ignore")
                                                except UnicodeDecodeError:
                                                        meta = k.upper() + " - " + (v.encode("iso-8859-15", "ignore")).decode('ascii','ignore')
                                        pdf.cell(0, 10, txt=meta, ln=1, align="L")
                        if isinstance(v, dict):
                                twitterPDF(v,pdf)
                        else:
                                if v not in ignore and k not in ignore:
                                        try:
                                                meta = k.upper()+"-"+str(v).encode("iso-8859-15", "xmlcharrefreplace")
                                        except UnicodeEncodeError:
                                                try:
                                                        meta = k.upper() + " - " + v.encode("iso-8859-15", "ignore")
                                                except UnicodeDecodeError:
                                                        meta = k.upper() + " - " + (v.encode("iso-8859-15", "ignore")).decode('ascii','ignore')
                                        pdf.cell(0, 10, txt=meta, ln=1, align="L")

def TWcreatepdf(data):
        global TwitterList
        pdf = fpdf.FPDF(format='letter')
        pdf.add_page()
        pdf.set_font("Arial", size=8)
        separator = 200*'-'
        for result in data["statuses"]:
                twitterPDF(result,pdf)
                pdf.cell(0, 10, txt=separator, ln=1, align="C")
        print "Created Output File: ", Keyword+'_'+"Twitter.pdf"
        pdf.output(Keyword+'_'+"Twitter.pdf")



if __name__ == "__main__":
  global Keyword
  argparser = argparse.ArgumentParser(description='Social Media Information Gathering Tool')
  argparser.add_argument("-q", help="Search keyword. Space and special character separated by \ ",required=False)
  argparser.add_argument("-max_results", help='Maximum number of search. \n Standard and default is 50.', default=50)
  argparser.add_argument("-output", help="The output file format such as xlsx, csv, txt, pdf, doc.\n Default is PDF.", default='pdf')
  args = argparser.parse_args()
  if args.q != None:
        print "The search keyword is: %s" % args.q
  elif args.q == None:
        args.q  = str(raw_input("Search Keyword:   "))
  googlenews={}
  timestamp=str(datetime.datetime.now())
  Keyword = args.q+'_'+timestamp
  try:
    youtubedata = youtube_search(args)
    print "Youtube Unstructured Data:", youtubedata     
    twitterdata=twitter_search(args)
    print "Twitter Unstructured Data:", twitterdata  
    googlenews = google_news(args)
    print "Google News Unstructured Data:", googlenews
    rssfeed = RSSFeed(args)
    print "RSS Feed Unstructured Data:", rssfeed
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
  FileType = (args.output).lower()
  if FileType == 'pdf':
          YTcreatepdf(youtubedata)#[List[List{Dictionary}]]
          GNcreatepdf(googlenews)
          TWcreatepdf(twitterdata)
          RSSPdf(rssfeed) #List of dictionary
  '''elif FileType == 'csv':
          createpdf(googlenews)
  elif FileType == 'txt':
          createpdf(googlenews)
  elif FileType == 'doc':
          createpdf(googlenews)
  elif FileType == 'xlsx':
          createpdf(googlenews)
  else: # Default is PDF
          GNcreatepdf(googlenews)'''

