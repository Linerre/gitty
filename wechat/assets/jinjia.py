from jinja2 import Environment, FileSystemLoader

try:
	file_loader = FileSystemLoader('templates/')
	env = Environment(loader=file_loader)

	template = env.get_template('te-1843-base.html')

	output = template.render()
	print(output)
	with open('test.html', 'w', encoding='utf-8') as test:
		test.write(output)
except Exception as error:
	print(error)