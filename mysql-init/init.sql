-- mysql-init/init.sql
CREATE DATABASE IF NOT EXISTS diario CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE diario;

-- Tabela de usuários
CREATE TABLE IF NOT EXISTS usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL, -- armazene hash da senha
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabela de entradas (registro de enxaqueca)
CREATE TABLE IF NOT EXISTS entrada (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    data DATE NOT NULL,
    intensidade TINYINT NOT NULL CHECK (intensidade BETWEEN 0 AND 10),
    observacoes VARCHAR(500),
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabela de gatilhos (1 entrada -> N gatilhos)
CREATE TABLE IF NOT EXISTS gatilho (
    id INT AUTO_INCREMENT PRIMARY KEY,
    entrada_id INT NOT NULL,
    tipo VARCHAR(100) NOT NULL,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (entrada_id) REFERENCES entrada(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabela de medicações (Medicacao) (1 entrada -> N medicacoes)
CREATE TABLE IF NOT EXISTS medicacao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    entrada_id INT NOT NULL,
    nome_medicacao VARCHAR(150) NOT NULL,
    dosagem VARCHAR(100),
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (entrada_id) REFERENCES entrada(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabela opcional para cache do dashboard (estatísticas pré-calculadas)
CREATE TABLE IF NOT EXISTS dashboard_cache (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NULL, -- se vazio = global; se preenchido = estatísticas por usuário
    media_intensidade FLOAT NULL,
    episodios_por_mes JSON NULL,   -- ex: {"2025-09": 4, "2025-08": 2}
    gatilhos_comuns JSON NULL,     -- ex: {"estresse": 5, "sono": 3}
    atualizado_em DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
