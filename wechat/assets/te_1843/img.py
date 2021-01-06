#!\usr\bin\env python3

# Parse 1843 article pages and get the images
# This single module exists solely for getting images
# it also acts as the prototype of the same class in the main 
# `telongreads.py` file

import requests
from pathlib import Path
from html.parser import HTMLParser
from urllib.request import urlopen


class GetImage(HTMLParser):
    def __init__(self):
        super().__init__()
        self.recording = 0
        self.img_srcs = []

    def handle_starttag(self, tag, attrs):
        # outmost layer
        if (tag == 'div' and ('class', 'article__lead-image') in attrs) or \
            (tag == 'figure' and ('data-image-nozoom', 'true') in attrs):
            self.recording += 1
        # enter the outmost layer
        # and count the second
        if self.recording:
            if (tag == 'div' and ('itemprop', 'image') in attrs):
                self.recording += 1
        # reach the innermost layer: img
        if self.recording == 2 and tag == 'img':
            for attr, val in attrs:
                if attr == 'src':
                    self.img_srcs.append(val)

    def handle_endtag(self, tag):
        if (tag == 'div' or tag =='figure') and self.recording:
            self.recording -= 1 

    def get_result(self):
        print(self.img_srcs)
        return

    def store_imgs(self, path):
        with requests.Session() as s: 
            for i in range(len(self.img_srcs)):
                r = s.get(self.img_srcs[i]) 
                if i == 0 and Path(path).exists():
                    #TODO
                    # use os to make sure img exists 
                    with open(f'{path}/header-img.{self.img_srcs[i][-3:]}', 'wb') as img: 
                        img.write(r.content)
                else:
                    # or create it if it doesn't
                    Path('img').mkdir()
                    with open(f'{path}/body-{i}.{self.img_srcs[i][-3:]}', 'wb') as img:
                            img.write(r.content)



#url = urlopen(argv[1])
#html = url.read().decode('UTF-8')
#url.close()
#test = GetImage()
#test.feed(html)
#test.get_result()
#test.store_imgs('img')
