import {
  escaparHtml,
  requisicaoApi,
  elementoPrincipal,
  carregarBibliotecaDoMapa,
  mostrarAviso,
} from "./api.js";
import { obterUsuarioAtual } from "./state.js";
import { renderizarItensChecklist } from "./checklist.js";
import { renderizarAvaliacoes } from "./avaliacoes.js";
import { renderizarFormularioConclusao } from "./historico.js";

export async function renderizarPaginaInicial() {
  const parametros = new URLSearchParams(location.search);
  const filtros = {
    q: parametros.get("q") || "",
    difficulty: parametros.get("difficulty") || "",
    sort: parametros.get("sort") || "",
    maxDistance: parametros.get("maxDistance") || "",
    maxDuration: parametros.get("maxDuration") || "",
    minRating: parametros.get("minRating") || "",
    lat: parametros.get("lat") || "",
    lon: parametros.get("lon") || "",
  };
  const query = new URLSearchParams(
    Object.fromEntries(Object.entries(filtros).filter(([, valor]) => valor)),
  );
  const dados = await requisicaoApi(`/trails?${query}`);
  const seletorDificuldade = ["FACIL", "MODERADA", "DIFICIL"]
    .map(valor => `<option value="${valor}" ${filtros.difficulty === valor ? "selected" : ""}>${valor}</option>`)
    .join("");
  const lista = dados.items.length
    ? `<div class="cards">
         ${dados.items.map(trilha => {
           const localizacao = trilha.distanciaProxima != null
             ? `${trilha.localizacao || ""} · ${trilha.distanciaProxima} km daqui`
             : trilha.localizacao;
           return renderizarCardTrilha({ ...trilha, localizacao });
         }).join("")}
       </div>`
    : `<div class="empty">Nenhuma trilha encontrada.</div>`;

  elementoPrincipal.innerHTML = `
    <section class="hero"><div class="container">
      <h1>Encontre sua próxima trilha.</h1>
      <p class="lead">Descubra rotas, acompanhe expedições e salve suas trilhas favoritas.</p>
      <form class="searchbar" id="search">
        <input name="q" value="${escaparHtml(filtros.q)}" placeholder="Buscar trilha ou região...">
        <select name="difficulty">
          <option value="">Todas as dificuldades</option>${seletorDificuldade}
        </select>
        <button class="button primary">Buscar</button>
      </form>
      <form class="panel form-grid" id="trail-filters" style="margin-top:14px">
        <input type="hidden" name="q" value="${escaparHtml(filtros.q)}">
        <input type="hidden" name="difficulty" value="${escaparHtml(filtros.difficulty)}">
        <input type="hidden" name="lat" value="${escaparHtml(filtros.lat)}">
        <input type="hidden" name="lon" value="${escaparHtml(filtros.lon)}">
        <label>Ordenar por
          <select name="sort">
            <option value="">Padrão</option>
            <option value="distancia" ${filtros.sort === "distancia" ? "selected" : ""}>Menor distância</option>
            <option value="duracao" ${filtros.sort === "duracao" ? "selected" : ""}>Menor duração</option>
            <option value="nota" ${filtros.sort === "nota" ? "selected" : ""}>Maior nota</option>
          </select>
        </label>
        <label>Distância máxima (km)
          <input name="maxDistance" type="number" min="0" step="0.1" value="${filtros.maxDistance}">
        </label>
        <label>Duração máxima (min)
          <input name="maxDuration" type="number" min="0" value="${filtros.maxDuration}">
        </label>
        <label>Nota mínima
          <input name="minRating" type="number" min="1" max="5" step="0.1" value="${filtros.minRating}">
        </label>
        <button class="button ghost">Aplicar filtros</button>
        <button type="button" class="button ghost" data-action="nearby">Trilhas próximas</button>
      </form>
      ${obterUsuarioAtual()
        ? `<button class="button ghost report-home" data-action="report" data-category="BUG">Reportar bug ou sugestão</button>`
        : ""}
    </div></section>
    <section class="section"><div class="container">
      <div class="section-header">
        <h2>${filtros.q || filtros.difficulty ? "Resultados da busca" : "Trilhas em destaque"}</h2>
        <span class="muted">${dados.items.length} encontrada(s)</span>
      </div>
      ${lista}
    </div></section>`;
}

