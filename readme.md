How Much xxx Made on YouTube
==========
Based on the money per view, payed on YouTube, this script crawls the views of a channel and calculates the money earned from the business
----------

# How?

Get the channel name from http://www.youtube.com/user/xxx and fire the request with

`python getit.py xxx`

It will produce following result.


# Result


```
Crawling HerrTutorial's Channel...
SAMi's MUST HAVES im JANUAR: Beauty, Fashion, Lifestyle, Technik + VERLOSUNG!!: 106.611 Aufrufe (11:30min)
WHAT'S ON MY iPHONE 5S!? & Wie ich meine Fotos bearbeite! + OUTTAKES!: 167.772 Aufrufe (11:45min)
3 DIY GESUNDE ESSENS-IDEEN für die SCHULE/Arbeit/Zu Hause in 10 Minuten! + OUTTAKES!: 151.363 Aufrufe (8:45min)
...
..
.
==========================================================
318 Videos with 90949037 Views in HerrTutorial's Channel
363796$ so far from YouTube (assuming 4$/1.000 Views)
HerrTutorial made 1144$/Video, 114$/min Video, 0.004000$/view
```

And you have this Bar Chart, showing all videos with earned money:

![Bargraph](https://raw.github.com/balzer82/howmuchsamimade/master/howmuch-HerrTutorial-made.png)

with the assumption of 4$/1000Views, mentioned in [this](http://www.googlewatchblog.de/2014/02/sinkende-werbepreise-youtube-stars/) article.

# Thanks to

[shaurz](https://gist.github.com/shaurz/6796103) for the YouTube Beautifulsoup

# Dependencies

- Beautifulsoup
- Numpy
- Matplotlib
