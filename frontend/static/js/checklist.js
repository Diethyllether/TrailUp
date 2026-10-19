import { escaparHtml, requisicaoApi, mostrarAviso } from "./api.js";
import { obterUsuarioAtual } from "./state.js";

export function renderizarItensChecklist(itens, marcados) {
  if (!itens.length) {
    return `<p class="muted">Nenhum equipamento cadastrado para esta trilha.</p>`;
  }

  const usuario = obterUsuarioAtual();
  return itens.map(item => `
    <label class="checklist-item">
      <input type="checkbox" data-checklist="${item.idChecklistItem}"
        ${usuario ? "" : "disabled"}
        ${marcados[item.idChecklistItem] ? "checked" : ""}>
      <span>${escaparHtml(item.descricao)} ${item.obrigatorio ? "(obrigatório)" : ""}</span>
    </label>`).join("");
}

export async function tratarMarcacaoChecklist(evento) {
  const caixa = evento.target.closest("[data-checklist]");
  if (!caixa) {
    return false;
  }

  if (!obterUsuarioAtual()) {
    caixa.checked = !caixa.checked;
    mostrarAviso("Entre para salvar as marcações.", "info");
    return true;
  }

  try {
    await requisicaoApi(`/checklist/${caixa.dataset.checklist}`, {
      method: "PATCH",
      body: JSON.stringify({ marcado: caixa.checked }),
    });
  } catch (erro) {
    caixa.checked = !caixa.checked;
    mostrarAviso(erro.message, "danger");
  }
  return true;
}
