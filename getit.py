# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import urllib
import json
from bs4 import BeautifulSoup
from collections import namedtuple
import matplotlib.pyplot as plt
import numpy as np

# <codecell>

# Source: https://gist.github.com/shaurz/6796103
# Thanks!

Video = namedtuple("Video", "video_id title duration views thumbnail")
 
def parse_video_div(div):
    video_id = div.get("data-context-item-id", "")
    title = div.get("data-context-item-title", "")
    duration = div.get("data-context-item-time", "")
    views = div.get("data-context-item-views", "")
    img = div.find("img")
    thumbnail = "http:" + img.get("src", "") if img else ""
    return Video(video_id, title, duration, views, thumbnail)
 
def parse_videos_page(page):
    video_divs = page.find_all("div", attrs={"data-context-item-type": "video"})
    return [parse_video_div(div) for div in video_divs]
 
def find_load_more_url(page):
    for button in page.find_all("button"):
        url = button.get("data-uix-load-more-href")
        if url:
            return "http://www.youtube.com" + url
 
def download_page(url):
    #print("Downloading {0}".format(url))
    return urllib.urlopen(url).read()
 
def get_videos(username):
    page_url = "http://www.youtube.com/user/{0}/videos".format(username)
    page = BeautifulSoup(download_page(page_url))
    videos = parse_videos_page(page)
    page_url = find_load_more_url(page)
    while page_url:
        json_data = json.loads(download_page(page_url))
        page = BeautifulSoup(json_data.get("content_html", ""))
        videos.extend(parse_videos_page(page))  
        page_url = find_load_more_url(BeautifulSoup(json_data.get("load_more_widget_html", "")))
    return videos
 
if __name__ == "__main__":
    
    # Channel Name here:
    chname = 'HerrTutorial'
    
    videos = get_videos(chname)

    value = 4.0   # € per 1000 Views
    # source: http://www.googlewatchblog.de/2014/02/sinkende-werbepreise-youtube-stars/
    
    name=[]
    money=[]
    for video in videos:
            name.append(video.title)
            
            views = video.views.split()[0]
            views = float(views.replace('.',''))
            money.append(views * value/1000.0)
    
    su = np.sum(money)
    print('%dEUR so far from YouTube' % su)
    
    
    fig = plt.figure(figsize=(5,len(name)/2))
    pos = np.arange(len(name))+0.5
    plt.barh(pos, money, align='center',height=0.8)
    plt.axis('tight')
    plt.yticks(pos, name)
    plt.annotate(u'ca. %dEUR' % su, xy=(0.95, 0.05),
                xycoords='figure fraction',
                horizontalalignment='right', verticalalignment='top',
                fontsize=100,
                color='#FF6700')
    plt.xlabel('$EURO$')
    plt.title('How much Money \'%s\' made?' % chname)
    plt.savefig('howmuch-%s-made.png' % chname, dpi=72, bbox_inches='tight', transparent=True)
    plt.close()

# <codecell>


# <codecell>


# <codecell>


