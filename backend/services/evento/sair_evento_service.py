from models.participante_evento_model import ParticipanteEvento


class SairEventoService:
    def __init__(self, modelo_participante=None):
        self.modelo_participante = modelo_participante or ParticipanteEvento

    def executar(self, id_evento, id_usuario):
        participante = self.modelo_participante.buscar(id_usuario, id_evento)
        if participante:
            participante.deletar()
        return {"participating": False}
