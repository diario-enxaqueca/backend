-- Script de inicialização do banco de dados Diário de Enxaqueca

USE diario_enxaqueca;

-- =====================================================
-- TABELA: usuarios
-- =====================================================
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABELA: gatilhos
-- =====================================================
CREATE TABLE IF NOT EXISTS gatilhos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    UNIQUE KEY unique_gatilho_por_usuario (usuario_id, nome),
    INDEX idx_usuario (usuario_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABELA: medicacoes
-- =====================================================
CREATE TABLE IF NOT EXISTS medicacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    dosagem VARCHAR(100),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    UNIQUE KEY unique_medicacao_por_usuario (usuario_id, nome),
    INDEX idx_usuario (usuario_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABELA: episodios
-- =====================================================
CREATE TABLE IF NOT EXISTS episodios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    data DATE NOT NULL,
    intensidade INT NOT NULL CHECK (intensidade >= 0 AND intensidade <= 10),
    duracao INT,  -- em minutos
    observacoes TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    INDEX idx_usuario (usuario_id),
    INDEX idx_data (data),
    INDEX idx_intensidade (intensidade)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABELA: episodio_gatilho (N:N)
-- =====================================================
CREATE TABLE IF NOT EXISTS episodio_gatilho (
    episodio_id INT NOT NULL,
    gatilho_id INT NOT NULL,
    PRIMARY KEY (episodio_id, gatilho_id),
    FOREIGN KEY (episodio_id) REFERENCES episodios(id) ON DELETE CASCADE,
    FOREIGN KEY (gatilho_id) REFERENCES gatilhos(id) ON DELETE CASCADE,
    INDEX idx_episodio (episodio_id),
    INDEX idx_gatilho (gatilho_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABELA: episodio_medicacao (N:N)
-- =====================================================
CREATE TABLE IF NOT EXISTS episodio_medicacao (
    episodio_id INT NOT NULL,
    medicacao_id INT NOT NULL,
    PRIMARY KEY (episodio_id, medicacao_id),
    FOREIGN KEY (episodio_id) REFERENCES episodios(id) ON DELETE CASCADE,
    FOREIGN KEY (medicacao_id) REFERENCES medicacoes(id) ON DELETE CASCADE,
    INDEX idx_episodio (episodio_id),
    INDEX idx_medicacao (medicacao_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- DADOS DE EXEMPLO (OPCIONAL - para testes)
-- =====================================================

-- Inserir usuário de teste
-- Senha: senha123 (hash bcrypt)
INSERT INTO usuarios (nome, email, senha_hash) VALUES
('Usuário Teste', 'teste@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5K/6JCGE.J7K2');

-- Inserir gatilhos de exemplo
INSERT INTO gatilhos (usuario_id, nome) VALUES
(1, 'Estresse'),
(1, 'Falta de sono'),
(1, 'Chocolate'),
(1, 'Café'),
(1, 'Luz forte');

-- Inserir medicações de exemplo
INSERT INTO medicacoes (usuario_id, nome, dosagem) VALUES
(1, 'Paracetamol', '500mg'),
(1, 'Ibuprofeno', '400mg');

-- Inserir episódio de exemplo
INSERT INTO episodios (usuario_id, data, intensidade, duracao, observacoes) VALUES
(1, '2025-10-23', 8, 240, 'Episódio após reunião estressante');

-- Associar gatilhos ao episódio
INSERT INTO episodio_gatilho (episodio_id, gatilho_id) VALUES
(1, 1), -- Estresse
(1, 2); -- Falta de sono

-- Associar medicação ao episódio
INSERT INTO episodio_medicacao (episodio_id, medicacao_id) VALUES
(1, 1); -- Paracetamol
