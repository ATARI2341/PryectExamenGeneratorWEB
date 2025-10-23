-- =========================================================
-- DATABASE: ExamenGeneratorWEB
-- DESCRIPTION: Sistema de generación automática de exámenes
--              con soporte LaTeX (MathJax) y almacenamiento
--              de PDFs por alumno y examen.
-- AUTHOR: Aaron
-- =========================================================

-- Crear base de datos (ejecutar solo si no existe)
CREATE DATABASE "ExamenGeneratorWEB";
\c "ExamenGeneratorWEB";

-- ================================
-- 1. TABLA: users
-- ================================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    role VARCHAR(20) CHECK (role IN ('teacher', 'student')) NOT NULL,
    full_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- ================================
-- 2. TABLA: courses
-- ================================
CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    teacher_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ================================
-- 3. TABLA: question_bank
-- ================================
CREATE TABLE question_bank (
    id SERIAL PRIMARY KEY,
    course_id INT REFERENCES courses(id) ON DELETE CASCADE,
    teacher_id INT REFERENCES users(id) ON DELETE SET NULL,
    title VARCHAR(150),
    question_template TEXT NOT NULL, -- Ej: "Calcula la derivada de $f(x)={{a}}x^{{n}}$"
    latex_code TEXT,                 -- Representación completa LaTeX opcional
    parameters_json JSONB,           -- {"a":{"min":1,"max":5},"n":{"min":2,"max":5}}
    correct_answer_json JSONB,       -- {"formula":"{{a*n}}x^{{n-1}}"}
    type VARCHAR(30) CHECK (type IN (
        'open', 'multiple_choice', 'true_false',
        'fill_blank', 'match_pairs', 'numeric', 'graphical'
    )) NOT NULL,
    difficulty_level INT DEFAULT 1 CHECK (difficulty_level BETWEEN 1 AND 5),
    topic VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ================================
-- 4. TABLA: exams
-- ================================
CREATE TABLE exams (
    id SERIAL PRIMARY KEY,
    course_id INT REFERENCES courses(id) ON DELETE CASCADE,
    teacher_id INT REFERENCES users(id) ON DELETE SET NULL,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    config_json JSONB,  -- {"num_questions":10,"difficulty":[1,3],"topics":["Derivadas"],"randomize_params":true}
    regenerate_seed BIGINT, -- semilla para regenerar versión idéntica
    pdf_path TEXT, -- ruta al PDF generado del examen base
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- ================================
-- 5. TABLA: exam_questions
-- ================================
CREATE TABLE exam_questions (
    id SERIAL PRIMARY KEY,
    exam_id INT REFERENCES exams(id) ON DELETE CASCADE,
    question_index INT NOT NULL,
    question_id INT REFERENCES question_bank(id) ON DELETE SET NULL,
    rendered_question_json JSONB NOT NULL,
    -- {"question":"Calcula la derivada de $f(x)=3x^4$", "options":["12x^3","x^2"], "correct_answer_index":0, "type":"multiple_choice"}
    parameters_used JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ================================
-- 6. TABLA: student_exams
-- ================================
CREATE TABLE student_exams (
    id SERIAL PRIMARY KEY,
    student_id INT REFERENCES users(id) ON DELETE CASCADE,
    exam_id INT REFERENCES exams(id) ON DELETE CASCADE,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    finished_at TIMESTAMP,
    score DECIMAL(5,2),
    status VARCHAR(20) CHECK (status IN ('pending','in_progress','completed')) DEFAULT 'pending',
    pdf_path TEXT  -- ruta al PDF generado para este alumno
);

-- ================================
-- 7. TABLA: student_answers
-- ================================
CREATE TABLE student_answers (
    id SERIAL PRIMARY KEY,
    student_exam_id INT REFERENCES student_exams(id) ON DELETE CASCADE,
    question_index INT NOT NULL,
    question_id INT REFERENCES exam_questions(id) ON DELETE CASCADE,
    answer_json JSONB NOT NULL,
    -- Ejemplos:
    -- multiple_choice: {"selected_index":2}
    -- open: {"latex":"12x^3"}
    -- true_false: {"value":true}
    -- numeric: {"value":3.1416}
    -- match_pairs: {"pairs":[{"left":"f'(x)","right":"2x"}]}
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    auto_score DECIMAL(5,2),
    manual_score DECIMAL(5,2),
    total_score DECIMAL(5,2) GENERATED ALWAYS AS (COALESCE(auto_score,0) + COALESCE(manual_score,0)) STORED
);

-- ================================
-- 8. ÍNDICES
-- ================================
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_question_topic ON question_bank(topic);
CREATE INDEX idx_exam_seed ON exams(regenerate_seed);
CREATE INDEX idx_exam_question_index ON exam_questions(exam_id, question_index);
CREATE INDEX idx_student_exam_status ON student_exams(status);
CREATE INDEX idx_answer_index ON student_answers(student_exam_id, question_index);

-- ================================
-- 9. EJEMPLO DE USO (opcional)
-- ================================
-- INSERT INTO users (username, password_hash, email, role, full_name)
-- VALUES ('prof_math', 'hashed_pass', 'prof@uni.edu', 'teacher', 'Prof. Matemáticas');

-- INSERT INTO courses (name, description, teacher_id)
-- VALUES ('Cálculo I', 'Curso de derivadas e integrales básicas', 1);

-- =========================================================
-- FIN DEL SCRIPT
-- =========================================================
