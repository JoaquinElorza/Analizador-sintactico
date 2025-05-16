import re
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Definición de tokens
TOKENS = [
    ('p_reservada', r'Robot'),
    ('identificador', r'r\d+'),
    ('accion', r'iniciar'),
    ('conector', r'\.'),
    ('metodo', r'(velocidad|base|cuerpo|garra)'),
    ('valor', r'\d+'),
    ('parentesis_abierto', r'\('),
    ('parentesis_cerrado', r'\)'),
   # ('fin_instruccion', r'@'),
    ('coma', r',')
]

class AnalizadorLexicoApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Analizador Léxico de Instrucciones")
        self.root.geometry("600x500") #Tamaño de la interfaz
        
        self.create_widgets()
    
    def create_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Etiqueta y area de entrada de las instrucciones 
        tk.Label(main_frame, text="Ingrese las instrucciones:").pack(anchor=tk.W)
        self.entrada_text = scrolledtext.ScrolledText(main_frame, height=10, wrap=tk.WORD)
        self.entrada_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Boton para analizar la instruccion ingresada
        tk.Button(main_frame, text="Analizar", command=self.leer_entradas, 
                bg="#4CAF50", fg="white").pack(pady=(0, 10))
        
        # area de resultados
        tk.Label(main_frame, text="Resultados del análisis:").pack(anchor=tk.W)
        self.resultados_text = scrolledtext.ScrolledText(main_frame, height=15, wrap=tk.WORD)
        self.resultados_text.pack(fill=tk.BOTH, expand=True)
        
        # estilo de texto para resultados
        self.resultados_text.tag_config('error', foreground='red')
        self.resultados_text.tag_config('header', foreground='blue', font=('Arial', 10, 'bold'))
    
    def analizar_instruccion(self, instruccion):
        position = 0
        tokens_encontrados = []
        
        while position < len(instruccion):
            match_found = False
            for nombre_token, patron in TOKENS:
                regex = re.compile(patron)
                match = regex.match(instruccion, position)
                if match:
                    lexema = match.group(0)
                    tokens_encontrados.append((nombre_token, lexema))
                    position += len(lexema)
                    match_found = True
                    break
            
            if not match_found:
                if instruccion[position] in [' ', '\t', '\n']:
                    position += 1
                    continue
                raise ValueError(f"Token no reconocido en posición {position}: '{instruccion[position]}'")
        
        return tokens_encontrados
    
    def leer_entradas(self):
        # Limpiar resultados anteriores
        self.resultados_text.delete(1.0, tk.END)
        
        # Obtener instrucciones del área de texto
        texto = self.entrada_text.get(1.0, tk.END).strip()
        if not texto:
            messagebox.showwarning("Advertencia", "Por favor ingrese al menos una instrucción.")
            return
        
        instrucciones = [line.strip() for line in texto.split('\n') if line.strip()] 
        
        for idx, instruccion in enumerate(instrucciones, 1):
            self.resultados_text.insert(tk.END, f"\nInstrucción {idx}: {instruccion}\n", 'header')
            
            try:
                resultado = self.analizar_instruccion(instruccion)
                if not resultado:
                    self.resultados_text.insert(tk.END, "  (Instrucción vacía)\n")
                    continue
                    
                for tipo, valor in resultado:
                    self.resultados_text.insert(tk.END, f"  {tipo:20}: {valor}\n")
            except ValueError as e:
                self.resultados_text.insert(tk.END, f"  Error: {e}\n", 'error')
        
        self.resultados_text.insert(tk.END, "\nAnálisis completado.\n", 'header')

if __name__ == "_main_":
    root = tk.Tk()
    app = AnalizadorLexicoApp(root)
    root.mainloop()