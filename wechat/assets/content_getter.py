from html.parser import HTMLParser
from urllib.request import urlopen

url = urlopen('https://www.economist.com/1843/2020/11/13/tiktok-ology-lessons-from-the-15-second-philosophers')
html = url.read().decode('UTF-8')
url.close()

class Parse(HTMLParser):
    def __init__(self):
    # Since Python 3, we need to call the __init__() function 
    # of the parent class
        super().__init__()
        self.reset()
    
    # Defining what the methods should output when called by HTMLParser.
    def handle_starttag(self, tag, attrs):
        # only parse body paras:
        if tag == 'p':
            for attr, val in attrs:
                if attr == 'class' and val == 'article__body-text':
                    print(f'Encounter body {tag} with class name {val}')
                    self.Parse_para.handle_data(data)

    class Parse_para(HTMLParser):
        """Inner class to avoid arbitrarily extract text nodes"""

        def handle_data(self, data):
            print(data)



test_parse = Parse()
test_parse.feed(html)
