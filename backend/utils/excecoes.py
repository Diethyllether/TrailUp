"""Exceções previsíveis dos casos de uso e seus status HTTP."""


class ErroDeDominio(Exception):
    status_http = 400

    def __init__(self, mensagem):
        super().__init__(mensagem)
        self.mensagem = mensagem


class ErroDeValidacao(ErroDeDominio):
    status_http = 400


class RecursoNaoEncontrado(ErroDeDominio):
    status_http = 404


class PermissaoNegada(ErroDeDominio):
    status_http = 403


class ConflitoDeDados(ErroDeDominio):
    status_http = 409


class NaoAutenticado(ErroDeDominio):
    status_http = 401
