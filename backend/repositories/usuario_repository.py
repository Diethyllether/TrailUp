from models.usuario_model import Usuario
from repositories.base_repository import BaseRepository

class UsuarioRepository(BaseRepository):
    """Consultas específicas de usuário. CRUD simples permanece na Model."""

    model = Usuario

    def buscar_por_email(self, email):
        return Usuario.query.filter_by(email=email).first()
