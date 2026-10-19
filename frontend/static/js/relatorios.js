import { escaparHtml, elementoPrincipal, requisicaoApi, mostrarAviso } from "./api.js";

export async function renderizarPaginaRanking() {
  const resposta = await requisicaoApi("/reports/ranking?limite=20");
  const linhas = resposta.items.length
    ? resposta.items.map((item, indice) => `
        <tr>
          <td>${indice + 1}</td>
          <td>${escaparHtml(item.nome)}</td>
          <td>${item.trilhasConcluidas}</td>
          <td>${Number(item.distanciaTotalKm || 0).toFixed(1)} km</td>
          <td>${item.avaliacoesRealizadas}</td>
        </tr>`).join("")
    : `<tr><td colspan="5">Ainda não há atividade para exibir.</td></tr>`;

  elementoPrincipal.innerHTML = `
    <section class="section"><div class="container">
      <h1>Ranking de trilheiros</h1>
      <p class="lead">Trilhas concluídas, distância percorrida e avaliações da comunidade.</p>
      <div class="panel"><table>
        <thead><tr><th>Posição</th><th>Trilheiro</th><th>Trilhas</th><th>Distância</th><th>Avaliações</th></tr></thead>
        <tbody>${linhas}</tbody>
      </table></div>
    </div></section>`;
}

export async function renderizarPaginaResumo() {
  const resposta = await requisicaoApi("/reports/summary");
  const item = resposta.item;
  const cartoes = [
    ["Trilhas concluídas", item.trilhasRealizadas],
    ["Distância", `${Number(item.distanciaTotalKm || 0).toFixed(1)} km`],
    ["Tempo em trilhas", `${Number(item.tempoTotalMin || 0).toFixed(0)} min`],
    ["Favoritos", item.totalFavoritos],
    ["Avaliações", item.totalAvaliacoes],
    ["Eventos", item.eventosParticipados],
  ];

  elementoPrincipal.innerHTML = `
    <section class="section"><div class="container">
      <h1>Resumo da sua atividade</h1>
      <div class="grid cards">
        ${cartoes.map(([rotulo, valor]) => `
          <article class="panel"><p class="muted">${rotulo}</p>
            <strong>${escaparHtml(valor ?? 0)}</strong></article>`).join("")}
      </div>
    </div></section>`;
}

export async function tratarRelatoProblema(evento) {
  const botao = evento.target.closest('[data-action="report"]');
  if (!botao) {
    return false;
  }

  const descricao = window.prompt("Descreva o problema:");
  if (!descricao) {
    return true;
  }
  const categoria = botao.dataset.category;
  const dados = {
    categoria,
    idTrilha: categoria === "TRILHA" ? Number(botao.dataset.id) : undefined,
    idEvento: categoria === "EVENTO" ? Number(botao.dataset.id) : undefined,
    descricao,
  };
  try {
    await requisicaoApi("/reports", {
      method: "POST",
      body: JSON.stringify(dados),
    });
    mostrarAviso("Relato enviado. Obrigado.", "success");
  } catch (erro) {
    mostrarAviso(erro.message, "danger");
  }
  return true;
}
