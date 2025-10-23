-- Crear base de datos
CREATE DATABASE IF NOT EXISTS ExamenGeneratorWEB
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE ExamenGeneratorWEB;

-- Tabla de usuarios (docentes y alumnos)
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    rol ENUM('docente', 'alumno') NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de exámenes
CREATE TABLE examenes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    descripcion TEXT,
    id_docente INT NOT NULL,
    preguntas_json JSON NOT NULL,  -- Estructura de preguntas generadas
    respuestas_correctas_json JSON NOT NULL, -- Clave de respuestas correctas
    pdf_generado_path VARCHAR(255), -- PDF general del examen
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_docente) REFERENCES usuarios(id)
);

-- Tipos de preguntas (opcional para flexibilidad futura)
CREATE TABLE tipos_pregunta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL, -- ejemplo: 'opcion_multiple', 'abierta', 'verdadero_falso'
    descripcion TEXT
);

-- Tabla de preguntas (almacenadas individualmente para reutilización)
CREATE TABLE preguntas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_docente INT NOT NULL,
    tipo_id INT NOT NULL,
    enunciado_latex TEXT NOT NULL, -- texto en LaTeX renderizado con MathJax
    opciones_json JSON, -- sólo si aplica (opción múltiple)
    respuesta_correcta_json JSON, -- puede ser texto o índice (p. ej. {"correcta": 2})
    dificultad ENUM('baja', 'media', 'alta') DEFAULT 'media',
    tema VARCHAR(100),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_docente) REFERENCES usuarios(id),
    FOREIGN KEY (tipo_id) REFERENCES tipos_pregunta(id)
);

-- Tabla de intentos de examen por alumno
CREATE TABLE intentos_examen (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_examen INT NOT NULL,
    id_alumno INT NOT NULL,
    respuestas_json JSON NOT NULL, -- incluye índice de pregunta y respuesta dada
    calificacion DECIMAL(5,2),
    pdf_respuestas_path VARCHAR(255), -- PDF del alumno con sus respuestas
    fecha_presentacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_examen) REFERENCES examenes(id),
    FOREIGN KEY (id_alumno) REFERENCES usuarios(id)
);

-- Índices
CREATE INDEX idx_usuario_rol ON usuarios(rol);
CREATE INDEX idx_examen_docente ON examenes(id_docente);
CREATE INDEX idx_intentos_alumno ON intentos_examen(id_alumno);
