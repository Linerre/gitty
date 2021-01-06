
#!/usr/bin/env python3

# scrape a article page from TE's 1843 long reads
# Three classes to get paragraphs, header, and images respectively

# It seems html.parser's methods can be defined within a class
# in an artbitrary order
# while the parser itself parses html string in the order of
# handle_starttag => handle_data (if any) => handle_endtag
import requests
from sys import argv
from html.parser import HTMLParser
from urllib.request import urlopen


url = urlopen(argv[1])
html = url.read().decode('UTF-8')
url.close()

class GetBody(HTMLParser):
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
            self.paras[-1] = self.paras[-1] + data

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


class GetHeader(HTMLParser):
    def __init__(self):
        self.record_subheadline = 0
        self.record_headline = 0
        self.record_description = 0
        self.header = []
        # in Python 2
        # super(Parser, self).__init__()
        # in Python 3, though Python 2 style also applies 
        super().__init__()
        #self.reset()

    def handle_starttag(self, tag, attrs):
        for attr, val in attrs:
            # count subheadline, headline, description respectively
            if attr == 'class' and val == 'article__subheadline':
                self.record_subheadline += 1
                break
            elif attr == 'class' and val == 'article__headline':
                self.record_headline += 1
                break
            elif attr == 'class' and val == 'article__description':
                self.record_description += 1
                break
        else:
            return


    def handle_endtag(self, tag):
        if tag == 'span' and self.record_subheadline:
            self.record_subheadline -= 1
        elif tag == 'span' and self.record_headline:
            self.record_headline -= 1
        elif tag == 'p' and self.record_description:
            self.record_description -= 1

    def handle_data(self, data):
        if self.record_headline or \
           self.record_subheadline or \
           self.record_description:
            self.header.append(data)

    def get_header(self):
        return self.header

    def process_header(self):
        if len(self.header) == 3:
            self.header[0] = '<h2 class="tel-col">' + self.header + '</h2>'
            self.header[1] = '<h1 class="tel-title">' + self.header + '</h1>'
            self.header[2] = '<h3 class="tel-subtitle">' + self.header + '</h3>'
            return self.header
        else:
            print('Header has more than 3 elements.')

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
                if i == 0:
                    #TODO
                    # use os to make sure img exists or create it if it doesn't
                    with open(f'{path}/header-img.{self.img_srcs[i][-3:]}', 'wb') as img: 
                        img.write(r.content)
                else:
                    with open(f'{path}/body-{i}.{self.img_srcs[i][-3:]}', 'wb') as img:
                        img.write(r.content)
