#!/usr/bin/env python3

# scrape a article page from TE's 1843 long reads
# and collect all the paragraphs, including the photographer's bio

# It seems html.parser's methods can be defined within a class
# in an artbitrary order
# while the parser itself parses html string in the order of
# handle_starttag => handle_data (if any) => handle_endtag

from sys import argv
from html.parser import HTMLParser
from urllib.request import urlopen


url = urlopen(argv[1])
html = url.read().decode('UTF-8')
url.close()

class Parse(HTMLParser):
    def __init__(self):
    # Since Python 3, we need to call the __init__() function 
    # of the parent class
        # use this counter as a switch
        self.para_counter = 0
        self.nested_counter = 0
        # List is not empty to let the first dropped letter
        # have an achor to attach itself to
        # otherwise it will try to find list[-1] of an empty list
        self.paras = ['']
        super().__init__()
        self.reset()
    
    # Defining what the methods should output when called by HTMLParser.
    def handle_starttag(self, tag, attrs):
        # small and em tag to handle a few TE styled words
        # span tag to specifically handle the EOF, a square
        if tag != 'p' and tag != 'small' and tag != 'em' and tag != 'span' and tag != 'strong':
            return
        if self.para_counter:
            # because in the case of TE 
            # only small or em or span or strong will be nested
            self.nested_counter += 1
            return
        # only parse body paras:
        for attr, val in attrs:
            if attr == 'class' and 'article__body-text' in val:
                break
        else:
            return
        # if encounter any body para, count 1
        self.para_counter = 1
    
    def handle_endtag(self, tag):
        # if such p contains child tag
        # the child tag's data will be read first
        # before the counter reduces to 0 again
        if tag == 'p' and self.para_counter and self.nested_counter:
            self.nested_counter -= 1
            self.para_counter -= 1
        elif tag == 'p' and self.para_counter and not self.nested_counter:
            self.para_counter -= 1

    def handle_data(self, data):
        if self.para_counter and not self.nested_counter:
            self.paras.append(data)
        elif self.nested_counter:
            try:
                self.paras[-1] = self.paras[-1] + data
            except Exception:
                print(Exception)

    def get_data(self):
#         print(len(self.paras))
        return self.paras 


    def process_data(self):
        for i in range(len(self.paras)):
            if len(self.paras[i]) == 1 and i < len(self.paras) - 1:
                self.paras[i+1] =  '<span class="te-drop">' + self.paras[i] + '</span>' \
                                + self.paras[i+1]
            else:
                self.paras[i] = '<p class="tel-p">' + self.paras[i] + '</p>'
        return self.paras


test_parse = Parse()
test_parse.feed(html)
print(test_parse.get_data())
with open('te-1843-body.html', 'w', encoding='utf-8') as body:
    for para in test_parse.process_data():
        body.write(para+'\n\n')