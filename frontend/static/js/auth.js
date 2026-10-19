import { escaparHtml, requisicaoApi, mostrarAviso, elementoPrincipal, urlDoTermo } from "./api.js";
import { definirUsuarioAtual } from "./state.js";

export function renderizarPaginaAcesso(cadastro = false) {
  const titulo = cadastro ? "Criar conta" : "Entrar";
  const campoNome = cadastro
    ? `<label>Nome<input name="nome" required maxlength="100"></label>`
    : "";
  const aceiteTermo = cadastro
    ? `<label class="consent-field">
         <input type="checkbox" name="aceitouTermo" required>
         <span>Confirmo que li o <a href="${urlDoTermo()}" target="_blank" rel="noopener">Termo de Consentimento TrailUp (PDF)</a>.</span>
       </label>`
    : "";
  const linkSenha = cadastro
    ? ""
    : `<a href="/?page=forgot-password">Esqueci minha senha</a>`;

  elementoPrincipal.innerHTML = `
    <section class="section">
      <div class="container">
        <form class="panel form-grid" id="auth-form">
          <h1>${titulo}</h1>
          ${campoNome}
          <label>E-mail<input type="email" name="email" required></label>
          <label>Senha<input type="password" name="senha" required minlength="6"></label>
          ${aceiteTermo}
          <button class="button primary">${titulo}</button>
          <a href="/?page=${cadastro ? "login" : "register"}">
            ${cadastro ? "Já tem conta? Entrar" : "Criar conta"}
          </a>
          ${linkSenha}
        </form>
      </div>
    </section>`;
}

export function renderizarPaginaRedefinicao() {
  const parametros = new URLSearchParams(location.search);
  const pagina = parametros.get("page");
  const recuperar = pagina === "forgot-password";

  if (recuperar) {
    elementoPrincipal.innerHTML = `
      <section class="section"><div class="container">
        <form id="forgot-form" class="panel form-grid">
          <h1>Recuperar senha</h1>
          <label>E-mail<input type="email" name="email" required></label>
          <button class="button primary">Enviar link de recuperação</button>
        </form>
      </div></section>`;
    return;
  }

  elementoPrincipal.innerHTML = `
    <section class="section"><div class="container">
      <form id="reset-form" class="panel form-grid">
        <h1>Definir nova senha</h1>
        <input type="hidden" name="token" value="${escaparHtml(parametros.get("token") || "")}">
        <label>Nova senha<input type="password" name="senha" minlength="6" required></label>
        <button class="button primary">Salvar nova senha</button>
      </form>
    </div></section>`;
}

export async function tratarEnvioDeAcesso(evento) {
  const formulario = evento.target;
  if (formulario.id !== "auth-form") {
    return false;
  }

  evento.preventDefault();
  const dados = Object.fromEntries(new FormData(formulario));
  const cadastro = new URLSearchParams(location.search).get("page") === "register";
  if (cadastro) {
    dados.aceitouTermo = formulario.elements.aceitouTermo.checked;
  }

  try {
    const resposta = await requisicaoApi(`/auth/${cadastro ? "register" : "login"}`, {
      method: "POST",
      body: JSON.stringify(dados),
    });
    definirUsuarioAtual(resposta.user);
    location.href = "/";
  } catch (erro) {
    mostrarAviso(erro.message, "danger");
  }
  return true;
}

export async function tratarEnvioDeSenha(evento) {
  const formulario = evento.target;
  if (formulario.id !== "forgot-form" && formulario.id !== "reset-form") {
    return false;
  }

  evento.preventDefault();
  const dados = Object.fromEntries(new FormData(formulario));
  const recuperacao = formulario.id === "forgot-form";
  const rota = recuperacao ? "/auth/password-reset" : "/auth/password-reset/confirm";

  try {
    const resposta = await requisicaoApi(rota, {
      method: "POST",
      body: JSON.stringify(dados),
    });
    mostrarAviso(
      recuperacao ? resposta.message : "Senha atualizada. Entre com a nova senha.",
      "success",
    );
    if (!recuperacao) {
      location.href = "/?page=login";
    }
  } catch (erro) {
    mostrarAviso(erro.message, "danger");
  }
  return true;
}

export async function tratarCliqueDeSessao(evento) {
  const botao = evento.target.closest('[data-action="logout"]');
  if (!botao) {
    return false;
  }
  evento.preventDefault();
  try {
    await requisicaoApi("/auth/logout", { method: "POST" });
    definirUsuarioAtual(null);
    location.href = "/";
  } catch (erro) {
    mostrarAviso(erro.message, "danger");
  }
  return true;
}
