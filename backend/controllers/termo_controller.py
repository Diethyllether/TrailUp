from flask import send_file

from services.termo.obter_termo_consentimento_service import ObterTermoConsentimentoService


class TermoController:
    @staticmethod
    def servir():
        caminho = ObterTermoConsentimentoService().executar()
        return send_file(caminho, mimetype="application/pdf", as_attachment=False)
