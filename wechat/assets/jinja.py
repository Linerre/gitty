#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

print(env.list_templates(extensions=["html"]))
    #TODO
    # figure out how this 'parent' argument works
    # and let the lookup order goes deeper
template = env.get_template('te-base.html')

output = template.render()
print('output is', output)
	#with open('test.html', 'w', encoding='utf-8') as test:
	#	test.write(output)
