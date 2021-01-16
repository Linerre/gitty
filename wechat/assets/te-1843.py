#!/usr/bin/env python3

# Parse te 1843 article pages:
# headlines, paragraphs, imgs

from urllib.request import urlopen
from te import te_parser as te
from sys import argv
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
import os.path

project_dir = 'C:\\Users\\zl37\\projects\\gitty\\wechat'
article_url = argv[1]
article_dir = os.path.join(project_dir, str(argv[2])) 
article_til = argv[3]

try:
    # prepare html to feed
    url = urlopen(article_url)
    html = url.read().decode('UTF-8')
    url.close()
    

    # prepare the article parser
    te_article_header = te.GetHeader()
    te_article_body = te.GetBody()
    te_article_img = te.GetImage()

    # scrape needed parts 
    te_article_header.feed(html)
    te_article_body.feed(html)
    te_article_img.feed(html)
    
    # create header template
    # header
    headers = te_article_header.process_header()  # a list
    with open(article_dir + article_til + '\\header.html', 'w', encoding='utf-8') as h:
        for header in headers:
            h.write(header)


    # body
    paras =  te_article_body.process_data()  # a list
    with open(article_dir + article_til + '\\body.html', 'w', encoding='utf-8') as b:
        for para in paras:
            b.write(para)

    # img
    te_article_img.download_imgs(article_dir+article_til+'\\img')



except Exception as error:
    logger.exception(error)
