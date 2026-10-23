from flask import jsonify, request, session

from services.usuario.atualizar_perfil_service import AtualizarPerfilService
from services.usuario.exportar_dados_usuario_service import ExportarDadosUsuarioService


class UsuarioController:
    @staticmethod
    def atualizar_perfil():
        dados = request.get_json(silent=True) or {}
        usuario = AtualizarPerfilService().executar(session["id_usuario"], dados)
        return jsonify(user=usuario)

    @staticmethod
    def exportar_dados():
        dados = ExportarDadosUsuarioService().executar(session["id_usuario"])
        resposta = jsonify(dados)
        resposta.headers["Content-Disposition"] = 'attachment; filename="trailup-meus-dados.json"'
        return resposta
