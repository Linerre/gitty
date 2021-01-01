#!/usr/bin/env python3

# It seems html.parser's methods can be defined within a class
# in an artbitrary order
# while the parser itself parses html string in the order of
# handle_starttag, handle_data (if any), handle_endtag
from html.parser import HTMLParser
from urllib.request import urlopen

url = urlopen('https://www.economist.com/1843/2020/11/13/tiktok-ology-lessons-from-the-15-second-philosophers')
html = url.read().decode('UTF-8')
url.close()

class Parse(HTMLParser):
    def __init__(self):
    # Since Python 3, we need to call the __init__() function 
    # of the parent class
        # use this counter as a switch
        self.para_counter = 0
        self.paras = []
        super().__init__()
        self.reset()
    
    # Defining what the methods should output when called by HTMLParser.
    def handle_starttag(self, tag, attrs):
        if tag != 'p':
            return 
        # only parse body paras:
        for attr, val in attrs:
            if attr == 'class' and 'article__body-text' in val:
                break
        else:
            return 
        self.para_counter = 1
    
    def handle_endtag(self, tag):
        if tag == 'p' and self.para_counter:
            self.para_counter -= 1

    def handle_data(self, data):
        if self.para_counter:
            self.paras.append(data)

    def get_data(self):
        print(len(self.paras))
        for para in self.paras:
            print(para + '\n')

#test_parse = Parse()
#test_parse.feed(html)
#test_parse.get_data()

class Parse(HTMLParser):
    def __init__(self):
    # Since Python 3, we need to call the __init__() function 
    # of the parent class
        # use this counter as a switch
        self.para_counter = 0
        self.nested_counter = 0
        self.paras = []
        super().__init__()
        self.reset()
    
    # Defining what the methods should output when called by HTMLParser.
    def handle_starttag(self, tag, attrs):
        if tag != 'p' and tag != 'small' and tag != 'em':
            return
        if self.para_counter:
            # because in this case only
            # small or em will be nested
            self.nested_counter += 1
            return
        # only parse body paras:
        for attr, val in attrs:
            if attr == 'class' and 'article__body-text' in val:
                print('Found start tag: ', tag)
                break
        else:
            return
        # if encounter any body para, count 1
        self.para_counter = 1
        print(self.para_counter)
    
    def handle_endtag(self, tag):
        # if such p contains child tag
        # the child tag's data will be read first
        # before the counter reduces to 0 again
        if tag == 'p' and self.para_counter \
            and self.nested_counter:
            self.nested_counter -= 1
            self.para_counter -= 1
        elif tag == 'p' and self.para_counter \
            and not self.nested_counter:
            self.para_counter -= 1
            
            
#         elif (tag == 'em' or tag == 'small') and \
#             self.nested_counter:
#                 self.nested_counter -= 1

    def handle_data(self, data):
        if self.para_counter and \
        not self.nested_counter:
            print('Para counter now is ', self.para_counter)
            print('Append data: ', data)
            self.paras.append(data)
        elif self.nested_counter:
            print('Nested Counter now is ', self.nested_counter)
            self.paras[-1] = self.paras[-1] + data

    def get_data(self):
#         print(len(self.paras))
        for para in self.paras:
            print(para + '\n')
