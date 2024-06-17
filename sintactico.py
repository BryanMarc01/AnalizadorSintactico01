import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import ttk
import ply.yacc as yacc
from lexer import tokens, analizador

# resultado del analisis
resultado_gramatica = []

precedence = (
    ('right', 'ASIGNAR'),
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULT', 'DIV'),
    ('right', 'UMINUS'),
)

nombres = {}

def p_declaracion_asignar(t):
    'declaracion : IDENTIFICADOR ASIGNAR expresion PUNTOCOMA'
    nombres[t[1]] = t[3]

def p_declaracion_expr(t):
    'declaracion : expresion'
    t[0] = t[1]

def p_expresion_operaciones(t):
    '''
    expresion  :   expresion SUMA expresion
                |   expresion RESTA expresion
                |   expresion MULT expresion
                |   expresion DIV expresion
                |   expresion POTENCIA expresion
                |   expresion MODULO expresion
    '''
    if t[2] == '+':
        t[0] = t[1] + t[3]
    elif t[2] == '-':
        t[0] = t[1] - t[3]
    elif t[2] == '*':
        t[0] = t[1] * t[3]
    elif t[2] == '/':
        t[0] = t[1] / t[3]
    elif t[2] == '%':
        t[0] = t[1] % t[3]
    elif t[2] == '**':
        i = t[3]
        t[0] = t[1]
        while i > 1:
            t[0] *= t[1]
            i -= 1

def p_expresion_uminus(t):
    'expresion : RESTA expresion %prec UMINUS'
    t[0] = -t[2]

def p_expresion_grupo(t):
    '''
    expresion  : PARIZQ expresion PARDER
                | LLAIZQ expresion LLADER
                | CORIZQ expresion CORDER
    '''
    t[0] = t[2]

def p_expresion_logicas(t):
    '''
    expresion   :  expresion MENORQUE expresion 
                |  expresion MAYORQUE expresion 
                |  expresion MENORIGUAL expresion 
                |   expresion MAYORIGUAL expresion 
                |   expresion IGUAL expresion 
                |   expresion DISTINTO expresion
                |  PARIZQ expresion PARDER MENORQUE PARIZQ expresion PARDER
                |  PARIZQ expresion PARDER MAYORQUE PARIZQ expresion PARDER
                |  PARIZQ expresion PARDER MENORIGUAL PARIZQ expresion PARDER 
                |  PARIZQ  expresion PARDER MAYORIGUAL PARIZQ expresion PARDER
                |  PARIZQ  expresion PARDER IGUAL PARIZQ expresion PARDER
                |  PARIZQ  expresion PARDER DISTINTO PARIZQ expresion PARDER
    '''
    if t[2] == "<": t[0] = t[1] < t[3]
    elif t[2] == ">": t[0] = t[1] > t[3]
    elif t[2] == "<=": t[0] = t[1] <= t[3]
    elif t[2] == ">=": t[0] = t[1] >= t[3]
    elif t[2] == "==": t[0] = t[1] is t[3]
    elif t[2] == "!=": t[0] = t[1] != t[3]
    elif t[3] == "<":
        t[0] = t[2] < t[4]
    elif t[2] == ">":
        t[0] = t[2] > t[4]
    elif t[3] == "<=":
        t[0] = t[2] <= t[4]
    elif t[3] == ">=":
        t[0] = t[2] >= t[4]
    elif t[3] == "==":
        t[0] = t[2] is t[4]
    elif t[3] == "!=":
        t[0] = t[2] != t[4]

def p_expresion_booleana(t):
    '''
    expresion   :   expresion AND expresion 
                |   expresion OR expresion 
                |   expresion NOT expresion 
                |  PARIZQ expresion AND expresion PARDER
                |  PARIZQ expresion OR expresion PARDER
                |  PARIZQ expresion NOT expresion PARDER
    '''
    if t[2] == "&&":
        t[0] = t[1] and t[3]
    elif t[2] == "||":
        t[0] = t[1] or t[3]
    elif t[2] == "!":
        t[0] =  t[1] is not t[3]
    elif t[3] == "&&":
        t[0] = t[2] and t[4]
    elif t[3] == "||":
        t[0] = t[2] or t[4]
    elif t[3] == "!":
        t[0] =  t[2] is not t[4]

def p_expresion_numero(t):
    'expresion : ENTERO'
    t[0] = t[1]

def p_expresion_cadena(t):
    'expresion : COMDOB expresion COMDOB'
    t[0] = t[2]

def p_expresion_nombre(t):
    'expresion : IDENTIFICADOR'
    try:
        t[0] = nombres[t[1]]
    except LookupError:
        print("Nombre desconocido ", t[1])
        t[0] = 0

def p_error(t):
    global resultado_gramatica
    if t:
        resultado = "Error sintactico de tipo {} en el valor {}".format( str(t.type),str(t.value))
        print(resultado)
    else:
        resultado = "Error sintactico {}".format(t)
        print(resultado)
    resultado_gramatica.append(resultado)

# instanciamos el analizador sistactico
parser = yacc.yacc(debug=False)

def prueba_sintactica(data):
    global resultado_gramatica
    resultado_gramatica.clear()

    for item in data.splitlines():
        if item:
            gram = parser.parse(item, lexer=analizador)
            if gram is not None:
                resultado_gramatica.append(str(gram))
        else:
            print("False")

    print("result: ", resultado_gramatica)
    return resultado_gramatica

class ParserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Sintáctico")
      
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure('TFrame', background='#2c3e50')
        self.style.configure('TLabel', background='#2c3e50', foreground='#ecf0f1', font=('Helvetica', 14))
        self.style.configure('TButton', background='#2980b9', foreground='#ecf0f1', font=('Helvetica', 12))
        self.style.configure('TEntry', fieldbackground='#ecf0f1', font=('Helvetica', 14))
        
        self.frame = ttk.Frame(root, padding="20")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.label = ttk.Label(self.frame, text="Ingrese una expresión aritmética:")
        self.label.grid(row=0, column=0, columnspan=2, pady=10, sticky=tk.W)
        
        self.entry = ttk.Entry(self.frame, width=60)
        self.entry.grid(row=1, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        self.button = ttk.Button(self.frame, text="Analizar", command=self.analyze)
        self.button.grid(row=2, column=0, columnspan=2, pady=20)
        
        self.result_frame = ttk.Frame(self.frame)
        self.result_frame.grid(row=3, column=0, columnspan=2, pady=20, sticky=(tk.W, tk.E))
        
        self.ast_label = ttk.Label(self.result_frame, text="Analizador Sintactico")
        self.ast_label.grid(row=0, column=0, pady=5, sticky=tk.W)
        
        self.ast_text = scrolledtext.ScrolledText(self.result_frame, width=80, height=15, wrap=tk.WORD, font=('Helvetica', 12), background='#ecf0f1')
        self.ast_text.grid(row=1, column=0, pady=5, sticky=(tk.W, tk.E))
        
        self.result_label = ttk.Label(self.frame, text="")
        self.result_label.grid(row=4, column=0, columnspan=2, pady=20)
        
        for child in self.frame.winfo_children():
            child.grid_configure(padx=10, pady=5)
    
    def analyze(self):
        expression = self.entry.get()
        try:
            results = prueba_sintactica(expression)
            self.ast_text.delete(1.0, tk.END)
            self.ast_text.insert(tk.END, '\n'.join(results))
            self.result_label.config(text=f"Resultado: {results}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ParserApp(root)
    root.mainloop()
