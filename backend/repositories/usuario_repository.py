from models.usuario_model import Usuario
from repositories.base_repository import BaseRepository

class UsuarioRepository(BaseRepository):
    model = Usuario

    def buscar_por_email(self, email):
        return Usuario.query.filter_by(email=email).first()