export function renderizarCardTrilha(trilha) {
  const usuario = obterUsuarioAtual();
  const imagem = trilha.imagemUrl
    ? `<img src="${escaparHtml(trilha.imagemUrl)}" alt="${escaparHtml(trilha.nome)}">`
    : "";
  const avaliacao = trilha.media?.[0] != null
    ? `<span class="badge">★ ${Number(trilha.media[0]).toFixed(1)}</span>`
    : "";
  const botaoFavorito = usuario
    ? `<div class="card-body card-actions">
         <button class="button ghost" data-action="favorite" data-id="${trilha.idTrilha}"
           data-fav="${Boolean(trilha.favorito)}">
           ${trilha.favorito ? "★ Remover dos favoritos" : "☆ Favoritar"}
         </button>
       </div>`
    : "";

  return `
    <article class="card">
      <a href="/?page=trail&id=${trilha.idTrilha}">
        <div class="card-media">${imagem}</div>
        <div class="card-body">
          <div class="card-title">${escaparHtml(trilha.nome)}</div>
          <div class="meta">
            ${escaparHtml(trilha.localizacao || "")}
            ${trilha.distancia != null ? ` · ${Number(trilha.distancia).toFixed(1)} km` : ""}
          </div>
          <div class="meta card-badges">
            <span class="badge">${escaparHtml(trilha.dificuldade || "Sem dificuldade")}</span>
            <span class="badge">${trilha.tempoEstimadoMin
              ? `~ ${Math.round(trilha.tempoEstimadoMin)} min`
              : "Tempo variável"}</span>
            ${avaliacao}
          </div>
        </div>
      </a>
      ${botaoFavorito}
    </article>`;
}

export async function renderizarPaginaTrilha(idTrilha) {
  const usuario = obterUsuarioAtual();
  const [dados, checklist] = await Promise.all([
    requisicaoApi(`/trails/${idTrilha}`),
    usuario
      ? requisicaoApi(`/trails/${idTrilha}/checklist-state`)
      : Promise.resolve({ itens: {} }),
  ]);
  const trilha = dados.trail;
  const pontos = Array.isArray(dados.checkpoints) ? dados.checkpoints : [];
  const avaliacoes = Array.isArray(dados.reviews) ? dados.reviews : [];
  const botaoFavorito = usuario
    ? `<button class="button ghost" data-action="favorite" data-id="${idTrilha}"
         data-fav="${dados.favorite}">
         ${dados.favorite ? "★ Remover dos favoritos" : "☆ Salvar nos favoritos"}
       </button>`
    : "";
  const descricao = trilha.descricao
    ? `<section class="trail-description"><h2>Sobre esta trilha</h2><p>${escaparHtml(trilha.descricao)}</p></section>`
    : "";
  const secaoConclusao = usuario
    ? `${renderizarFormularioConclusao(idTrilha)}
       <button class="button ghost" data-action="report" data-category="TRILHA" data-id="${idTrilha}">
         Reportar problema nesta trilha
       </button>`
    : "";

  elementoPrincipal.innerHTML = `
    <section class="section trail-page"><div class="container">
      <a class="back-link" href="/">← Voltar às trilhas</a>
      <header class="trail-heading">
        <div>
          <span class="eyebrow">TRILHA</span>
          <h1>${escaparHtml(trilha.nome)}</h1>
          <div class="trail-tags">
            <span>${escaparHtml(trilha.localizacao || "Local não informado")}</span>
            <span>${escaparHtml(trilha.dificuldade || "Dificuldade não informada")}</span>
            ${trilha.distancia != null ? `<span>${Number(trilha.distancia).toFixed(1)} km</span>` : ""}
            ${trilha.duracao != null ? `<span>${Math.round(Number(trilha.duracao))} min</span>` : ""}
          </div>
        </div>
        ${botaoFavorito}
      </header>
      ${descricao}
      <section class="trail-section">
        <div class="section-header">
          <div><span class="eyebrow">PERCURSO</span><h2>Mapa e checkpoints</h2></div>
          <span class="muted">${pontos.length} ponto(s)</span>
        </div>
        ${renderizarPontosTrilha(pontos)}
      </section>
      <section class="trail-section">
        <h2>Checklist de equipamentos</h2>
        <div class="panel form-grid">
          ${renderizarItensChecklist(dados.checklist || [], checklist.itens || {})}
          <p class="muted">${usuario ? "Marcações salvas na sua conta." : "Entre para salvar as marcações."}</p>
        </div>
      </section>
      ${renderizarAvaliacoes(avaliacoes, dados.average, idTrilha)}
      ${secaoConclusao}
    </div></section>`;

  if (pontos.length) {
    iniciarMapaTrilha(pontos);
  }
}

