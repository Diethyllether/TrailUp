from models.usuario_model import Usuario

class UsuarioRepository:
    """Consultas específicas de usuário. CRUD simples permanece na Model."""

    def buscar_por_email(self, email):
        return Usuario.query.filter_by(email=email).first()
