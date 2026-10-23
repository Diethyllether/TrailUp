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
      <div class="panel profile-export">
        <h2>Meus dados (LGPD)</h2>
        <p>Baixe uma cópia em JSON de todos os dados que o TrailUp guarda sobre você: perfil, favoritos, avaliações, histórico, checklist, expedições, comentários e reportes. A senha não é incluída.</p>
        <button class="button ghost" type="button" data-action="export-data">Baixar meus dados</button>
      </div>
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

export async function tratarExportacaoDados(evento) {
  const botao = evento.target.closest('[data-action="export-data"]');
  if (!botao) {
    return false;
  }

  try {
    const dados = await requisicaoApi("/profile/export");
    const arquivo = new Blob([JSON.stringify(dados, null, 2)], { type: "application/json" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(arquivo);
    link.download = "trailup-meus-dados.json";
    document.body.append(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(link.href);
    mostrarAviso("Seus dados foram exportados.", "success");
  } catch (erro) {
    mostrarAviso(erro.message, "danger");
  }
  return true;
}
