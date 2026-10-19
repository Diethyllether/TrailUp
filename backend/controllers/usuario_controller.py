from flask import jsonify, request, session

from services.usuario.atualizar_perfil_service import AtualizarPerfilService


class UsuarioController:
    @staticmethod
    def atualizar_perfil():
        dados = request.get_json(silent=True) or {}
        usuario = AtualizarPerfilService().executar(session["id_usuario"], dados)
        return jsonify(user=usuario)
