#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader
from sys import argv

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

print(env.list_templates(extensions=["html"]))
    #TODO
    # figure out how this 'parent' argument works
    # and let the lookup order goes deeper
    # FileSystemLoader will also load templates in subdirectories
    # but it recognizes those templates as they are: /path/to/template
    # if parent='string' given, then it would be string/path/to/template
    # which in turn leads TemplateNotFound error

    # better to keep templates in the same folder at the same depth
template = env.get_template('te-base.html')

output = template.render(title='Tiktok')
print('output is', output)
with open('test.html', 'w', encoding='utf-8') as test:
    test.write(output)
