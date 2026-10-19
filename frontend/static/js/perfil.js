import { escaparHtml, elementoPrincipal, requisicaoApi, mostrarAviso } from "./api.js";
import { obterUsuarioAtual, definirUsuarioAtual } from "./state.js";
import { renderizarListaHistorico } from "./historico.js";

export async function renderizarPaginaPerfil() {
  const [respostaHistorico] = await Promise.all([requisicaoApi("/history")]);
  const usuario = obterUsuarioAtual();
  const foto = usuario?.fotoPerfil
    ? `<img class="profile-photo" src="${escaparHtml(usuario.fotoPerfil)}"
         alt="Foto de ${escaparHtml(usuario.nome)}">`
    : "";

  elementoPrincipal.innerHTML = `
    <section class="section"><div class="container">
      <h1>Perfil</h1>
      ${foto}
      <form class="panel form-grid" id="profile-form">
        <label>Nome<input name="nome" maxlength="100" required value="${escaparHtml(usuario?.nome || "")}"></label>
        <label>E-mail<input name="email" type="email" required value="${escaparHtml(usuario?.email || "")}"></label>
        <label>Foto (URL)<input name="fotoPerfil" type="url" value="${escaparHtml(usuario?.fotoPerfil || "")}"></label>
        <button class="button primary">Salvar perfil</button>
      </form>
      <h2 class="profile-history-title">Histórico de trilhas</h2>
      ${renderizarListaHistorico(respostaHistorico.items)}
    </div></section>`;
}

export async function tratarAtualizacaoPerfil(evento) {
  const formulario = evento.target;
  if (formulario.id !== "profile-form") {
    return false;
  }

  evento.preventDefault();
  const dados = Object.fromEntries(new FormData(formulario));
  try {
    const resposta = await requisicaoApi("/profile", {
      method: "PATCH",
      body: JSON.stringify(dados),
    });
    definirUsuarioAtual(resposta.user);
    mostrarAviso("Perfil atualizado.", "success");
    window.location.reload();
  } catch (erro) {
    mostrarAviso(erro.message, "danger");
  }
  return true;
}
