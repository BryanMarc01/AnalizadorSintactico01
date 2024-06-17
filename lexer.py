import ply.lex as lex

# Lista de tokens
tokens = (
    'IDENTIFICADOR', 'ENTERO', 'SUMA', 'RESTA', 'MULT', 'DIV', 'POTENCIA', 'MODULO',
    'ASIGNAR', 'PUNTOCOMA', 'PARIZQ', 'PARDER', 'LLAIZQ', 'LLADER', 'CORIZQ', 'CORDER',
    'MENORQUE', 'MAYORQUE', 'MENORIGUAL', 'MAYORIGUAL', 'IGUAL', 'DISTINTO',
    'AND', 'OR', 'NOT', 'COMDOB'
)

# Expresiones regulares para tokens simples
t_SUMA = r'\+'
t_RESTA = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_POTENCIA = r'\*\*'
t_MODULO = r'%'
t_ASIGNAR = r'='
t_PUNTOCOMA = r';'
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_LLAIZQ = r'\{'
t_LLADER = r'\}'
t_CORIZQ = r'\['
t_CORDER = r'\]'
t_MENORQUE = r'<'
t_MAYORQUE = r'>'
t_MENORIGUAL = r'<='
t_MAYORIGUAL = r'>='
t_IGUAL = r'=='
t_DISTINTO = r'!='
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_COMDOB = r'\"'

def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# Construir el analizador léxico
analizador = lex.lex()
