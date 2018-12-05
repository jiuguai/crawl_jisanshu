from scrapy import cmdline
cmdline.execute('scrapy crawl js2'.split())

# lpush js2:start_urls https://www.jianshu.com/trending/monthly?utm_medium=index-banner-s&utm_source=desktop