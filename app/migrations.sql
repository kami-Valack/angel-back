-- SQL para criar as tabelas principais do sistema de ensino

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    bio TEXT,
    avatar VARCHAR(512),
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(64),
    level VARCHAR(32),
    thumbnail VARCHAR(512),
    price VARCHAR(32),
    tags TEXT,
    published BOOLEAN DEFAULT FALSE,
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS modules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    courseId INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    `order` INT,
    totalLessons INT DEFAULT 0,
    totalDuration INT DEFAULT 0,
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (courseId) REFERENCES courses(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS lessons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    moduleId INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    content TEXT,
    videoUrl VARCHAR(512),
    duration INT,
    `order` INT,
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (moduleId) REFERENCES modules(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS resources (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lessonId INT NOT NULL,
    title VARCHAR(255),
    type VARCHAR(32),
    url VARCHAR(512),
    FOREIGN KEY (lessonId) REFERENCES lessons(id) ON DELETE CASCADE
);

-- Tabela para categorias de cursos
CREATE TABLE IF NOT EXISTS categories (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    icon VARCHAR(512),
    description TEXT
);

-- Tabela para progresso do usuário em cursos, módulos e lições
CREATE TABLE IF NOT EXISTS user_progress (
    id INT AUTO_INCREMENT PRIMARY KEY,
    userId INT NOT NULL,
    courseId INT,
    moduleId INT,
    lessonId INT,
    completed BOOLEAN DEFAULT 0,
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (userId) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (courseId) REFERENCES courses(id) ON DELETE CASCADE,
    FOREIGN KEY (moduleId) REFERENCES modules(id) ON DELETE CASCADE,
    FOREIGN KEY (lessonId) REFERENCES lessons(id) ON DELETE CASCADE
);
