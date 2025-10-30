# -*- coding: utf-8 -*-
#
# ARCHIVO: C:\...\app\ExamGenerator\Preguntas\EspVec__OM__DepLin\create_question.py
# VERSIÓN REGENERADA: Ahora devuelve un 'dict' en lugar de escribir archivos.
#

import sys
import fractions
import numpy as np
import random
import os

# --- 1. FUNCIÓN PRINCIPAL ---
# (Ya no necesitamos importar LibCreateQuestion_class)
#
def generar_pregunta():
    """
    Genera una única pregunta de dependencia lineal
    y DEVUELVE un diccionario (dict) con los datos.
    """
    
    # --- 2. LÓGICA MATEMÁTICA (Generación de Parámetros) ---
    # (Esta lógica es idéntica a tu versión original)
    a = random.choice([random.randint(-3, -1), random.randint(1, 3)])
    b = random.choice([random.randint(-3, -1), random.randint(1, 3)])
    c = random.choice([random.randint(-3, -1), random.randint(1, 3)])
    x = random.choice([random.randint(-3, -1), random.randint(1, 3)])
    y = random.choice([random.randint(-3, -1), random.randint(1, 3)])
    
    d, e, f = a, b + c * b, c * a
    g, h, i = x * a, x * b + y * b, y * a

    # --- 3. DEFINICIÓN DEL ENUNCIADO (PLANTILLA) ---
    Question = r"""
    Considere los siguientes tres vectores de $\mathbb{R}^3$.
    $$
    v_1=\begin{bmatrix} [a] \\ [b] \\ 0 \end{bmatrix} \ \ \ 
    v_2=\begin{bmatrix} 0 \\ [b] \\ [a] \end{bmatrix} \ \ \ 
    v_3=\begin{bmatrix} [d] \\ [e] \\ [f] \end{bmatrix} \ \ \ 
    $$
    Haga un planteamiento claro para determinar cuál de las siguientes incisos es correcto.
    """

    # --- 4. DEFINICIÓN DE OPCIONES (PLANTILLAS) ---
    dict_choices = {"Correct": [], "Incorrect": []}
    
    correct_choice_string = r"""Los tres vectores son linealmente dependientes, pues una solución no trivial a la ecuación $\alpha_1v_1+\alpha_2v_2+\alpha_3v_3=0$ es, por ejemplo, con $\alpha_1=1$, $\alpha_2=[c]$, y $\alpha_3=-1$."""
    dict_choices["Correct"].append(correct_choice_string)
    
    dict_choices["Incorrect"].append( r"Los tres vectores son linealmente dependientes y son una base para $\mathbb{R}^3$.")
    dict_choices["Incorrect"].append(r"Los tres vectores son linealmente independientes y son una base para $\mathbb{R}^3." )
    dict_choices["Incorrect"].append(r"Los tres vectores son linealmente independientes y la única solución a $\alpha_1v_1+\alpha_2v_2+\alpha_3v_3=0$ es la trivial ($\alpha_1=0$, $\alpha_2=0$, $\alpha_3=0$).")
    dict_choices["Incorrect"].append(r"Los tres vectores son linealmente independientes y el vector $v=\begin{bmatrix} [g] \\ [h] \\ [i] \end{bmatrix}$ se expresa como $v=[x]v_1+[y]v_2+0v_3$.")

    # --- 5. SUSTITUCIÓN DE VALORES ---
    
    # Diccionario de sustitución (string a string)
    substitutions = {
        "[a]": str(a), "[b]": str(b), "[c]": str(c),
        "[d]": str(d), "[e]": str(e), "[f]": str(f),
        "[g]": str(g), "[h]": str(h), "[i]": str(i),
        "[x]": str(x), "[y]": str(y)
    }

    # Rellenar el enunciado
    enunciado_final = Question
    for key, val in substitutions.items():
        enunciado_final = enunciado_final.replace(key, val)
        
    # Rellenar las opciones, mezclarlas y encontrar el índice correcto
    lista_opciones_finales = []
    respuesta_correcta_idx = -1 # Placeholder

    # Crear lista [(texto_opcion, es_correcta_bool)]
    opciones_mezcladas = []
    for choice_text in dict_choices["Correct"]:
        opciones_mezcladas.append((choice_text, True))
    for choice_text in dict_choices["Incorrect"]:
        opciones_mezcladas.append((choice_text, False))
    
    random.shuffle(opciones_mezcladas) # Mezclarlas
    
    # Procesar la lista mezclada
    for i, (text, is_correct) in enumerate(opciones_mezcladas):
        # Rellenar los placeholders (ej. [c]) en el texto de la opción
        final_text = text
        for key, val in substitutions.items():
            final_text = final_text.replace(key, val)
        
        lista_opciones_finales.append(final_text)
        
        if is_correct:
            respuesta_correcta_idx = i # Guardar el índice (0, 1, 2, 3...) de la correcta
            
    # --- 6. VALOR DE RETORNO ---
    #
    # En lugar de escribir archivos, devolvemos el diccionario
    # que 'app/main.py' espera.
    #
    return {
        "enunciado_latex": enunciado_final,
        "opciones": lista_opciones_finales,
        "respuesta_correcta": respuesta_correcta_idx
    }

# --- BLOQUE DE PRUEBA (SOLO PARA EJECUCIÓN DIRECTA) ---
if __name__ == "__main__":
    print("Ejecutando prueba del script 'create_question.py'...")
    pregunta_generada = generar_pregunta()
    print("\n--- PREGUNTA GENERADA (DICT) ---")
    import json
    print(json.dumps(pregunta_generada, indent=2, ensure_ascii=False))