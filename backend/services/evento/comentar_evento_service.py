from models.comentario_evento_model import ComentarioEvento
from models.participante_evento_model import ParticipanteEvento
from utils.excecoes import ErroDeValidacao, PermissaoNegada


class ComentarEventoService:
    def __init__(self, modelo_comentario=None, modelo_participante=None):
        self.modelo_comentario = modelo_comentario or ComentarioEvento
        self.modelo_participante = modelo_participante or ParticipanteEvento

    def executar(self, id_evento, id_usuario, texto):
        if self.modelo_participante.buscar(id_usuario, id_evento) is None:
            raise PermissaoNegada("apenas participantes confirmados podem comentar")
        texto = (texto or "").strip()
        if not texto or len(texto) > 2000:
            raise ErroDeValidacao("comentário deve ter entre 1 e 2000 caracteres")
        comentario = self.modelo_comentario(
            texto=texto, idUsuario=id_usuario, idEvento=id_evento
        ).salvar()
        return comentario.to_dict()
