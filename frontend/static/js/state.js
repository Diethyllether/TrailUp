let usuarioAtual = null;

export function obterUsuarioAtual() {
  return usuarioAtual;
}

export function definirUsuarioAtual(usuario) {
  usuarioAtual = usuario;
}
