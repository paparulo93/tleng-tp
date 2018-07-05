import ply.lex as lex
import ply.yacc as yacc

f= open("jsonObjet.txt","r")

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

def t_NUMBER(t):
	r'-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?'
	return t

def t_STRING(t):
	r'\"[^\\"]*\"'
	return t

t_ignore = " \t"

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

def t_error(t):
	print("SOS UN BOLUDO, QUE CARAJO ENTENDISTE")

lexer = lex.lex()

class TokenWithAttributes:
	def __init__(self, tipo, yaml):
		self.tipo = tipo
		self.yaml = yaml

start = 'first'

def p_first(p):
	'first : value'
	parsedValue = p[1]
	print("---" + parsedValue.yaml(-1))
	p[0] = parsedValue.yaml(-1)

def p_object(p):
	''' object : LLAVEIZQ LLAVEDER
				| LLAVEIZQ members LLAVEDER '''

	if p[2] == '}':
		# O -> { }
		p[0] = TokenWithAttributes("terminal", (lambda x : "{}"))
	else:
		# O -> { M }
		parsedObject = p[2]
		p[0] = TokenWithAttributes("object", (lambda x : "\n" + parsedObject.yaml(x) ))

def p_members(p):
	'''members : pair
				| pair COMA members '''

	parsedPair = p[1]
	if (len(p) > 2):
		# E -> V, E
			parsedMembers = p[3]
			p[0] = TokenWithAttributes("lista", (lambda x : x*"\t" + parsedPair.yaml(x) + "\n"+ parsedMembers.yaml(x)))
	else:
		# E -> V
			p[0] = TokenWithAttributes("lista",(lambda x : x*"\t" + parsedPair.yaml(x)))

def p_pair(p):
	'pair : STRING DOSPUNTOS value'
	# P -> string : M
	keyName = p[1].strip("\"")
	valor = p[3]
	p[0] = TokenWithAttributes("par", (lambda x : x*"\t" + keyName + ": " + valor.yaml(x)))

def p_array(p):
	'''array : CORCHEIZQ CORCHEDER
			| CORCHEIZQ elements CORCHEDER'''

	if len(p) == 3:
		# A -> [ ]
		p[0] = TokenWithAttributes("terminal", (lambda x : "[]"))
	else:
		# A -> [ E ]
		parsedElements = p[2]
		p[0] = TokenWithAttributes("array", (lambda x : "\n" + x*"\t" + parsedElements.yaml(0)))

def p_elements(p):
	''' elements : value COMA elements
				| value '''

	parsedValue = p[1]
	# E -> V
	if(len(p) > 2):
		parsedElements = p[3]
		p[0] = TokenWithAttributes("lista", (lambda x : x*"\t" + "-" + parsedValue.yaml(0) + "\n" + parsedElements.yaml(x)))
	else:
		p[0] = TokenWithAttributes("lista", (lambda x : x*"\t" + "-" + parsedValue.yaml(0)))

def p_value_array(p):
	'value : array '
	parsedObject = p[1]
	p[0] = TokenWithAttributes("array", (lambda x : parsedObject.yaml(x + 1)))

def p_value_object(p):
	'value : object '
	parsedObject = p[1]
	p[0] = TokenWithAttributes("object", (lambda x : parsedObject.yaml(x + 1)))

def p_value_string(p):
	'value : STRING '
	valor = str(p[1]).strip('\"')
	p[0] = TokenWithAttributes("terminal", (lambda x : valor))

def p_value_number(p):
	'value : NUMBER '
	valor = str(p[1])
	p[0] = TokenWithAttributes("terminal", (lambda x : valor))

def p_value_true(p):
	'value : TRUE '
	p[0] = TokenWithAttributes("terminal", (lambda x : x*"\t" + "true"))

def p_value_false(p):
	'value : FALSE '
	p[0] = TokenWithAttributes("terminal", (lambda x : x*"\t" + "false"))

def p_value_null(p):
	'value : NULL '
	p[0] = TokenWithAttributes("terminal", (lambda x : x*"\t"))


def p_error(p):
	raise Exception('NO RECONOCI NADA', p)

lexer.input(f.read())

#while True:
#    tok = lexer.token()
#    if not tok:
#        break
#    print(tok)

parser = yacc.yacc(start = 'first')

result = parser.parse(lexer = lexer)

