-- =========================================================
-- TrailUp - Script de criação do banco de dados
-- Baseado no create_database.sql original, com os seguintes
-- ajustes em relação à versão entregue:
--   1. Criada a tabela `favorito` (requisito 14 - estava faltando)
--   2. `evento` ganhou latitude/longitude/horarioSaida/imediata
--      para permitir exibir "salas" como pins no mapa em tempo real
--   3. `mapaOffline` ganhou `arquivoUrl` (o que é baixado)
--   4. `notificacao` e `denuncia` passaram a referenciar `usuario`
--      diretamente (destinatário / denunciante / denunciado)
--   5. `historicoTrilha` ganhou `idUsuario` (histórico é por usuário)
--   6. `trilha` ganhou `imagemUrl` e `tempoEstimadoMin`
-- =========================================================

CREATE DATABASE IF NOT EXISTS trilhas_db;
USE trilhas_db;

-- =========================================================
-- USUARIO
-- =========================================================
CREATE TABLE usuario (
    idUsuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    fotoPerfil VARCHAR(255),
    dataCadastro DATE
);

-- =========================================================
-- TRILHA
-- =========================================================
CREATE TABLE trilha (
    idTrilha INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    localizacao VARCHAR(200),
    distancia DOUBLE,              -- km
    duracao DOUBLE,                -- duração de referência (min)
    dificuldade VARCHAR(50),       -- FACIL | MODERADA | DIFICIL
    descricao TEXT,
    imagemUrl VARCHAR(255),
    tempoEstimadoMin DOUBLE        -- calculado automaticamente (req. 15)
);

-- =========================================================
-- AVALIACAO (N:N usuario x trilha)
-- =========================================================
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

-- =========================================================
-- FAVORITO (N:N usuario x trilha) - req. 14
-- =========================================================
CREATE TABLE favorito (
    idFavorito INT AUTO_INCREMENT PRIMARY KEY,
    dataSalvo DATE,
    idUsuario INT NOT NULL,
    idTrilha INT NOT NULL,

    UNIQUE KEY uq_favorito (idUsuario, idTrilha),
    FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario),
    FOREIGN KEY (idTrilha) REFERENCES trilha(idTrilha)
);

-- =========================================================
-- CHECKPOINT (ponto fixo de referência da trilha)
-- =========================================================
CREATE TABLE checkpoint (
    idCheckpoint INT AUTO_INCREMENT PRIMARY KEY,
    latitude DOUBLE,
    longitude DOUBLE,
    horario DATETIME,
    idTrilha INT NOT NULL,

    FOREIGN KEY (idTrilha) REFERENCES trilha(idTrilha)
);

-- =========================================================
-- FOTO (galeria geral da trilha) - req. 7
-- =========================================================
CREATE TABLE foto (
    idFoto INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255),
    legenda VARCHAR(255),
    idTrilha INT NOT NULL,

    FOREIGN KEY (idTrilha) REFERENCES trilha(idTrilha)
);

-- =========================================================
-- MAPA OFFLINE - req. 10
-- =========================================================
CREATE TABLE mapaOffline (
    idMapa INT AUTO_INCREMENT PRIMARY KEY,
    arquivoUrl VARCHAR(255),
    tamanhoArquivo DOUBLE,
    dataDownload DATE,
    idTrilha INT NOT NULL,

    FOREIGN KEY (idTrilha) REFERENCES trilha(idTrilha)
);

-- =========================================================
-- EVENTO ("sala de trilha" / expedição) - req. 17
-- =========================================================
CREATE TABLE evento (
    idEvento INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    descricao TEXT,
    data DATE,
    horarioSaida DATETIME,
    imediata BOOLEAN DEFAULT FALSE,
    vagas INT,
    tipo ENUM('INDIVIDUAL','GRUPO') NOT NULL,
    latitude DOUBLE,
    longitude DOUBLE,
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

-- =========================================================
-- NOTIFICACAO - req. 19
-- =========================================================
CREATE TABLE notificacao (
    idNotificacao INT AUTO_INCREMENT PRIMARY KEY,
    mensagem TEXT,
    dataEnvio DATETIME,
    lida BOOLEAN DEFAULT FALSE,
    idUsuario INT NOT NULL,
    idEvento INT,

    FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario),
    FOREIGN KEY (idEvento) REFERENCES evento(idEvento)
);

-- =========================================================
-- DENUNCIA - req. 13
-- =========================================================
CREATE TABLE denuncia (
    idDenuncia INT AUTO_INCREMENT PRIMARY KEY,
    descricao TEXT,
    dataEnvio DATETIME,
    status VARCHAR(50) DEFAULT 'PENDENTE',
    idEvento INT NOT NULL,
    idUsuarioDenunciante INT NOT NULL,
    idUsuarioDenunciado INT,

    FOREIGN KEY (idEvento) REFERENCES evento(idEvento),
    FOREIGN KEY (idUsuarioDenunciante) REFERENCES usuario(idUsuario),
    FOREIGN KEY (idUsuarioDenunciado) REFERENCES usuario(idUsuario)
);

-- =========================================================
-- HISTORICO TRILHA - req. 18
-- =========================================================
CREATE TABLE historicoTrilha (
    idHistorico INT AUTO_INCREMENT PRIMARY KEY,
    dataRealizacao DATE,
    tempo DOUBLE,
    avaliacaoPessoal INT,
    idUsuario INT NOT NULL,
    idEvento INT,
    idTrilha INT NOT NULL,

    FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario),
    FOREIGN KEY (idEvento) REFERENCES evento(idEvento),
    FOREIGN KEY (idTrilha) REFERENCES trilha(idTrilha)
);

-- =========================================================
-- REGISTRO REALIZADO (checkpoint via GPS durante a trilha) - req. 16
-- =========================================================
CREATE TABLE registroRealizado (
    idRegistro INT AUTO_INCREMENT PRIMARY KEY,
    latitude DOUBLE,
    longitude DOUBLE,
    horario DATETIME,
    observacao TEXT,
    idHistorico INT NOT NULL,

    FOREIGN KEY (idHistorico) REFERENCES historicoTrilha(idHistorico)
);

-- =========================================================
-- FOTO REGISTRO (foto vinculada ao checkpoint realizado) - req. 16
-- =========================================================
CREATE TABLE fotoRegistro (
    idFotoRegistro INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255),
    legenda VARCHAR(255),
    idRegistro INT NOT NULL,

    FOREIGN KEY (idRegistro) REFERENCES registroRealizado(idRegistro)
);
