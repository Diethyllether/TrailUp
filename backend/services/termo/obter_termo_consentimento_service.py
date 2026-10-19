from pathlib import Path

from utils.excecoes import RecursoNaoEncontrado


class ObterTermoConsentimentoService:
    def __init__(self, caminho=None):
        raiz = Path(__file__).resolve().parents[3]
        self.caminho = (
            Path(caminho)
            if caminho
            else raiz / "docs" / "TermoDeConsentimentoTrailUp.pdf"
        )

    def executar(self):
        if not self.caminho.is_file():
            raise RecursoNaoEncontrado(
                "PDF do termo de consentimento ainda não foi disponibilizado."
            )
        return self.caminho
