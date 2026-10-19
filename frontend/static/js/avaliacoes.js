import { escaparHtml, requisicaoApi, mostrarAviso } from "./api.js";
import { obterUsuarioAtual } from "./state.js";

export function renderizarAvaliacoes(avaliacoes, media, idTrilha) {
  const usuario = obterUsuarioAtual();
  const lista = avaliacoes.length
    ? `<div class="review-list">
         ${avaliacoes.map(avaliacao => renderizarAvaliacao(avaliacao, usuario)).join("")}
       </div>`
    : `<div class="empty review-empty">
         Ainda não há comentários. Seja a primeira pessoa a avaliar esta trilha.
       </div>`;
  const formulario = usuario
    ? `<form id="review-form" data-id="${idTrilha}" class="panel review-form">
         <h3>Conte como foi sua experiência</h3>
         <label>Nota
           <select name="nota">
             <option value="5">5 — Excelente</option>
             <option value="4">4 — Muito boa</option>
             <option value="3">3 — Boa</option>
             <option value="2">2 — Regular</option>
             <option value="1">1 — Difícil</option>
           </select>
         </label>
         <label>Comentário
           <textarea name="comentario" maxlength="2000" rows="4"
             placeholder="Como foi o percurso? Tem alguma dica para a próxima pessoa?"></textarea>
         </label>
         <button class="button primary">Publicar avaliação</button>
       </form>`
    : `<p class="review-signin"><a href="/?page=login">Entre na sua conta</a> para avaliar.</p>`;

  return `
    <section class="trail-section reviews-section">
      <div class="section-header">
        <div><span class="eyebrow">COMUNIDADE</span><h2>Comentários e avaliações</h2></div>
        <span class="rating-summary">
          ${media != null ? `★ ${Number(media).toFixed(1)} / 5` : "Ainda sem notas"}
        </span>
      </div>
      ${lista}
      ${formulario}
    </section>`;
}

function renderizarAvaliacao(avaliacao, usuario) {
  const acoes = usuario?.idUsuario === avaliacao.idUsuario
    ? `<button class="button ghost" data-action="edit-review"
         data-id="${avaliacao.idAvaliacao}" data-note="${avaliacao.nota}"
         data-comment="${escaparHtml(avaliacao.comentario || "")}">Editar</button>
       <button class="button danger" data-action="delete-review"
         data-id="${avaliacao.idAvaliacao}">Excluir</button>`
    : "";

  return `
    <article class="review-card">
      <div class="review-card-heading">
        <strong>${escaparHtml(avaliacao.nomeUsuario || "Pessoa trilheira")}</strong>
        <span class="review-rating">★ ${Number(avaliacao.nota)}/5</span>
      </div>
      <p>${avaliacao.comentario
        ? escaparHtml(avaliacao.comentario)
        : `<span class="muted">Sem comentário escrito.</span>`}</p>
      ${acoes}
    </article>`;
}

export async function tratarPublicacaoAvaliacao(evento) {
  const formulario = evento.target;
  if (formulario.id !== "review-form") {
    return false;
  }

  evento.preventDefault();
  const dados = Object.fromEntries(new FormData(formulario));
  try {
    await requisicaoApi(`/trails/${formulario.dataset.id}/reviews`, {
      method: "POST",
      body: JSON.stringify(dados),
    });
    mostrarAviso("Avaliação publicada.", "success");
    window.location.reload();
  } catch (erro) {
    mostrarAviso(erro.message, "danger");
  }
  return true;
}

export async function tratarAcoesAvaliacao(evento) {
  const botao = evento.target.closest('[data-action="delete-review"], [data-action="edit-review"]');
  if (!botao) {
    return false;
  }

  const id = botao.dataset.id;
  try {
    if (botao.dataset.action === "delete-review") {
      if (!window.confirm("Excluir sua avaliação?")) {
        return true;
      }
      await requisicaoApi(`/reviews/${id}`, { method: "DELETE" });
    } else {
      const comentario = window.prompt("Edite seu comentário:", botao.dataset.comment || "");
      if (comentario === null) {
        return true;
      }
      const nota = window.prompt("Nota de 1 a 5:", botao.dataset.note);
      if (nota === null) {
        return true;
      }
      await requisicaoApi(`/reviews/${id}`, {
        method: "PUT",
        body: JSON.stringify({ nota, comentario }),
      });
    }
    window.location.reload();
  } catch (erro) {
    mostrarAviso(erro.message, "danger");
  }
  return true;
}
