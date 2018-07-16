import ply.lex as lex
import ply.yacc as yacc
import sys

jsonToParse = sys.stdin.read()

tokens = ( 'LLAVEIZQ','LLAVEDER', 'CORCHEIZQ','CORCHEDER','COMA','DOSPUNTOS','STRING', 'NUMBER','TRUE', 'FALSE', 'NULL' )

# Tokens
t_LLAVEIZQ = r'\{'
t_LLAVEDER = r'\}'
t_CORCHEIZQ = r'\['
t_CORCHEDER = r'\]'
t_COMA = r','
t_DOSPUNTOS = r':'
t_TRUE = r'true'
t_FALSE = r'false'
t_NULL = r'null'
t_NUMBER = r'-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?'
t_STRING = r'\"((?=\\)\\(\"|\/|\\|b|f|n|r|t|u[0-9a-zA-Z]{4})|[^\\"]*)*\"'

t_ignore = " \t"

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

def t_error(t):
	raise Exception("NO SE PUDO TOKENIZAR CORRECTAMENTE EL JSON")

lexeer = lex.lex()

class TokenWithAttributes:
	def __init__(self, yaml, claves):
		self.yaml = yaml
		self.claves = claves

start = 'first'

def p_first(p):
	'first : value'
	parsedValue = p[1]
	f = open("result.txt", "w")
	f. write("---" + parsedValue.yaml(-1))
	f.close()
	print("---" + parsedValue.yaml(-1))
	p[0] = parsedValue.yaml(-1)

def p_object(p):
	''' object : LLAVEIZQ LLAVEDER
				| LLAVEIZQ members LLAVEDER '''

	if p[2] == '}':
		# O -> { }
		p[0] = TokenWithAttributes((lambda x : "{}"), [])
	else:
		# O -> { M }
		parsedMemembers = p[2]
		p[0] = TokenWithAttributes((lambda x : "\n" + parsedMemembers.yaml(x) ), [])

def p_members(p):
	'''members : pair
				| pair COMA members '''

	parsedPair = p[1]
	if (len(p) > 2):
		# E -> V, E
		parsedMembers = p[3]
		p[0] = TokenWithAttributes((lambda x : parsedPair.yaml(x) + "\n"+ parsedMembers.yaml(x)), parsedPair.claves+parsedMembers.claves)
		if(parsedPair.claves[0] in parsedMembers.claves):
			raise Exception('EL JSON TIENE CLAVES REPETIDAS')
	else:
		# E -> V
		p[0] = TokenWithAttributes((lambda x : parsedPair.yaml(x)), parsedPair.claves)

def p_pair(p):
	'pair : STRING DOSPUNTOS value'
	# P -> string : M
	keyName = p[1]
	valor = p[3]

	if ("-" in keyName) or ("\\" in keyName):
		p[0] = TokenWithAttributes((lambda x : x*"  " + keyName + ": " + valor.yaml(x)), [keyName])
	else:
		p[0] = TokenWithAttributes((lambda x : x*"  " + keyName.strip("\"") + ": " + valor.yaml(x)), [keyName])


def p_array(p):
	'''array : CORCHEIZQ CORCHEDER
			| CORCHEIZQ elements CORCHEDER'''

	if len(p) == 3:
		# A -> [ ]
		p[0] = TokenWithAttributes((lambda x : "[]"), [])
	else:
		# A -> [ E ]
		parsedElements = p[2]
		p[0] = TokenWithAttributes((lambda x : "\n" + parsedElements.yaml(x)), [])

def p_elements(p):
	''' elements : value COMA elements
				| value '''

	parsedValue = p[1]
	# E -> V
	if(len(p) > 2):
		parsedElements = p[3]
		p[0] = TokenWithAttributes((lambda x : x*"  " + "- " + parsedValue.yaml(x) + "\n" + parsedElements.yaml(x)), [])
	else:
		p[0] = TokenWithAttributes((lambda x : x*"  " + "- " + parsedValue.yaml(x)), [])

def p_value_array(p):
	'value : array '
	parsedObject = p[1]
	p[0] = TokenWithAttributes((lambda x : parsedObject.yaml(x + 1)), [])

def p_value_object(p):
	'value : object '
	parsedObject = p[1]
	p[0] = TokenWithAttributes((lambda x : parsedObject.yaml(x + 1)), [])

def p_value_string(p):
	'value : STRING '
	valor = str(p[1])
	if ("-" in valor) or ("\\" in valor):
		p[0] = TokenWithAttributes((lambda x : valor), [])
	else:
		p[0] = TokenWithAttributes((lambda x : valor.strip('\"')), [])

def p_value_number(p):
	'value : NUMBER '
	valor = str(p[1])
	p[0] = TokenWithAttributes((lambda x : valor), [])

def p_value_true(p):
	'value : TRUE '
	p[0] = TokenWithAttributes((lambda x : "true"), [])

def p_value_false(p):
	'value : FALSE '
	p[0] = TokenWithAttributes((lambda x : "false"), [])

def p_value_null(p):
	'value : NULL '
	p[0] = TokenWithAttributes((lambda x : ""), [])

def p_error(p):
	raise Exception('LA SINTAXIS DEL JSON ES ERRONEA')

lexeer.input(jsonToParse)

parser = yacc.yacc(start = 'first')

result = parser.parse(lexer = lexeer)

