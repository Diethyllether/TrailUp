import { escaparHtml, requisicaoApi, mostrarAviso } from "./api.js";

export function renderizarFormularioConclusao(idTrilha) {
  return `
    <section class="trail-section">
      <h2>Concluir trilha</h2>
      <form class="panel form-grid" id="history-form" data-trail="${idTrilha}">
        <label>Data<input type="date" name="dataRealizacao"
          value="${new Date().toISOString().slice(0, 10)}" required></label>
        <label>Tempo realizado (minutos)
          <input type="number" name="tempo" min="0" step="1">
        </label>
        <label>Avaliação pessoal
          <select name="avaliacaoPessoal">
            <option value="">Sem nota</option>
            ${[5, 4, 3, 2, 1].map(nota => `<option value="${nota}">${nota} / 5</option>`).join("")}
          </select>
        </label>
        <button class="button primary">Registrar conclusão</button>
      </form>
    </section>`;
}

export function renderizarListaHistorico(itens) {
  if (!itens.length) {
    return `<p class="muted">Você ainda não registrou trilhas.</p>`;
  }

  return itens.map(item => `
    <article class="panel">
      <strong>${escaparHtml(item.nomeTrilha)}</strong>
      <p>${escaparHtml(item.dataRealizacao || "")} · ${item.tempo ?? "—"} min
        · Avaliação pessoal: ${item.avaliacaoPessoal ?? "—"}</p>
    </article>`).join("");
}

export async function tratarRegistroHistorico(evento) {
  const formulario = evento.target;
  if (formulario.id !== "history-form") {
    return false;
  }

  evento.preventDefault();
  const dados = Object.fromEntries(new FormData(formulario));
  dados.idTrilha = Number(formulario.dataset.trail);
  dados.tempo = dados.tempo ? Number(dados.tempo) : null;
  dados.avaliacaoPessoal = dados.avaliacaoPessoal
    ? Number(dados.avaliacaoPessoal)
    : null;

  try {
    await requisicaoApi("/history", {
      method: "POST",
      body: JSON.stringify(dados),
    });
    mostrarAviso("Trilha registrada no histórico.", "success");
    window.location.reload();
  } catch (erro) {
    mostrarAviso(erro.message, "danger");
  }
  return true;
}
