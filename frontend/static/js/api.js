export const elementoPrincipal = document.querySelector("#app");
export const elementoNavegacao = document.querySelector("#navigation");
export const elementoAvisos = document.querySelector("#messages");

export function urlDaApi() {
  return (window.TRAILUP_API_URL || "http://localhost:5000/api").replace(/\/$/, "");
}

export function urlDoTermo() {
  return `${urlDaApi().replace(/\/api\/?$/, "")}/termo-consentimento`;
}

export async function requisicaoApi(caminho, opcoes = {}) {
  const resposta = await fetch(`${urlDaApi()}${caminho}`, {
    ...opcoes,
    credentials: "include",
    headers: { "Content-Type": "application/json", ...(opcoes.headers || {}) },
  });
  const dados = await resposta.json().catch(() => ({}));
  if (!resposta.ok) {
    throw new Error(dados.error || "Não foi possível concluir a solicitação");
  }
  return dados;
}

export function escaparHtml(valor = "") {
  const mapa = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  };
  return String(valor).replace(/[&<>"']/g, caractere => mapa[caractere]);
}

export function mostrarAviso(texto, tipo = "info") {
  elementoAvisos.innerHTML = `<div class="flash ${tipo}">${escaparHtml(texto)}</div>`;
  window.setTimeout(() => elementoAvisos.replaceChildren(), 4000);
}

export function carregarBibliotecaDoMapa() {
  if (window.maplibregl) {
    return Promise.resolve();
  }

  return new Promise((resolve, reject) => {
    const script = document.createElement("script");
    script.src = "https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js";
    script.onload = () => {
      if (window.maplibregl) {
        resolve();
      } else {
        reject(new Error("A biblioteca do mapa não inicializou."));
      }
    };
    script.onerror = () => {
      reject(new Error("Não foi possível carregar o mapa. Verifique sua conexão."));
    };
    document.head.append(script);
  });
}
