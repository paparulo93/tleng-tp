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
    try:
        t.value = float(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    #t.tipo = "num"
    return t

def t_STRING(t):
    r'\"[^\\"]*\"'
    t.tipo = "string"
    t.value=t.value
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("SOS UN BOLUDO, QUE CARAJO ENTENDISTE")

lexer = lex.lex()

start = 'first'

def p_first(p):
    'first : value'
    p[0].tipo="primero"
    p[1].tabs = 0
    p[0].yaml = "" + p[1].yaml
    print(p[0].yaml)

def p_object(p):
    ''' object : LLAVEIZQ LLAVEDER
                | LLAVEIZQ members LLAVEDER '''

    p[0].tipo = "object"
    if p[2] == '}':
        # O -> { }
        p[0].yaml="{}"
    else:
        # O -> { M }
        p[2].tabs = p[0].tabs+1
        p[0].yaml += "\n" + p[2].yaml

def p_members(p):
    '''members : pair
                | pair COMA members '''

    p[0].tipo="lista"
    p[1].tabs = p[0].tabs
    p[0].yaml += "\n"+p[1].yaml + "\n"
    # E -> V

    if len(p) > 2:
        # E -> V, E
        p[3].tabs = p[0].tabs
        p[0].yaml += p[3].yaml

def p_pair(p):
    'pair : STRING DOSPUNTOS value'
    # P -> string : M
    p[0].tipo = "par"
    p[3].tabs = p[0].tabs+1
    p[0].yaml = p[0].tabs*"\t" + p[1].value+": "+p[3].yaml

def p_array(p):
    '''array : CORCHEIZQ CORCHEDER
            | CORCHEIZQ elements CORCHEDER'''

    p[0].tipo = "array"
    if len(p) == 3:
        # A -> [ ]
        p[0].yaml = "[]"
    else:
        # A -> [ E ]
        p[2].tabs = p[0].tabs+1
        p[0].yaml += "\n" + p[2].yaml


def p_elements(p):
    ''' elements : value COMA elements
                | value '''

    p[0].tipo="lista"
    # E -> V
    if(p[1].tipo in Set(["array", "object"])):
        p[1].tabs = p[0].tabs+1
        p[0].yaml += p[0].tabs*"\t"+"-"+"\n"+ p[1].yaml + "\n"
    else:
        p[0].yaml += p[0].tabs*"\t"+"-"+ p[1].yaml + "\n"

    if len(p) > 2:
        # E -> V, E
        p[3].tabs = p[0].tabs
        p[0].yaml += p[3].yaml



def p_value_array(p):
    'value : array '
    p[0].tipo = "array"
    p[0].yaml = p[1].yaml

def p_value_object(p):
    'value : object '
    p[0].tipo = "object"
    p[0].yaml = p[1].yaml

def p_value_string(p):
    'value : STRING '
    p[0].tipo = "valor"
    p[0].yaml = p[1].value

def p_value_number(p):
    'value : NUMBER '
    p[0].tipo = "valor"
    p[0].yaml = p[1].value

def p_value_true(p):
    'value : TRUE '
    p[0].tipo = "valor"
    p[0].yaml = "true"

def p_value_false(p):
    'value : FALSE '
    p[0].tipo = "valor"
    p[0].yaml = "false"

def p_value_null(p):
    'value : NULL '
    p[0].tipo = "valor"
    p[0].yaml = ""



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
