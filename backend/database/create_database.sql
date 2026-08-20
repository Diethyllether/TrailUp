CREATE DATABASE IF NOT EXISTS trilhas_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE trilhas_db;

CREATE TABLE IF NOT EXISTS usuario (
    idUsuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    fotoPerfil VARCHAR(255) NULL,
    dataCadastro DATE DEFAULT (CURRENT_DATE)
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
    tempoEstimadoMin FLOAT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS evento (
    idEvento INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    descricao TEXT NULL,
    data DATE NULL,
    horarioSaida DATETIME NULL,
    imediata BOOLEAN DEFAULT FALSE,
    vagas INT NULL,
    tipo ENUM('INDIVIDUAL', 'GRUPO') NOT NULL,
    latitude FLOAT NULL,
    longitude FLOAT NULL,
    idCriador INT NOT NULL,
    CONSTRAINT fk_evento_criador
        FOREIGN KEY (idCriador) REFERENCES usuario(idUsuario)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS avaliacao (
    idAvaliacao INT AUTO_INCREMENT PRIMARY KEY,
    nota INT NOT NULL,
    comentario TEXT NULL,
    data DATE NULL,
    idUsuario INT NOT NULL,
    idTrilha INT NOT NULL,
    CONSTRAINT fk_avaliacao_usuario
        FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario),
    CONSTRAINT fk_avaliacao_trilha
        FOREIGN KEY (idTrilha) REFERENCES trilha(idTrilha)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS favorito (
    idFavorito INT AUTO_INCREMENT PRIMARY KEY,
    dataSalvo DATE DEFAULT (CURRENT_DATE),
    idUsuario INT NOT NULL,
    idTrilha INT NOT NULL,
    CONSTRAINT uq_favorito UNIQUE (idUsuario, idTrilha),
    CONSTRAINT fk_favorito_usuario
        FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario),
    CONSTRAINT fk_favorito_trilha
        FOREIGN KEY (idTrilha) REFERENCES trilha(idTrilha)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS checkpoint (
    idCheckpoint INT AUTO_INCREMENT PRIMARY KEY,
    latitude FLOAT NULL,
    longitude FLOAT NULL,
    horario DATETIME NULL,
    idTrilha INT NOT NULL,
    CONSTRAINT fk_checkpoint_trilha
        FOREIGN KEY (idTrilha) REFERENCES trilha(idTrilha)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS foto (
    idFoto INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255) NULL,
    legenda VARCHAR(255) NULL,
    idTrilha INT NOT NULL,
    CONSTRAINT fk_foto_trilha
        FOREIGN KEY (idTrilha) REFERENCES trilha(idTrilha)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS mapaOffline (
    idMapa INT AUTO_INCREMENT PRIMARY KEY,
    arquivoUrl VARCHAR(255) NULL,
    tamanhoArquivo FLOAT NULL,
    dataDownload DATE DEFAULT (CURRENT_DATE),
    idTrilha INT NOT NULL,
    CONSTRAINT fk_mapa_offline_trilha
        FOREIGN KEY (idTrilha) REFERENCES trilha(idTrilha)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS evento_trilha (
    idEvento INT NOT NULL,
    idTrilha INT NOT NULL,
    PRIMARY KEY (idEvento, idTrilha),
    CONSTRAINT fk_evento_trilha_evento
        FOREIGN KEY (idEvento) REFERENCES evento(idEvento),
    CONSTRAINT fk_evento_trilha_trilha
        FOREIGN KEY (idTrilha) REFERENCES trilha(idTrilha)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS participante_evento (
    idUsuario INT NOT NULL,
    idEvento INT NOT NULL,
    PRIMARY KEY (idUsuario, idEvento),
    CONSTRAINT fk_participante_usuario
        FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario),
    CONSTRAINT fk_participante_evento
        FOREIGN KEY (idEvento) REFERENCES evento(idEvento)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS notificacao (
    idNotificacao INT AUTO_INCREMENT PRIMARY KEY,
    mensagem TEXT NULL,
    dataEnvio DATETIME NULL,
    lida BOOLEAN DEFAULT FALSE,
    idUsuario INT NOT NULL,
    idEvento INT NULL,
    CONSTRAINT fk_notificacao_usuario
        FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario),
    CONSTRAINT fk_notificacao_evento
        FOREIGN KEY (idEvento) REFERENCES evento(idEvento)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS denuncia (
    idDenuncia INT AUTO_INCREMENT PRIMARY KEY,
    descricao TEXT NULL,
    dataEnvio DATETIME NULL,
    status VARCHAR(50) DEFAULT 'PENDENTE',
    idEvento INT NOT NULL,
    idUsuarioDenunciante INT NOT NULL,
    idUsuarioDenunciado INT NULL,
    CONSTRAINT fk_denuncia_evento
        FOREIGN KEY (idEvento) REFERENCES evento(idEvento),
    CONSTRAINT fk_denuncia_denunciante
        FOREIGN KEY (idUsuarioDenunciante) REFERENCES usuario(idUsuario),
    CONSTRAINT fk_denuncia_denunciado
        FOREIGN KEY (idUsuarioDenunciado) REFERENCES usuario(idUsuario)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS historicoTrilha (
    idHistorico INT AUTO_INCREMENT PRIMARY KEY,
    dataRealizacao DATE NULL,
    tempo FLOAT NULL,
    avaliacaoPessoal INT NULL,
    idUsuario INT NOT NULL,
    idEvento INT NULL,
    idTrilha INT NOT NULL,
    CONSTRAINT fk_historico_usuario
        FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario),
    CONSTRAINT fk_historico_evento
        FOREIGN KEY (idEvento) REFERENCES evento(idEvento),
    CONSTRAINT fk_historico_trilha
        FOREIGN KEY (idTrilha) REFERENCES trilha(idTrilha)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS registroRealizado (
    idRegistro INT AUTO_INCREMENT PRIMARY KEY,
    latitude FLOAT NULL,
    longitude FLOAT NULL,
    horario DATETIME NULL,
    observacao TEXT NULL,
    idHistorico INT NOT NULL,
    CONSTRAINT fk_registro_historico
        FOREIGN KEY (idHistorico) REFERENCES historicoTrilha(idHistorico)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS fotoRegistro (
    idFotoRegistro INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255) NULL,
    legenda VARCHAR(255) NULL,
    idRegistro INT NOT NULL,
    CONSTRAINT fk_foto_registro
        FOREIGN KEY (idRegistro) REFERENCES registroRealizado(idRegistro)
) ENGINE=InnoDB;
