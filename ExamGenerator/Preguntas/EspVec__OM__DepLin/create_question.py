import sys
import fractions
import numpy as np
import random
import os

# --- Ruta robusta (sin cambios) ---
try:
    list_dir = os.path.abspath(os.path.dirname(__file__)).split(os.sep)[:-2]
    LibraryFolder = os.sep.join(list_dir)
except Exception:
    LibraryFolder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(LibraryFolder)
import LibCreateQuestion

def generar_pregunta(output_format='html'):
    DestFolder = os.path.dirname(__file__)
    json_dict = dict()
    substitutions = dict()
    json_dict["Type"] = "OM"
    TemplateFile = 'ExamTemplate/TemplateSimple.tex'

    # --- Definición del enunciado en LaTeX (sin cambios) ---
    Question = r"""
    Considere los siguientes tres vectores de $\mathbb{R}^3$.

    $$
    v_1=\begin{bmatrix} [a] \\ [b] \\ 0 \end{bmatrix} \ \ \ 
    v_2=\begin{bmatrix} 0 \\ [b] \\ [a] \end{bmatrix} \ \ \ 
    v_3=\begin{bmatrix} [d] \\ [e] \\ [f] \end{bmatrix} \ \ \ 
    $$

    Haga un planteamiento claro para determinar cuál de las siguientes incisos es correcto.
    """

    dict_choices = {"Correct": [], "Incorrect": []}

    # --- Generación de parámetros y cálculos (sin cambios) ---
    parameters = dict()
    a = random.choice([random.randint(-3, -1), random.randint(1, 3)])
    b = random.choice([random.randint(-3, -1), random.randint(1, 3)])
    c = random.choice([random.randint(-3, -1), random.randint(1, 3)])
    x = random.choice([random.randint(-3, -1), random.randint(1, 3)])
    y = random.choice([random.randint(-3, -1), random.randint(1, 3)])
    json_dict["Parameters"] = {"a": a, "b": b, "c": c, "x": x, "y": y}
    
    d, e, f = a, b + c * b, c * a
    g, h, i = x * a, x * b + y * b, y * a

    # --- Sustituciones para la plantilla (sin cambios) ---
    substitutions = {
        "a": (a, "{value}"), "b": (b, "{value}"), "c": (c, "{value}"),
        "d": (d, "{value}"), "e": (e, "{value}"), "f": (f, "{value}"),
        "g": (g, "{value}"), "h": (h, "{value}"), "i": (i, "{value}"),
        "x": (x, "{value}"), "y": (y, "{value}")
    }

    # ▼▼▼ INICIO DE LA MODIFICACIÓN IMPORTANTE ▼▼▼
    # --- Definición de las opciones correctas e incorrectas ---

    # Reescribimos la opción correcta para que sea mucho más clara
    correct_choice_string = r"""
    Los tres vectores son linealmente dependientes, pues una solución no trivial a la ecuación $\alpha_1v_1+\alpha_2v_2+\alpha_3v_3=0$ es, por ejemplo, con $\alpha_1=1$, $\alpha_2=[c]$, y $\alpha_3=-1$.
    """
    
    dict_choices["Correct"].append(correct_choice_string)

    dict_choices["Incorrect"].append(
        r"Los tres vectores son linealmente dependientes y son una base para $\mathbb{R}^3$."
    )
    dict_choices["Incorrect"].append(
        r"Los tres vectores son linealmente independientes y son una base para $\mathbb{R}^3$."
    )
    dict_choices["Incorrect"].append(
        r"Los tres vectores son linealmente independientes y la única solución a $\alpha_1v_1+\alpha_2v_2+\alpha_3v_3=0$ es la trivial ($\alpha_1=0$, $\alpha_2=0$, $\alpha_3=0$)."
    )
    dict_choices["Incorrect"].append(
        r"Los tres vectores son linealmente independientes y el vector $v=\begin{bmatrix} [g] \\ [h] \\ [i] \end{bmatrix}$ se expresa como $v=[x]v_1+[y]v_2+0v_3$."
    )
    # ▲▲▲ FIN DE LA MODIFICACIÓN ▲▲▲

    # --- Creación del objeto pregunta y generación de archivos (sin cambios) ---
    question = LibCreateQuestion.create_question(
        DestFolder, TemplateFile, LibraryFolder,
        LatexQuestion=Question, dict_choices=dict_choices, output_format=output_format
    )
    
    json_dict["CR"] = question.CR
    question.substitutions(substitutions)
    question.write_output_file()
    question.write_json_file(json_dict)

    return os.path.join(DestFolder, 'Response.tex')

# --- Bloque para ejecución directa (sin cambios) ---
if __name__ == "__main__":
    print("Generando pregunta en formato LaTeX para PDF...")
    ruta_archivo = generar_pregunta(output_format='latex') 
    print(f"Archivo 'Response.tex' con código LaTeX creado en: {ruta_archivo}")