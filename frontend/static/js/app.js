import {
  elementoNavegacao,
  elementoPrincipal,
  escaparHtml,
  requisicaoApi,
} from "./api.js";
import { definirUsuarioAtual, obterUsuarioAtual } from "./state.js";
import { renderizarPaginaAcesso, renderizarPaginaRedefinicao, tratarEnvioDeAcesso, tratarEnvioDeSenha, tratarCliqueDeSessao } from "./auth.js";
import { renderizarPaginaInicial, renderizarPaginaTrilha, tratarFiltrosTrilhas, tratarAcoesDeTrilha } from "./trilhas.js";
import { renderizarPaginaFavoritos } from "./favoritos.js";
import { renderizarPaginaEventos, tratarEnvioEvento, tratarAcoesEvento } from "./eventos.js";
import { tratarPublicacaoAvaliacao, tratarAcoesAvaliacao } from "./avaliacoes.js";
import { tratarRegistroHistorico } from "./historico.js";
import { renderizarPaginaPerfil, tratarAtualizacaoPerfil, tratarExportacaoDados } from "./perfil.js";
import { renderizarPaginaRanking, renderizarPaginaResumo, tratarRelatoProblema } from "./relatorios.js";
import { tratarMarcacaoChecklist } from "./checklist.js";

function renderizarNavegacao() {
  const links = obterLinksNavegacao(obterUsuarioAtual());
  elementoNavegacao.innerHTML = links;
}

function obterLinksNavegacao(usuario) {
  const linksConta = usuario
    ? `<a href="/?page=favorites">Favoritos</a>
       <a href="/?page=profile">Perfil</a>
       <a href="/?page=summary">Resumo</a>
       <a href="/?page=ranking">Ranking</a>
       <button class="link-button" data-action="logout">Sair</button>`
    : `<a href="/?page=login">Entrar</a>
       <a class="nav-cta" href="/?page=register">Criar conta</a>`;

  return `<a href="/">Home</a>
    <a href="/?page=events">Expedições</a>
    ${linksConta}`;
}

async function renderizarAplicacao() {
  try {
    const sessao = await requisicaoApi("/session");
    definirUsuarioAtual(sessao.user);
    renderizarNavegacao();

    const parametros = new URLSearchParams(location.search);
    const pagina = parametros.get("page");

    if (pagina === "login") {
      renderizarPaginaAcesso();
    } else if (pagina === "register") {
      renderizarPaginaAcesso(true);
    } else if (pagina === "forgot-password" || pagina === "reset-password") {
      renderizarPaginaRedefinicao();
    } else if (pagina === "trail") {
      await renderizarPaginaTrilha(parametros.get("id"));
    } else if (pagina === "events") {
      await renderizarPaginaEventos();
    } else if (pagina === "favorites") {
      if (obterUsuarioAtual()) {
        await renderizarPaginaFavoritos();
      } else {
        renderizarPaginaAcesso();
      }
    } else if (pagina === "profile") {
      if (obterUsuarioAtual()) {
        await renderizarPaginaPerfil();
      } else {
        renderizarPaginaAcesso();
      }
    } else if (pagina === "ranking") {
      await renderizarPaginaRanking();
    } else if (pagina === "summary") {
      if (obterUsuarioAtual()) {
        await renderizarPaginaResumo();
      } else {
        renderizarPaginaAcesso();
      }
    } else {
      await renderizarPaginaInicial();
    }
  } catch (erro) {
    elementoPrincipal.innerHTML = `
      <section class="section"><div class="container empty">
        ${escaparHtml(erro.message)}
      </div></section>`;
  }
}

async function tratarEnvioFormulario(evento) {
  const tratadores = [
    tratarEnvioDeAcesso,
    tratarEnvioDeSenha,
    tratarFiltrosTrilhas,
    tratarEnvioEvento,
    tratarPublicacaoAvaliacao,
    tratarRegistroHistorico,
    tratarAtualizacaoPerfil,
  ];
  for (const tratar of tratadores) {
    if (await tratar(evento)) {
      return;
    }
  }
}

async function tratarClique(evento) {
  const tratadores = [
    tratarCliqueDeSessao,
    tratarAcoesEvento,
    tratarAcoesDeTrilha,
    tratarAcoesAvaliacao,
    tratarRelatoProblema,
    tratarExportacaoDados,
  ];
  for (const tratar of tratadores) {
    if (await tratar(evento)) {
      return;
    }
  }
}

elementoPrincipal.addEventListener("submit", tratarEnvioFormulario);
elementoPrincipal.addEventListener("change", tratarMarcacaoChecklist);
document.addEventListener("click", tratarClique);
window.addEventListener("popstate", renderizarAplicacao);

renderizarAplicacao();
