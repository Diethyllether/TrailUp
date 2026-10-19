USE trilhas_db;

-- Atualiza bancos existentes sem inventar consentimento para contas antigas.
-- As colunas ficam NULL para registros legados sem evidência de aceite.
ALTER TABLE usuario
    ADD COLUMN termoAceitoEm DATETIME NULL,
    ADD COLUMN versaoTermo VARCHAR(20) NULL;

CREATE TABLE checklist_usuario (
    idUsuario INT NOT NULL,
    idChecklistItem INT NOT NULL,
    marcado BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (idUsuario, idChecklistItem),
    CONSTRAINT fk_checklist_usuario_usuario FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_checklist_usuario_item FOREIGN KEY (idChecklistItem) REFERENCES checklist_item(idChecklistItem)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE token_recuperacao (
    idToken INT AUTO_INCREMENT PRIMARY KEY,
    idUsuario INT NOT NULL,
    tokenHash CHAR(64) NOT NULL UNIQUE,
    expiraEm DATETIME NOT NULL,
    usadoEm DATETIME NULL,
    CONSTRAINT fk_token_recuperacao_usuario FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario)
        ON UPDATE CASCADE ON DELETE CASCADE,
    INDEX idx_token_recuperacao_expira (expiraEm)
) ENGINE=InnoDB;

-- Novos cadastros devem exigir aceite e gravar ambas as colunas.
-- Defina uma política de reconsentimento para contas legadas antes de tornar
-- termoAceitoEm e versaoTermo NOT NULL nesta base já existente.
