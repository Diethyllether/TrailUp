import { escaparHtml, elementoPrincipal, requisicaoApi, mostrarAviso } from "./api.js";
import { obterUsuarioAtual } from "./state.js";

export async function renderizarPaginaEventos() {
  const dados = await requisicaoApi("/events");
  const usuario = obterUsuarioAtual();
  const formulario = usuario ? renderizarFormularioEvento(dados.trails) : "";
  const lista = dados.items.length
    ? dados.items.map(evento => renderizarEvento(evento, dados.participating, usuario)).join("")
    : `<div class="empty">Nenhuma expedição ativa disponível.</div>`;

  elementoPrincipal.innerHTML = `
    <section class="section"><div class="container">
      <h1>Expedições ativas</h1>
      ${formulario}
      <div class="event-list">${lista}</div>
    </div></section>`;
}

function renderizarFormularioEvento(trilhas) {
  const opcoes = trilhas.map(trilha =>
    `<option value="${trilha.idTrilha}">${escaparHtml(trilha.nome)}</option>`,
  ).join("");

  return `
    <form class="panel form-grid" id="event-form">
      <h2>Criar expedição</h2>
      <label>Título<input name="titulo" required></label>
      <label>Descrição<textarea name="descricao"></textarea></label>
      <label>Trilha<select name="idTrilha">${opcoes}</select></label>
      <label>Data<input name="data" type="date"></label>
      <label>Horário<input name="horario" type="time"></label>
      <label>Vagas<input name="vagas" type="number" min="1"></label>
      <label>Tipo<select name="tipo">
        <option value="GRUPO">Grupo</option>
        <option value="INDIVIDUAL">Individual</option>
      </select></label>
      <button class="button primary">Criar</button>
    </form>`;
}

function renderizarEvento(evento, participantesAtuais, usuario) {
  const participa = participantesAtuais.includes(evento.idEvento);
  const organizador = usuario?.idUsuario === evento.idCriador;
  const controles = usuario
    ? `<button class="button primary" data-action="${participa ? "leave" : "join"}"
         data-id="${evento.idEvento}">${participa ? "Sair" : "Participar"}</button>
       ${organizador ? `
         <button class="button ghost" data-action="edit-event" data-id="${evento.idEvento}">Editar</button>
         <button class="button danger" data-action="delete-event" data-id="${evento.idEvento}">Cancelar</button>` : ""}`
    : `<a class="button ghost" href="/?page=login">Entrar para participar</a>`;
  const comentarios = evento.comentarios || [];
  const nomes = evento.participantes || [];
  const formularioComentario = participa
    ? `<form class="form-grid event-comment-form" data-id="${evento.idEvento}">
         <textarea name="texto" required maxlength="2000"
           placeholder="Combine os detalhes da expedição"></textarea>
         <button class="button ghost">Comentar</button>
       </form>`
    : "";
  const relatar = usuario
    ? `<button class="button ghost" data-action="report" data-category="EVENTO"
         data-id="${evento.idEvento}">Reportar evento</button>`
    : "";

  return `
    <article class="panel event-card" data-event="${evento.idEvento}"
      data-event-date="${evento.data || ""}"
      data-event-time="${evento.horarioSaida ? evento.horarioSaida.slice(11, 16) : ""}"
      data-event-spots="${evento.vagas ?? ""}">
      <div class="event-row">
        <div>
          <strong>${escaparHtml(evento.titulo)}</strong>
          <p>${escaparHtml(evento.descricao || "")}</p>
          <p class="muted">
            ${escaparHtml(evento.data || "Data a definir")}
            ${evento.horarioSaida ? ` · ${escaparHtml(evento.horarioSaida.slice(11, 16))}` : ""}
            · ${escaparHtml(evento.tipo)} · ${evento.participantesAtuais} participante(s)
            · Organizador: ${escaparHtml(evento.nomeCriador || "")}
          </p>
        </div>
        <div>${controles}</div>
      </div>
      <details>
        <summary>Participantes confirmados (${nomes.length})</summary>
        <p>${nomes.map(escaparHtml).join(", ") || "Nenhum participante"}</p>
      </details>
      <details>
        <summary>Comentários (${comentarios.length})</summary>
        <div class="review-list">
          ${comentarios.map(comentario => `
            <p><strong>${escaparHtml(comentario.nomeUsuario)}:</strong>
              ${escaparHtml(comentario.texto)}</p>`).join("")}
        </div>
        ${formularioComentario}
      </details>
      ${relatar}
    </article>`;
}

export async function tratarEnvioEvento(evento) {
  const formulario = evento.target;
  if (formulario.id !== "event-form" && !formulario.matches(".event-comment-form")) {
    return false;
  }

  evento.preventDefault();
  const dados = Object.fromEntries(new FormData(formulario));
  const criar = formulario.id === "event-form";
  const caminho = criar ? "/events" : `/events/${formulario.dataset.id}/comments`;

  try {
    await requisicaoApi(caminho, {
      method: "POST",
      body: JSON.stringify(dados),
    });
    mostrarAviso(criar ? "Expedição criada." : "Comentário publicado.", "success");
    window.location.reload();
  } catch (erro) {
    mostrarAviso(erro.message, "danger");
  }
  return true;
}

export async function tratarAcoesEvento(evento) {
  const botao = evento.target.closest(
    '[data-action="join"], [data-action="leave"], [data-action="delete-event"], [data-action="edit-event"]',
  );
  if (!botao) {
    return false;
  }

  const idEvento = botao.dataset.id;
  try {
    if (botao.dataset.action === "join") {
      await requisicaoApi(`/events/${idEvento}/participation`, { method: "POST" });
    } else if (botao.dataset.action === "leave") {
      await requisicaoApi(`/events/${idEvento}/participation`, { method: "DELETE" });
    } else if (botao.dataset.action === "delete-event") {
      if (!window.confirm("Cancelar e excluir esta expedição?")) {
        return true;
      }
      await requisicaoApi(`/events/${idEvento}`, { method: "DELETE" });
    } else {
      const cartao = botao.closest(".event-card");
      const titulo = window.prompt("Título da expedição:", cartao.querySelector("strong").textContent);
      if (titulo === null) return true;
      const descricao = window.prompt(
        "Descrição:",
        cartao.querySelector(".event-row p")?.textContent || "",
      );
      if (descricao === null) return true;
      const data = window.prompt("Data (AAAA-MM-DD; vazio remove):", cartao.dataset.eventDate);
      if (data === null) return true;
      const horario = window.prompt("Horário (HH:MM; vazio remove):", cartao.dataset.eventTime);
      if (horario === null) return true;
      const vagas = window.prompt("Número de vagas (vazio sem limite):", cartao.dataset.eventSpots);
      if (vagas === null) return true;
      await requisicaoApi(`/events/${idEvento}`, {
        method: "PUT",
        body: JSON.stringify({ titulo, descricao, data, horario, vagas }),
      });
    }
    window.location.reload();
  } catch (erro) {
    mostrarAviso(erro.message, "danger");
  }
  return true;
}
