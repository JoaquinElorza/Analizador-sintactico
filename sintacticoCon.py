import re
from tkinter import Tk, scrolledtext, Button, Frame, Label, messagebox, Text, BOTH, RIGHT, Y, LEFT

class AnalizadorSintactico:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Sintáctico para Robot")
        self.setup_ui()
        
        self.tokens = [
    ('p_reservada', r'Robot'),
    ('metodo', r'(velocidad|base|cuerpo|garra)'),
    ('identificador', r'[a-zA-Z_]\w*'),
    ('accion', r'iniciar'),
    ('conector', r'\.'),
    ('valor', r'\d+'),
    ('parentesis_abre', r'\('),
    ('parentesis_cierra', r'\)'),
    ('espacio', r'\s+')
]

        self.tokens_compilados = [(nombre, re.compile(patron)) for nombre, patron in self.tokens]

    def setup_ui(self):
        main_frame = Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill="both", expand=True)

        Label(main_frame, text="Ingrese las instrucciones:").pack(anchor="w")

        # Frame para numeración + entrada
        entry_frame = Frame(main_frame)
        entry_frame.pack(fill=BOTH, expand=True, pady=(0,10))

        # Widget para numeración de líneas
        self.line_numbers = Text(entry_frame, width=4, padx=4, takefocus=0, border=0,
                                 background='lightgray', state='disabled', wrap='none')
        self.line_numbers.pack(side=LEFT, fill=Y)

        # Área de entrada con scroll
        self.entrada = scrolledtext.ScrolledText(entry_frame, height=10, wrap="word")
        self.entrada.pack(side=RIGHT, fill=BOTH, expand=True)

        # Vincular eventos para sincronizar numeración
        self.entrada.bind('<KeyRelease>', self.update_line_numbers)
        self.entrada.bind('<MouseWheel>', self.update_line_numbers)  # Para scroll en Windows
        self.entrada.bind('<Button-4>', self.update_line_numbers)    # Para scroll en Linux
        self.entrada.bind('<Button-5>', self.update_line_numbers)    # Para scroll en Linux

        self.update_line_numbers()  # Inicializa numeración

        Button(main_frame, text="Analizar", command=self.analizar_instrucciones,
              bg="#4CAF50", fg="white").pack(pady=(0, 10))

        Label(main_frame, text="Resultados del análisis:").pack(anchor="w")
        self.resultados = scrolledtext.ScrolledText(main_frame, height=15, wrap="word")
        self.resultados.pack(fill="both", expand=True)

        self.resultados.tag_config('error', foreground='red')
        self.resultados.tag_config('exito', foreground='green')
        self.resultados.tag_config('token', foreground='blue')
        self.resultados.tag_config('header', foreground='#333', font=('Arial', 10, 'bold'))

    def update_line_numbers(self, event=None):
        # Actualiza la numeración según número de líneas en el área de entrada
        line_count = int(self.entrada.index('end-1c').split('.')[0])
        line_numbers_string = "\n".join(str(i) for i in range(1, line_count))
        self.line_numbers.config(state='normal')
        self.line_numbers.delete('1.0', 'end')
        self.line_numbers.insert('1.0', line_numbers_string)
        self.line_numbers.config(state='disabled')

        # Sincronizar scroll vertical con entrada
        self.line_numbers.yview_moveto(self.entrada.yview()[0])

    def analizar_lexico(self, instruccion):
        position = 0
        tokens_encontrados = []
        
        while position < len(instruccion):
            match_found = False
            for nombre_token, regex in self.tokens_compilados:
                match = regex.match(instruccion, position)
                if match:
                    lexema = match.group(0)
                    if nombre_token != 'espacio':
                        tokens_encontrados.append((nombre_token, lexema))
                    position += len(lexema)
                    match_found = True
                    break
            
            if not match_found:
                raise ValueError(f"Token no reconocido: '{instruccion[position]}' en posición {position}")
        
        return tokens_encontrados

    def verificar_sintaxis(self, tokens):
        if not tokens:
            return False, "Instrucción vacía"
            
        if len(tokens) == 2 and tokens[0][0] == 'p_reservada' and tokens[1][0] == 'identificador':
            return True, "Declaración válida de robot"
            
        patron_metodo = ['identificador', 'conector', 'metodo', 'parentesis_abre', 'valor', 'parentesis_cierra']
        tipos = [tipo for tipo, valor in tokens]
        
        if tipos == patron_metodo:
            metodo = tokens[2][1]
            valor = int(tokens[4][1])
            
            rangos = {
                'velocidad': (0, 10),
                'base': (0, 180),
                'cuerpo': (0, 100),
                'garra': (0, 100)
            }
            
            min_val, max_val = rangos.get(metodo, (0, 100))
            if not (min_val <= valor <= max_val):
                return False, f"Valor {valor} fuera de rango para {metodo} ({min_val}-{max_val})"
                
            return True, f"Instrucción de {metodo} válida"
        
        return False, "Estructura no reconocida. Formatos válidos:\n- Robot 'identificador'\n- r1.metodo(valor)"

    def analizar_instrucciones(self):
        self.resultados.delete(1.0, "end")
        texto = self.entrada.get(1.0, "end-1c")
        
        if not texto.strip():
            messagebox.showwarning("Advertencia", "Por favor ingrese instrucciones para analizar")
            return
        
        instrucciones = [line.rstrip() for line in texto.split('\n')]
        errores_encontrados = False
        
        for idx, instruccion in enumerate(instrucciones, 1):
            if not instruccion.strip():
                continue
            
            try:
                tokens = self.analizar_lexico(instruccion)
                print(f"Línea {idx} tokens: {tokens}")
                valido, mensaje = self.verificar_sintaxis(tokens)
                if not valido:
                    errores_encontrados = True
                    self.resultados.insert("end", f"Error en línea {idx}: {mensaje}\n", 'error')
            except ValueError as e:
                errores_encontrados = True
                self.resultados.insert("end", f"Error en línea {idx}: {e}\n", 'error')
        
        if not errores_encontrados:
            self.resultados.insert("end", "No se encontraron errores.\n", 'exito')


if __name__ == "__main__":
    root = Tk()
    root.geometry("700x600")
    app = AnalizadorSintactico(root)
    root.mainloop()
