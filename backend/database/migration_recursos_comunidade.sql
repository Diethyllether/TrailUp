USE trilhas_db;

-- Execute uma vez em bancos criados antes dos comentários e relatos de trilha.
CREATE TABLE IF NOT EXISTS comentario_evento (
    idComentario INT AUTO_INCREMENT PRIMARY KEY,
    texto TEXT NOT NULL,
    dataEnvio DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    idUsuario INT NOT NULL,
    idEvento INT NOT NULL,
    CONSTRAINT fk_comentario_evento_usuario FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_comentario_evento_evento FOREIGN KEY (idEvento) REFERENCES evento(idEvento) ON UPDATE CASCADE ON DELETE CASCADE,
    INDEX idx_comentario_evento (idEvento, dataEnvio)
) ENGINE=InnoDB;

ALTER TABLE denuncia
    MODIFY idEvento INT NULL,
    ADD COLUMN categoria VARCHAR(30) NOT NULL DEFAULT 'EVENTO' AFTER status,
    ADD COLUMN idTrilha INT NULL AFTER idEvento,
    ADD CONSTRAINT fk_denuncia_trilha FOREIGN KEY (idTrilha) REFERENCES trilha(idTrilha) ON UPDATE CASCADE ON DELETE CASCADE;
