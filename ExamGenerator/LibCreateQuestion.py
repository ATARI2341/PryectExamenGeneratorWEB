import json
import os
import random
import fractions
import shutil

# --- Plantillas para ambos formatos ---
LatexQuestionTemplate = r"""
\question[Pa]

[question]

\begin{choices}
    [choices]
\end{choices}
"""

HTMLQuestionTemplate = """
<p>
[question]
</p>
<ol type="A" style="list-style-type: upper-alpha;">
    [choices]
</ol>
"""

dict_incisos = {1: "A.", 2: "B.", 3: "C.", 4: "D.", 5: "E.", 6: "F."}

class create_question:

    def __init__(self, DestFolder, TemplateFile, LibraryFolder, LatexQuestion, dict_choices, output_format='html'):
        self.DestFolder = DestFolder
        self.TemplateFile = TemplateFile
        self.LibraryFolder = LibraryFolder
        self.LatexQuestion = LatexQuestion # El enunciado siempre es LaTeX
        self.dict_choices = dict_choices
        self.output_format = output_format
        self.CR = ""

        # Elegimos la plantilla correcta según el formato solicitado
        if self.output_format == 'html':
            self.OutputString = HTMLQuestionTemplate
        else: # 'latex'
            self.OutputString = LatexQuestionTemplate

        self.shuffle_choices()

    def shuffle_choices(self):
        if not self.dict_choices.get("Correct"):
            raise ValueError("Se requiere al menos una opción correcta.")

        list_choices_data = []
        for choice in self.dict_choices["Correct"]:
            list_choices_data.append(("C", choice))
        for choice in self.dict_choices["Incorrect"]:
            list_choices_data.append(("I", choice))

        random.shuffle(list_choices_data)
        list_choices_data.append(("I", "No sé."))

        # ▼▼▼ LÓGICA DUAL PARA GENERAR LAS OPCIONES ▼▼▼
        final_choices = []
        if self.output_format == 'html':
            for kind, text in list_choices_data:
                if kind == "C":
                    final_choices.append(f"<li><b>{text}</b></li>")
                else:
                    final_choices.append(f"<li>{text}</li>")
        else: # 'latex'
            for kind, text in list_choices_data:
                if kind == "C":
                    final_choices.append(r"\CorrectChoice " + f"{text}")
                else:
                    final_choices.append(r"\choice " + f"{text}")

        CR = [dict_incisos[i + 1] for i, item in enumerate(list_choices_data) if item[0] == "C"]
        self.CR = f"[{','.join(CR)}]"
        self.OutputString = self.OutputString.replace("[choices]", "\n".join(final_choices))

    def substitutions(self, substitutions: dict = dict()) -> None:
        for key, (value, fmt) in substitutions.items():
            # Reemplazamos en ambas cadenas para asegurar consistencia
            self.OutputString = self.OutputString.replace(f"[{key}]", str(value))
            self.LatexQuestion = self.LatexQuestion.replace(f"[{key}]", str(value))

    def write_output_file(self):
        # El nombre del archivo sigue siendo el mismo, pero su contenido cambia
        final_output = self.OutputString.replace("[question]", self.LatexQuestion)
        
        filepath = os.path.join(self.DestFolder, "Response.tex")
        with open(filepath, "w", encoding="utf-8") as outfile:
            outfile.write(final_output)
        return final_output

    def write_json_file(self, json_file: dict = dict()) -> None:
        filepath = os.path.join(self.DestFolder, "Question.json")
        with open(filepath, "w", encoding="utf-8") as outfile:
            json.dump(json_file, outfile, indent=4)