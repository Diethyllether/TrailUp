CREATE DATABASE IF NOT EXISTS trilhas_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE trilhas_db;

-- ============================================================
-- TrailUp - modelo atual do banco de dados
-- Versão web Flask + Jinja2 + Google Maps
--
-- A antiga entidade mapaOffline foi removida do schema ativo.
-- A rota visualizada no Google Maps é formada pelos checkpoints GPS
-- registrados para cada trilha.
-- ============================================================

CREATE TABLE IF NOT EXISTS usuario (
    idUsuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    fotoPerfil VARCHAR(255) NULL,
    dataCadastro DATE NOT NULL DEFAULT (CURRENT_DATE),
    INDEX idx_usuario_nome (nome)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS trilha (
    idTrilha INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    localizacao VARCHAR(200) NULL,
    distancia FLOAT NULL,
    duracao FLOAT NULL,
    dificuldade VARCHAR(50) NULL,
    descricao TEXT NULL,
    imagemUrl VARCHAR(255) NULL,
    tempoEstimadoMin FLOAT NULL,
    CONSTRAINT chk_trilha_distancia
        CHECK (distancia IS NULL OR distancia >= 0),
    CONSTRAINT chk_trilha_duracao
        CHECK (duracao IS NULL OR duracao >= 0),
    CONSTRAINT chk_trilha_tempo_estimado
        CHECK (tempoEstimadoMin IS NULL OR tempoEstimadoMin >= 0),
    INDEX idx_trilha_nome (nome),
    INDEX idx_trilha_localizacao (localizacao),
    INDEX idx_trilha_dificuldade (dificuldade)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS evento (
    idEvento INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    descricao TEXT NULL,
    data DATE NULL,
    horarioSaida DATETIME NULL,
    imediata BOOLEAN NOT NULL DEFAULT FALSE,
    vagas INT NULL,
    tipo ENUM('INDIVIDUAL', 'GRUPO') NOT NULL,
    latitude FLOAT NULL,
    longitude FLOAT NULL,
    idCriador INT NOT NULL,
    CONSTRAINT chk_evento_vagas
        CHECK (vagas IS NULL OR vagas > 0),
    CONSTRAINT chk_evento_latitude
        CHECK (latitude IS NULL OR latitude BETWEEN -90 AND 90),
    CONSTRAINT chk_evento_longitude
        CHECK (longitude IS NULL OR longitude BETWEEN -180 AND 180),
    CONSTRAINT fk_evento_criador
        FOREIGN KEY (idCriador) REFERENCES usuario(idUsuario)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    INDEX idx_evento_data (data),
    INDEX idx_evento_criador (idCriador),
    INDEX idx_evento_mapa (latitude, longitude)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS avaliacao (
    idAvaliacao INT AUTO_INCREMENT PRIMARY KEY,
    nota INT NOT NULL,
    comentario TEXT NULL,
    data DATE NOT NULL DEFAULT (CURRENT_DATE),
    idUsuario INT NOT NULL,
    idTrilha INT NOT NULL,
    CONSTRAINT chk_avaliacao_nota CHECK (nota BETWEEN 1 AND 5),
    CONSTRAINT fk_avaliacao_usuario
        FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_avaliacao_trilha
        FOREIGN KEY (idTrilha) REFERENCES trilha(idTrilha)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    INDEX idx_avaliacao_usuario (idUsuario),
    INDEX idx_avaliacao_trilha (idTrilha)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS favorito (
    idFavorito INT AUTO_INCREMENT PRIMARY KEY,
    dataSalvo DATE NOT NULL DEFAULT (CURRENT_DATE),
    idUsuario INT NOT NULL,
    idTrilha INT NOT NULL,
    CONSTRAINT uq_favorito UNIQUE (idUsuario, idTrilha),
    CONSTRAINT fk_favorito_usuario
        FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_favorito_trilha
        FOREIGN KEY (idTrilha) REFERENCES trilha(idTrilha)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    INDEX idx_favorito_trilha (idTrilha)
) ENGINE=InnoDB;

-- Os checkpoints formam a geometria usada pela Polyline do Google Maps.
-- A ordem de idCheckpoint representa a ordem padrão da rota.
CREATE TABLE IF NOT EXISTS checkpoint (
    idCheckpoint INT AUTO_INCREMENT PRIMARY KEY,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    horario DATETIME NULL,
    idTrilha INT NOT NULL,
    CONSTRAINT chk_checkpoint_latitude CHECK (latitude BETWEEN -90 AND 90),
    CONSTRAINT chk_checkpoint_longitude CHECK (longitude BETWEEN -180 AND 180),
    CONSTRAINT fk_checkpoint_trilha
        FOREIGN KEY (idTrilha) REFERENCES trilha(idTrilha)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    INDEX idx_checkpoint_trilha (idTrilha, idCheckpoint)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS foto (
    idFoto INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255) NOT NULL,
    legenda VARCHAR(255) NULL,
    idTrilha INT NOT NULL,
    CONSTRAINT fk_foto_trilha
        FOREIGN KEY (idTrilha) REFERENCES trilha(idTrilha)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    INDEX idx_foto_trilha (idTrilha)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS evento_trilha (
    idEvento INT NOT NULL,
    idTrilha INT NOT NULL,
    PRIMARY KEY (idEvento, idTrilha),
    CONSTRAINT fk_evento_trilha_evento
        FOREIGN KEY (idEvento) REFERENCES evento(idEvento)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_evento_trilha_trilha
        FOREIGN KEY (idTrilha) REFERENCES trilha(idTrilha)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    INDEX idx_evento_trilha_trilha (idTrilha)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS participante_evento (
    idUsuario INT NOT NULL,
    idEvento INT NOT NULL,
    PRIMARY KEY (idUsuario, idEvento),
    CONSTRAINT fk_participante_usuario
        FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_participante_evento
        FOREIGN KEY (idEvento) REFERENCES evento(idEvento)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    INDEX idx_participante_evento (idEvento)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS notificacao (
    idNotificacao INT AUTO_INCREMENT PRIMARY KEY,
    mensagem TEXT NOT NULL,
    dataEnvio DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    lida BOOLEAN NOT NULL DEFAULT FALSE,
    idUsuario INT NOT NULL,
    idEvento INT NULL,
    CONSTRAINT fk_notificacao_usuario
        FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_notificacao_evento
        FOREIGN KEY (idEvento) REFERENCES evento(idEvento)
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    INDEX idx_notificacao_usuario_lida (idUsuario, lida),
    INDEX idx_notificacao_evento (idEvento)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS denuncia (
    idDenuncia INT AUTO_INCREMENT PRIMARY KEY,
    descricao TEXT NOT NULL,
    dataEnvio DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDENTE',
    idEvento INT NOT NULL,
    idUsuarioDenunciante INT NOT NULL,
    idUsuarioDenunciado INT NULL,
    CONSTRAINT chk_denuncia_status
        CHECK (status IN ('PENDENTE', 'EM_ANALISE', 'RESOLVIDA', 'ARQUIVADA')),
    CONSTRAINT fk_denuncia_evento
        FOREIGN KEY (idEvento) REFERENCES evento(idEvento)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_denuncia_denunciante
        FOREIGN KEY (idUsuarioDenunciante) REFERENCES usuario(idUsuario)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_denuncia_denunciado
        FOREIGN KEY (idUsuarioDenunciado) REFERENCES usuario(idUsuario)
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    INDEX idx_denuncia_evento (idEvento),
    INDEX idx_denuncia_status (status),
    INDEX idx_denuncia_denunciante (idUsuarioDenunciante),
    INDEX idx_denuncia_denunciado (idUsuarioDenunciado)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS historicoTrilha (
    idHistorico INT AUTO_INCREMENT PRIMARY KEY,
    dataRealizacao DATE NOT NULL DEFAULT (CURRENT_DATE),
    tempo FLOAT NULL,
    avaliacaoPessoal INT NULL,
    idUsuario INT NOT NULL,
    idEvento INT NULL,
    idTrilha INT NOT NULL,
    CONSTRAINT chk_historico_tempo CHECK (tempo IS NULL OR tempo >= 0),
    CONSTRAINT chk_historico_avaliacao
        CHECK (avaliacaoPessoal IS NULL OR avaliacaoPessoal BETWEEN 1 AND 5),
    CONSTRAINT fk_historico_usuario
        FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_historico_evento
        FOREIGN KEY (idEvento) REFERENCES evento(idEvento)
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    CONSTRAINT fk_historico_trilha
        FOREIGN KEY (idTrilha) REFERENCES trilha(idTrilha)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    INDEX idx_historico_usuario (idUsuario),
    INDEX idx_historico_trilha (idTrilha),
    INDEX idx_historico_evento (idEvento),
    INDEX idx_historico_data (dataRealizacao)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS registroRealizado (
    idRegistro INT AUTO_INCREMENT PRIMARY KEY,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    horario DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    observacao TEXT NULL,
    idHistorico INT NOT NULL,
    CONSTRAINT chk_registro_latitude CHECK (latitude BETWEEN -90 AND 90),
    CONSTRAINT chk_registro_longitude CHECK (longitude BETWEEN -180 AND 180),
    CONSTRAINT fk_registro_historico
        FOREIGN KEY (idHistorico) REFERENCES historicoTrilha(idHistorico)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    INDEX idx_registro_historico (idHistorico, idRegistro)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS fotoRegistro (
    idFotoRegistro INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255) NOT NULL,
    legenda VARCHAR(255) NULL,
    idRegistro INT NOT NULL,
    CONSTRAINT fk_foto_registro
        FOREIGN KEY (idRegistro) REFERENCES registroRealizado(idRegistro)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    INDEX idx_foto_registro_registro (idRegistro)
) ENGINE=InnoDB;
