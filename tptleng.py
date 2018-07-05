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
	def __init__(self, tipo, listaTokensWithAttribute, yaml):
		self.tipo = tipo
		self.listaTokensWithAttribute = listaTokensWithAttribute
		self.yaml = yaml

start = 'first'

def p_first(p):
	'first : value'
	parsingTree = TokenWithAttribute("primero", p[1], "")
	p[0] = p[1].imprimir();

def p_object(p):
    ''' object : LLAVEIZQ LLAVEDER
                | LLAVEIZQ members LLAVEDER '''

    if p[2] == '}':
        # O -> { }
        p[0] = TokenWithAttributes("terminal",[],"{}")
    else:
        # O -> { M }
        p[0] = TokenWithAttributes("object",[p[1]],"")

def p_members(p):
    '''members : pair
                | pair COMA members '''

	if (len(p) > 2):
		# E -> V, E
	        p[0] = TokenWithAttributes("lista",[p[1],p[3]],"")
	else:
		# E -> V
	        p[0] = TokenWithAttributes("lista",[p[1]],"")

def p_pair(p):
    'pair : STRING DOSPUNTOS value'
    # P -> string : M
        p[0] = TokenWithAttributes("par",[p[1],p[3]],"")

def p_array(p):
    '''array : CORCHEIZQ CORCHEDER
            | CORCHEIZQ elements CORCHEDER'''

    if len(p) == 3:
        # A -> [ ]
        p[0] = TokenWithAttributes("terminal",[],"[]")
    else:
        # A -> [ E ]
        p[0] = TokenWithAttributes("array",[p[2]],"")

def p_elements(p):
    ''' elements : value COMA elements
                | value '''

    # E -> V
    if(len(p) > 2):
        p[0] = TokenWithAttributes("lista",[p[1],p[3]],"")
    else:
        p[0] = TokenWithAttributes("lista",[p[1]],"")

def p_value_array(p):
    'value : array '
        p[0] = TokenWithAttributes("array",[p[1]],"")

def p_value_object(p):
    'value : object '
        p[0] = TokenWithAttributes("object",[p[1]],"")

def p_value_string(p):
    'value : STRING '
        p[0] = TokenWithAttributes("terminal",[],"string")

def p_value_number(p):
    'value : NUMBER '
        p[0] = TokenWithAttributes("terminal",[],"number")

def p_value_true(p):
    'value : TRUE '
        p[0] = TokenWithAttributes("terminal",[],"true")

def p_value_false(p):
    'value : FALSE '
        p[0] = TokenWithAttributes("terminal",[],"false")

def p_value_null(p):
    'value : NULL '
        p[0] = TokenWithAttributes("terminal",[],"")


def p_error(p):
    print("ERROR NO RECONOCI NADA")

lexer.input(f.read())

#while True:
#    tok = lexer.token()
#    if not tok:
#        break
#    print(tok)

parser = yacc.yacc(start = 'first')

result = parser.parse(lexer = lexer)

