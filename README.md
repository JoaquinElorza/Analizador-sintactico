
# Analizador Sintáctico para garra robotica

Este proyecto es una aplicación de escritorio construida en Python usando `Tkinter`, que actúa como un **analizador léxico y sintáctico** para instrucciones relacionadas con un robot. Permite validar si las instrucciones escritas por el usuario cumplen con la sintaxis esperada.

## 🧠 ¿Qué hace?

La aplicación permite analizar instrucciones como:

```text
Robot r1
r1.velocidad(5)
r1.base(90)
````

Detecta errores sintácticos y muestra mensajes detallados por línea. También valida que los valores de cada método estén dentro de un rango aceptado.

## 🛠 Características

* Análisis **léxico** (tokenización)
* Análisis **sintáctico** (estructura de instrucciones)
* Interfaz gráfica con:

  * Entrada multilinea con numeración de líneas
  * Visualización clara de resultados
  * Scroll integrado
* Validación de rangos para cada método del robot:

  * `velocidad`: 0 - 10
  * `base`: 0 - 180
  * `cuerpo`: 0 - 100
  * `garra`: 0 - 100

## 📦 Requisitos

* Python 3.7 o superior
* No requiere librerías externas adicionales

## ▶️ Cómo ejecutar

1. Asegúrate de tener Python instalado.
2. Clona este repositorio o descarga el archivo.
3. Ejecuta el script:

```bash
python analizador_sintactico.py
```

## 💡 Sintaxis válida

### Declaración del robot:

```text
Robot r1
```

### Instrucciones válidas:

```text
r1.velocidad(5)
r1.base(90)
r1.cuerpo(50)
r1.garra(1)
```

## ⚠️ Errores comunes detectados

* Token no reconocido
* Identificadores mal escritos
* Uso incorrecto de paréntesis
* Valores fuera del rango permitido
