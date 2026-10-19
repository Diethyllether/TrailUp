import { elementoPrincipal, requisicaoApi } from "./api.js";
import { renderizarCardTrilha } from "./trilhas.js";

export async function renderizarPaginaFavoritos() {
  const dados = await requisicaoApi("/favorites");
  const conteudo = dados.items.length
    ? `<div class="cards">${dados.items.map(trilha => renderizarCardTrilha({
        ...trilha,
        favorito: true,
        media: trilha.media || [trilha.mediaNota, trilha.quantidadeAvaliacoes],
      })).join("")}</div>`
    : `<div class="empty">Você ainda não salvou trilhas.</div>`;

  elementoPrincipal.innerHTML = `
    <section class="section"><div class="container">
      <h1>Favoritos</h1>
      ${conteudo}
    </div></section>`;
}
