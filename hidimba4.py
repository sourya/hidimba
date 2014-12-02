#   Version 1 : just substitute the {{ var }} part
#   Version 2 : time to take decisions I - if boolean... (No nesting)
#		(include a fn execif(); edit strip() to include '{%'; 
#		include a global 'start', 'stop' variable to memorise needed index,
#		run_else to store whether 'if' or 'else' will run;
#	Version 3 : life goes round - introducing 'FOR' (an 'if' can be nested)
#	Version 4 : living in nests - introducing nested 'if' and nested 'for'
#
#
global dictpassed, start, stop, symbol, run_else, lines, keys, var_in_for
global ignoreif, ignorefor

def render(filename, dct):
	global index, dictpassed, lines, ignoreif, ignorefor
	ignoreif = False
	ignorefor = False
	index = 0
	
	dictpassed = dct
	result = ""
	
	html = open(filename)
	lines = html.readlines()
	
	while index < len(lines):
		line = lines[index]
		result = result + format(line)
		index += 1
	
	return result
	
def format(line):
	global symbol, index, start, stop, ignoreif, ignorefor, keys, var_in_for

	if '{%' in line and '%}' in line:
		symbol = ['{%', '%}']
		
		if 'if ' in line and 'endif' not in line: # usage is '{% if<space>boolean %}'; what if 'if' is a part of 'endif'
			line = execif(line)
			ignoreif = True
		elif 'else' in line:
			if run_else:
				start = index + 1
			else:
				stop = index - 1
			line = ''
		elif 'endif' in line:
			if run_else:
				stop = index - 1
			ignoreif = False
			line = editlines()
		elif 'for ' in line and 'endfor' not in line:
			start = index + 1
	
			keys = strip(line)[0].split()
			line = ''
			ignorefor = True
		elif 'endfor' in line:
			stop = index - 1
			ignorefor = False
			
			try: 
				loop = dictpassed[keys[3]]
			except KeyError:
				loop = eval(keys[3])
			line = ''
			for i in loop:
				var_in_for = i
				line = line + editlines()
		else:
			pass
	else:
		if ignoreif or ignorefor:
			line = ''
		else:
			line = line
	
	while '{{' in line and '}}' in line:
		symbol = ['{{', '}}']
		line = "\n" + getvar(line)
		
	return line
	
def getvar(line):
	stripped = strip(line)
	var = stripped[0]
	substr = stripped[1]
	
	try:
		line = line.replace(substr, str(dictpassed[var]))
	except KeyError:
		line = line.replace(substr, str(var_in_for))
	return line
	
def execif(line):
	global start, stop, run_else
	start = index + 1
	
	keys = strip(line)[0].split()
	
	if dictpassed[keys[1]]:
		run_else = False # don't execute its else part when 'if' condition is met
	else:
		run_else = True
	return ''
	
def editlines():
	editlines = lines[start:stop+1]
	edited = ""
	for eachline in editlines:
		edited = edited + "\n" + format(eachline)
	
	return edited + "\n"
	
def strip(line):
	index1 = line.index('{')
	index2 = line.index('}') + 1 # in case of }}
	
	if '%' in symbol[0]: # in case of %}
		index2 -= 1
	
	substr = line[index1:index2+1]
	var = substr.replace(symbol[0], '')
	var = var.replace(symbol[1], '')
	var = var.strip()
	
	return (var, substr)

print render('/home/sourya/file.html', {'name': 'Chudree', 'company': 'SyntaxError.com', 'title': 'My Page', 'error': True, 'bought': True})
