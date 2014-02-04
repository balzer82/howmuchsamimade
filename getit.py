# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import urllib
import json
import sys
from bs4 import BeautifulSoup
from collections import namedtuple
import matplotlib.pyplot as plt
import numpy as np

# <headingcell level=2>

# Crawl Definitions

# <markdowncell>

# Source: https://gist.github.com/shaurz/6796103
# Thanks!

# <codecell>

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

# <headingcell level=1>

# Main

# <codecell>

if __name__ == "__main__":
    
    if len(sys.argv)==2:
        chname = sys.argv[1]
    else:
        # Channel Name here:
        chname = 'HerrTutorial'        
    
    print('Crawling %s\'s Channel...' % chname)
    videos = get_videos(chname)

    value = 4.0   # $ per 1000 Views
    # source: http://www.googlewatchblog.de/2014/02/sinkende-werbepreise-youtube-stars/
 

# <headingcell level=2>

# Loop through all videos

# <codecell>

    name=[]
    money=[]
    durat=[]
    for video in videos:
        
            if len(video.views)==0:
                print('Keine Views zu dem Video')
                continue
            
            print('%s: %s (%smin)' % (video.title, video.views, video.duration))
            name.append(video.title)
            
            duration=video.duration.split(':')
            duration=60.0*float(duration[0])+float(duration[1])
            
            durat.append(duration)
            
            views = video.views.split()[0]
            views = float(views.replace('.',''))
            money.append(views * value/1000.0)

# <headingcell level=2>

# Statistics

# <codecell>

    smoney = np.sum(money) # in EUR
    sviews = np.sum(views) # in Views
    sdurat = np.sum(durat) # in Seconds
    
    print('==========================================================')
    print('%d Videos with %d Views in %s\'s Channel' % (len(name), sviews, chname))
    print('%d$ so far from YouTube (assuming %d$/1.000 Views)' % (smoney, value))
    print('%s made %d$/Video, %d$/min Video' % (chname, smoney/len(name), smoney/(sdurat/60)))

# <headingcell level=2>

# Chart

# <codecell>

    if (len(name)/2) > 400:
        figheight=400
    else:
        figheight=len(name)/2
        
    fig = plt.figure(figsize=(5,figheight))
    pos = np.arange(len(name))+0.5
    plt.xticks(rotation=45, fontsize=20)
    plt.barh(pos, money, align='center',height=0.8)
    plt.axis('tight')
    plt.yticks(pos, name)
    plt.annotate('{0:,}$'.format(int(smoney)), xy=(0.5, 0.05),
                xycoords='figure fraction',
                horizontalalignment='center', verticalalignment='top',
                fontsize=110,
                color='#FF6700')
    plt.annotate('%d\$/Video, %d\$/min' % (smoney/len(name), smoney/(sdurat/60)),
                 xy=(0.5, 0.035),
                xycoords='figure fraction',
                horizontalalignment='center', verticalalignment='top',
                fontsize=50,
                color='#FF6700')
    plt.xlabel('$')
    plt.title('How much Money \'%s\' made?' % chname)
    plt.savefig('howmuch-%s-made.png' % chname, dpi=72, bbox_inches='tight', transparent=True)
    plt.close()
    print('Done.')

# <codecell>


