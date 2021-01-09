#!/usr/bin/env python3
# get tny header part of personal history articel page


from urllib.request import urlopen
from html.parser import HTMLParser

class GetHeader(HTMLParser):
    def __init__(self):
        self.counter = 0
        self.nested = 0
        self.content = {}
        super().__init__()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            if 'class' in attrs[0] and 'rubric__link' in attrs[0][1]:
                print(attrs)
                self.counter += 1
        #if tag == 'a' and ('class' in attrs and 'rubric__link' in attrs):
        #    self.counter = 1
        if self.counter and tag == 'span':
            self.nested += 1


    def handle_data(self, data):
        if self.counter and self.nested:
            if 'personal_history' not in self.content:
                self.content['personal_history'] = data
            elif 'issue' not in self.content:
                self.content['issue'] = data

    def handle_endtag(self, tag):
        if self.counter and self.nested:
            self.nested -= 1
        if self.counter and not self.nested:
            self.counter -= 1

    def GetContent(self):
        return self.content
    
url = urlopen('https://www.newyorker.com/magazine/2019/11/25/my-life-as-a-child-chef')
html = url.read().decode('UTF-8')
url.close()

test = GetHeader()
test.feed(html)
print(test.GetContent())
