CREATE DATABASE trilhas_db;
USE trilhas_db;

CREATE TABLE usuario (
    idUsuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    fotoPerfil VARCHAR(255),
    dataCadastro DATE
);

CREATE TABLE trilha (
    idTrilha INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    localizacao VARCHAR(200),
    distancia DOUBLE,
    duracao DOUBLE,
    dificuldade VARCHAR(50),
    descricao TEXT
);

CREATE TABLE avaliacao (
    idAvaliacao INT AUTO_INCREMENT PRIMARY KEY,
    nota INT NOT NULL,
    comentario TEXT,
    data DATE,
    idUsuario INT NOT NULL,
    idTrilha INT NOT NULL,

    FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario),
    FOREIGN KEY (idTrilha) REFERENCES trilha(idTrilha)
);

CREATE TABLE checkpoint (
    idCheckpoint INT AUTO_INCREMENT PRIMARY KEY,
    latitude DOUBLE,
    longitude DOUBLE,
    horario DATETIME,
    idTrilha INT NOT NULL,

    FOREIGN KEY (idTrilha) REFERENCES trilha(idTrilha)
);

CREATE TABLE foto (
    idFoto INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255),
    legenda VARCHAR(255),
    idTrilha INT NOT NULL,

    FOREIGN KEY (idTrilha) REFERENCES trilha(idTrilha)
);

CREATE TABLE mapaOffline (
    idMapa INT AUTO_INCREMENT PRIMARY KEY,
    tamanhoArquivo DOUBLE,
    dataDownload DATE,
    idTrilha INT NOT NULL,

    FOREIGN KEY (idTrilha) REFERENCES trilha(idTrilha)
);

CREATE TABLE evento (
    idEvento INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    descricao TEXT,
    data DATE,
    vagas INT,
    tipo ENUM('INDIVIDUAL','GRUPO') NOT NULL,
    idCriador INT NOT NULL,

    FOREIGN KEY (idCriador) REFERENCES usuario(idUsuario)
);

-- Evento composto por uma ou mais trilhas
CREATE TABLE evento_trilha (
    idEvento INT,
    idTrilha INT,

    PRIMARY KEY (idEvento, idTrilha),

    FOREIGN KEY (idEvento) REFERENCES evento(idEvento),
    FOREIGN KEY (idTrilha) REFERENCES trilha(idTrilha)
);

-- Usuários participantes dos eventos
CREATE TABLE participante_evento (
    idUsuario INT,
    idEvento INT,

    PRIMARY KEY (idUsuario, idEvento),

    FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario),
    FOREIGN KEY (idEvento) REFERENCES evento(idEvento)
);

CREATE TABLE notificacao (
    idNotificacao INT AUTO_INCREMENT PRIMARY KEY,
    mensagem TEXT,
    dataEnvio DATETIME,
    lida BOOLEAN DEFAULT FALSE,
    idEvento INT NOT NULL,

    FOREIGN KEY (idEvento) REFERENCES evento(idEvento)
);

CREATE TABLE denuncia (
    idDenuncia INT AUTO_INCREMENT PRIMARY KEY,
    descricao TEXT,
    dataEnvio DATETIME,
    status VARCHAR(50),
    idEvento INT NOT NULL,

    FOREIGN KEY (idEvento) REFERENCES evento(idEvento)
);

CREATE TABLE historicoTrilha (
    idHistorico INT AUTO_INCREMENT PRIMARY KEY,
    dataRealizacao DATE,
    tempo DOUBLE,
    avaliacaoPessoal INT,
    idEvento INT NOT NULL,
    idTrilha INT NOT NULL,

    FOREIGN KEY (idEvento) REFERENCES evento(idEvento),
    FOREIGN KEY (idTrilha) REFERENCES trilha(idTrilha)
);

CREATE TABLE registroRealizado (
    idRegistro INT AUTO_INCREMENT PRIMARY KEY,
    latitude DOUBLE,
    longitude DOUBLE,
    horario DATETIME,
    observacao TEXT,
    idHistorico INT NOT NULL UNIQUE,

    FOREIGN KEY (idHistorico) REFERENCES historicoTrilha(idHistorico)
);

CREATE TABLE fotoRegistro (
    idFotoRegistro INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255),
    legenda VARCHAR(255),
    idRegistro INT NOT NULL,

    FOREIGN KEY (idRegistro) REFERENCES registroRealizado(idRegistro)
);
