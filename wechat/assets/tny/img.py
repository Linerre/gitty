#!\usr\bin\env python3
# -*- coding: utf-8 -*-
# Parse New Yorker's article pages and get the images
# This single module exists solely for getting images
# it also acts as the prototype of the same class in the main 
# `telongreads.py` file

import requests
from pathlib import Path
from html.parser import HTMLParser



class GetImages(HTMLParser):
    def __init__(self):
        super().__init__()
        self.img_recording = 0
        self.img_counter = 0
        self.caption_text_recording = 0
        self.caption_credit_recording = 0
        self.img_srcs = {}

    def handle_starttag(self, tag, attrs):
        if tag == 'img' and ('class', 'responsive-image__image') in attrs:
            self.img_recording += 1
            self.img_counter += 1
            # suppose all img tags are like: <img class="xxx" alt="yyy" src="url">
            self.img_srcs[self.img_counter] = {'src': attrs[2][1]}
        # caption text span
        elif tag == 'span' and ('class' in attrs and 'caption_text' in attrs[1]):
            self.caption_text_recording += 1
        # caption credit span
        elif tag == 'span' and ('class' in attrs and 'caption_credit' in attrs[1]):
            self.caption_credit_recording += 1

    def handle_data(self, data):
        if self.caption_text_recording:
            self.img_srcs[self.img_counter].update(('caption_text', data))
        elif self.caption_credit_recording:
            self.img_srcs[self.img_counter].update(('caption_credit', data))
    
    def handle_endtag(self, tag):
	if self.img_recording:
	  self.img_recording -= 1