function renderizarPontosTrilha(pontos) {
  if (!pontos.length) {
    return `<div class="map-placeholder">Esta trilha ainda não tem checkpoints cadastrados.</div>`;
  }

  const itens = pontos.map((ponto, indice) => {
    const nome = indice === 0
      ? "Início"
      : indice === pontos.length - 1
        ? "Fim"
        : `Checkpoint ${indice + 1}`;
    return `<li><span class="checkpoint-number">${indice + 1}</span>
      <span><strong>${nome}</strong>
      <small>${Number(ponto.latitude).toFixed(5)}, ${Number(ponto.longitude).toFixed(5)}</small></span></li>`;
  }).join("");

  return `
    <div id="trail-map" class="map" aria-label="Mapa do percurso com checkpoints conectados">
      <div class="map-message" id="trail-map-message">Carregando mapa…</div>
    </div>
    <ol class="checkpoint-list">${itens}</ol>`;
}

function iniciarMapaTrilha(pontos) {
  const iniciar = () => {
    const script = document.createElement("script");
    script.src = "static/js/trail-detail.js";
    script.dataset.checkpoints = JSON.stringify(pontos);
    document.body.append(script);
    script.onerror = () => {
      const status = document.getElementById("trail-map-message");
      if (status) {
        status.textContent = "Não foi possível iniciar o mapa. Os checkpoints continuam listados abaixo.";
      }
    };
  };

  if (window.maplibregl) {
    iniciar();
    return;
  }
  carregarBibliotecaDoMapa().then(iniciar).catch(erro => {
    const status = document.getElementById("trail-map-message");
    if (status) {
      status.textContent = `${erro.message} Os checkpoints continuam listados abaixo.`;
    }
  });
}

export async function tratarFiltrosTrilhas(evento) {
  const formulario = evento.target;
  if (formulario.id !== "search" && formulario.id !== "trail-filters") {
    return false;
  }
  evento.preventDefault();
  const parametros = new URLSearchParams(
    Object.fromEntries([...new FormData(formulario)].filter(([, valor]) => valor)),
  );
  location.href = `/?${parametros}`;
  return true;
}

export async function tratarAcoesDeTrilha(evento) {
  const botao = evento.target.closest('[data-action="favorite"], [data-action="nearby"]');
  if (!botao) {
    return false;
  }

  if (botao.dataset.action === "nearby") {
    if (!navigator.geolocation) {
      mostrarAviso("Este navegador não oferece geolocalização.", "danger");
      return true;
    }
    navigator.geolocation.getCurrentPosition(
      posicao => {
        const parametros = new URLSearchParams(location.search);
        parametros.set("lat", posicao.coords.latitude);
        parametros.set("lon", posicao.coords.longitude);
        location.href = `/?${parametros}`;
      },
      () => mostrarAviso("Não foi possível obter a localização.", "danger"),
    );
    return true;
  }

  try {
    const remover = botao.dataset.fav === "true";
    await requisicaoApi(`/trails/${botao.dataset.id}/favorite`, {
      method: remover ? "DELETE" : "POST",
    });
    location.reload();
  } catch (erro) {
    mostrarAviso(erro.message, "danger");
  }
  return true;
}
