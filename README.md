# Generador Dinámico de Exámenes (LaTeX y Web)

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.x-black.svg)
![LaTeX](https://img.shields.io/badge/LaTeX-PDF-orange.svg)
![MathJax](https://img.shields.io/badge/MathJax-Web-green.svg)

Este proyecto es un sistema modular para generar dinámicamente preguntas de examen con parámetros aleatorios. Está diseñado para producir dos tipos de salida a partir de una única fuente de lógica:

1.  **PDFs de alta calidad** a través de LaTeX, ideales para imprimir.
2.  **Páginas web interactivas** a través de un servidor Flask, perfectas para visualización en línea.

La idea central es separar la lógica de un problema matemático (`create_question.py`) de la lógica de formato (`LibCreateQuestion.py`), permitiendo crear nuevas preguntas de manera sencilla y escalable.

---

## ✨ Características

* **Generación Aleatoria:** Cada pregunta se genera con valores numéricos diferentes en cada ejecución, creando versiones únicas del mismo problema.
* **Doble Formato de Salida:** Genera código LaTeX para PDFs y HTML para la web desde la misma lógica.
* **Servidor Web Integrado:** Utiliza Flask para servir las preguntas en una página web que renderiza las ecuaciones matemáticas con MathJax.
* **Estructura Modular:** Fácil de extender. Puedes añadir nuevos tipos de preguntas simplemente creando un nuevo script en la carpeta `Preguntas`.
* **Manejo Automático de Respuestas:** Mezcla aleatoriamente las opciones correctas e incorrectas.

---

## 📂 Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

/ExamenGeneratorWEB/
├── app.py                  # Servidor web Flask que muestra las preguntas.
├── templates/
│   └── index.html          # Plantilla HTML para visualizar la pregunta en la web.
└── ExamGenerator/
├── LibCreateQuestion.py  # Librería principal que formatea la salida (LaTeX o HTML).
├── ExamTemplate/         # Plantillas y configuraciones de LaTeX.
│   └── TemplateSimple.tex
└── Preguntas/
└── EspVec__OM__DepLin/
└── create_question.py # Lógica para un tipo de pregunta específico.

* **`create_question.py`**: Contiene la "receta" de un problema. Define las variables, los cálculos y el texto de la pregunta y sus respuestas.
* **`LibCreateQuestion.py`**: Es el motor de formato. Recibe los datos de `create_question.py` y los ensambla en formato LaTeX o HTML.
* **`app.py`**: Es el servidor que conecta la lógica de generación con el mundo exterior a través de una página web.

---

## 🛠️ Prerrequisitos

Antes de empezar, asegúrate de tener instalado el siguiente software:

1.  **Python** (versión 3.8 o superior).
2.  **Un compilador de LaTeX**, como [MiKTeX](https://miktex.org/) (para Windows), [MacTeX](https://www.tug.org/mactex/) (para macOS) o [TeX Live](https://www.tug.org/texlive/) (para Linux).
3.  **Git** (opcional, para clonar el repositorio).

---

## 🚀 Instalación

1.  **Clona el repositorio (o descarga el ZIP):**
    ```bash
    git clone <URL-del-repositorio>
    cd ExamenGeneratorWEB
    ```

2.  **Crea un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3.  **Instala las dependencias de Python:**
    ```bash
    pip install Flask numpy
    ```

---

## ⚙️ Uso

Este proyecto tiene dos modos de uso principales:

### 1. Generar Preguntas en la Web (HTML)

Este es el modo ideal para visualizar preguntas rápidamente en el navegador.

1.  **Inicia el servidor Flask:**
    Desde la carpeta raíz del proyecto (`ExamenGeneratorWEB`), ejecuta el siguiente comando en tu terminal:
    ```bash
    flask --app app run
    ```

2.  **Abre tu navegador:**
    Visita la dirección `http://127.0.0.1:5000`. Verás una nueva pregunta de álgebra lineal. Cada vez que recargues la página, se generará una nueva versión con números diferentes.

### 2. Generar Exámenes para Imprimir (PDF)

Este modo genera un archivo `.tex` que puedes compilar para crear un PDF de alta calidad.

1.  **Ejecuta el script de la pregunta:**
    Desde la terminal, ejecuta directamente el script de la pregunta que deseas generar. Esto creará un archivo `Response.tex` con el formato LaTeX correcto.
    ```bash
    python ExamGenerator/Preguntas/EspVec__OM__DepLin/create_question.py
    ```
    Verás un mensaje confirmando que el archivo `Response.tex` fue creado.

2.  **Compila el PDF:**
    Para crear el documento final, necesitas un archivo principal de LaTeX (como `TemplateSimple.tex`) que incluya `Response.tex`. Luego, compílalo usando `pdflatex`.
    *(Nota: Este proceso puede ser automatizado con un script adicional si se generan muchas preguntas).*

---

## 💡 Cómo Añadir Nuevas Preguntas

La arquitectura del proyecto hace que sea muy fácil añadir nuevos tipos de problemas.

1.  **Crea una nueva carpeta** dentro de `ExamGenerator/Preguntas/`. El nombre debe ser descriptivo, por ejemplo, `Calculo__Derivadas`.
2.  **Copia el archivo `create_question.py`** existente a esta nueva carpeta.
3.  **Modifica el nuevo `create_question.py`:**
    * Cambia el texto de la variable `Question`.
    * Ajusta la lógica de generación de parámetros y cálculos.
    * Reescribe las opciones en `dict_choices` para que coincidan con tu nuevo problema.
4.  **Actualiza `app.py`** para que importe y llame a tu nueva función `generar_pregunta` si quieres verla en la web.

---

## 📜 Licencia

La licencia para este proyecto aún no se ha determinado. Todos los derechos quedan reservados por el autor.
