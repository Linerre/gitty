#!/usr/bin/env python3

# Use self-made pakcage to parse 1843 article pages:
# headlines, paragraphs, imgs

from urllib.request import urlopen
from te_1843 import img
from sys import argv
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

try:
    url = urlopen(argv[1])
    html = url.read().decode('UTF-8')
    url.close()

    test_parse = img.GetImage()
    test_parse.feed(html)
    test_parse.store_imgs('img')
except Exception as error:
    logger.exception(error)
