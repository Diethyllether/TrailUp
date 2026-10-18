const app = document.querySelector('#app');
const nav = document.querySelector('#navigation');
const messages = document.querySelector('#messages');
const API_BASE = (window.TRAILUP_API_URL || 'http://localhost:5000/api').replace(/\/$/, '');
let user = null;

const escapeHtml = (value = '') => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const checklistStorageKey = trailId => `trailup:checklist:${trailId}`;
function readChecklistState(trailId) {
  try { return JSON.parse(localStorage.getItem(checklistStorageKey(trailId)) || '{}'); }
  catch { return {}; }
}
const api = async (path, options = {}) => {
  const response = await fetch(`${API_BASE}${path}`, { credentials: 'include', headers: {'Content-Type':'application/json', ...(options.headers || {})}, ...options });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.error || 'Não foi possível concluir a solicitação');
  return data;
};
function loadMapLibrary() {
  if (window.maplibregl) return Promise.resolve();
  return new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = 'https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js';
    script.onload = () => window.maplibregl ? resolve() : reject(new Error('A biblioteca do mapa não inicializou.'));
    script.onerror = () => reject(new Error('Não foi possível carregar a biblioteca do mapa. Verifique sua conexão.'));
    document.head.append(script);
  });
}
function notice(text, kind='info') { messages.innerHTML = `<div class="flash ${kind}">${escapeHtml(text)}</div>`; setTimeout(() => messages.replaceChildren(), 4000); }
function navRender() { nav.innerHTML = `<a href="/">Home</a><a href="/?page=events">Expedições</a>${user ? '<a href="/?page=favorites">Favoritos</a><a href="/?page=profile">Perfil</a><button class="link-button" data-action="logout">Sair</button>' : '<a href="/?page=login">Entrar</a><a class="nav-cta" href="/?page=register">Criar conta</a>'}`; }
const card = t => `<article class="card"><a href="/?page=trail&id=${t.idTrilha}"><div class="card-media">${t.imagemUrl ? `<img src="${escapeHtml(t.imagemUrl)}" alt="${escapeHtml(t.nome)}">` : ''}</div><div class="card-body"><div class="card-title">${escapeHtml(t.nome)}</div><div class="meta">${escapeHtml(t.localizacao || '')}${t.distancia != null ? ` · ${Number(t.distancia).toFixed(1)} km` : ''}</div><div class="meta" style="margin-top:10px"><span class="badge">${escapeHtml(t.dificuldade || 'Sem dificuldade')}</span><span class="badge">${t.tempoEstimadoMin ? `~ ${Math.round(t.tempoEstimadoMin)} min` : 'Tempo variável'}</span>${t.media?.[0] != null ? `<span class="badge">★ ${Number(t.media[0]).toFixed(1)}</span>` : ''}</div></div></a>${user ? `<div class="card-body" style="padding-top:0"><button class="button ghost" data-action="favorite" data-id="${t.idTrilha}" data-fav="${t.favorito}">${t.favorito ? '★ Remover dos favoritos' : '☆ Favoritar'}</button></div>` : ''}</article>`;
async function home() {
  const params = new URLSearchParams(location.search); const q = params.get('q') || ''; const difficulty = params.get('difficulty') || '';
  const filters = {q, difficulty, sort:params.get('sort')||'', maxDistance:params.get('maxDistance')||'', maxDuration:params.get('maxDuration')||'', minRating:params.get('minRating')||'', lat:params.get('lat')||'', lon:params.get('lon')||''};
  const data = await api(`/trails?${new URLSearchParams(Object.fromEntries(Object.entries(filters).filter(([,v])=>v)))}`);
  app.innerHTML = `<section class="hero"><div class="container"><h1>Encontre sua próxima trilha.</h1><p class="lead">Descubra rotas, acompanhe expedições e salve suas trilhas favoritas.</p><form class="searchbar" id="search"><input name="q" value="${escapeHtml(q)}" placeholder="Buscar trilha ou região..."><select name="difficulty"><option value="">Todas as dificuldades</option>${['FACIL','MODERADA','DIFICIL'].map(x=>`<option value="${x}" ${difficulty===x?'selected':''}>${x}</option>`).join('')}</select><button class="button primary">Buscar</button></form><form class="panel form-grid" id="trail-filters" style="margin-top:14px"><input type="hidden" name="q" value="${escapeHtml(q)}"><input type="hidden" name="difficulty" value="${escapeHtml(difficulty)}"><input type="hidden" name="lat" value="${filters.lat}"><input type="hidden" name="lon" value="${filters.lon}"><label>Ordenar por<select name="sort"><option value="">Padrão</option><option value="distancia" ${filters.sort==='distancia'?'selected':''}>Menor distância</option><option value="duracao" ${filters.sort==='duracao'?'selected':''}>Menor duração</option><option value="nota" ${filters.sort==='nota'?'selected':''}>Maior nota</option></select></label><label>Distância máxima (km)<input name="maxDistance" type="number" min="0" step="0.1" value="${filters.maxDistance}"></label><label>Duração máxima (min)<input name="maxDuration" type="number" min="0" value="${filters.maxDuration}"></label><label>Nota mínima<input name="minRating" type="number" min="1" max="5" step="0.1" value="${filters.minRating}"></label><button class="button ghost">Aplicar filtros</button><button type="button" class="button ghost" data-action="nearby">Trilhas próximas</button></form>${user?'<button class="button ghost" style="margin-top:12px" data-action="report" data-category="BUG">Reportar bug ou sugestão</button>':''}</div></section><section class="section"><div class="container"><div class="section-header"><h2>${q||difficulty?'Resultados da busca':'Trilhas em destaque'}</h2><span class="muted">${data.items.length} encontrada(s)</span></div>${data.items.length ? `<div class="cards">${data.items.map(t=>card({...t,localizacao:t.distanciaProxima!=null?`${t.localizacao||''} · ${t.distanciaProxima} km de você`:t.localizacao})).join('')}</div>` : '<div class="empty">Nenhuma trilha encontrada. Para buscar por proximidade, permita o acesso à localização.</div>'}</div></section>`;
}
function authPage(register=false) { const consentUrl=`${API_BASE.replace(/\/api\/?$/,'')}/termo-consentimento`; app.innerHTML = `<section class="section"><div class="container"><form class="panel form-grid" id="auth-form"><h1>${register?'Criar conta':'Entrar'}</h1>${register?'<label>Nome<input name="nome" required maxlength="100"></label>':''}<label>E-mail<input type="email" name="email" required></label><label>Senha<input type="password" name="senha" required minlength="6"></label>${register?`<label style="display:flex;align-items:flex-start;gap:10px"><input style="width:auto;margin-top:3px" type="checkbox" name="aceitouTermo" required><span>Confirmo que li o <a href="${consentUrl}" target="_blank" rel="noopener">Termo de Consentimento TrailUp (PDF)</a>.</span></label>`:''}<button class="button primary">${register?'Criar conta':'Entrar'}</button><a href="/?page=${register?'login':'register'}">${register?'Já tem conta? Entrar':'Criar conta'}</a>${!register?'<a href="/?page=forgot-password">Esqueci minha senha</a>':''}</form></div></section>`; }
async function trailPage(id) {
  const d=await api(`/trails/${id}`), t=d.trail;
  const points = Array.isArray(d.checkpoints) ? d.checkpoints : [];
  const reviews = Array.isArray(d.reviews) ? d.reviews : [];
  const checklistState = readChecklistState(id);
  app.innerHTML = `<section class="section trail-page"><div class="container">
    <a class="back-link" href="/">← Voltar às trilhas</a>
    <header class="trail-heading"><div><span class="eyebrow">TRILHA</span><h1>${escapeHtml(t.nome)}</h1>
      <div class="trail-tags"><span>${escapeHtml(t.localizacao || 'Local não informado')}</span><span>${escapeHtml(t.dificuldade || 'Dificuldade não informada')}</span>${t.distancia != null ? `<span>${Number(t.distancia).toFixed(1)} km</span>` : ''}${t.duracao != null ? `<span>${Math.round(Number(t.duracao))} min</span>` : ''}</div>
    </div>${user ? `<button class="button ghost" data-action="favorite" data-id="${id}" data-fav="${d.favorite}">${d.favorite ? '★ Remover dos favoritos' : '☆ Salvar nos favoritos'}</button>` : ''}</header>
    ${t.descricao ? `<section class="trail-description"><h2>Sobre esta trilha</h2><p>${escapeHtml(t.descricao)}</p></section>` : ''}
    <section class="trail-section"><div class="section-header"><div><span class="eyebrow">PERCURSO</span><h2>Mapa e checkpoints</h2></div><span class="muted">${points.length} ponto(s)</span></div>
      ${points.length ? `<div id="trail-map" class="map" aria-label="Mapa do percurso com checkpoints conectados"><div class="map-message" id="trail-map-message">Carregando mapa…</div></div><ol class="checkpoint-list">${points.map((point, index) => `<li><span class="checkpoint-number">${index + 1}</span><span><strong>${index === 0 ? 'Início' : index === points.length - 1 ? 'Fim' : `Checkpoint ${index + 1}`}</strong><small>${Number(point.latitude).toFixed(5)}, ${Number(point.longitude).toFixed(5)}</small></span></li>`).join('')}</ol>` : '<div class="map-placeholder">Esta trilha ainda não tem checkpoints cadastrados.</div>'}
    </section>
    <section class="trail-section"><h2>Checklist de equipamentos</h2><div class="panel form-grid">${(d.checklist||[]).length ? d.checklist.map(item=>`<label style="display:flex;align-items:center;gap:10px"><input style="width:auto" type="checkbox" data-checklist="${item.idChecklistItem}" ${checklistState[item.idChecklistItem]?'checked':''}> ${escapeHtml(item.descricao)} ${item.obrigatorio?'(obrigatório)':''}</label>`).join('') : '<p class="muted">Nenhum equipamento cadastrado para esta trilha.</p>'}<p class="muted">As marcações ficam salvas neste navegador.</p></div></section>
    <section class="trail-section reviews-section"><div class="section-header"><div><span class="eyebrow">COMUNIDADE</span><h2>Comentários e avaliações</h2></div><span class="rating-summary">${d.average != null ? `★ ${Number(d.average).toFixed(1)} / 5` : 'Ainda sem notas'}</span></div>
      ${reviews.length ? `<div class="review-list">${reviews.map(review => `<article class="review-card"><div class="review-card-heading"><strong>${escapeHtml(review.nomeUsuario || 'Pessoa trilheira')}</strong><span class="review-rating">★ ${Number(review.nota)}/5</span></div><p>${review.comentario ? escapeHtml(review.comentario) : '<span class="muted">Sem comentário escrito.</span>'}</p>${user?.idUsuario===review.idUsuario?`<button class="button ghost" data-action="edit-review" data-id="${review.idAvaliacao}" data-note="${review.nota}" data-comment="${escapeHtml(review.comentario||'')}">Editar</button> <button class="button danger" data-action="delete-review" data-id="${review.idAvaliacao}">Excluir</button>`:''}</article>`).join('')}</div>` : '<div class="empty review-empty">Ainda não há comentários. Seja a primeira pessoa a avaliar esta trilha.</div>'}
      ${user ? `<form id="review-form" data-id="${id}" class="panel review-form"><h3>Conte como foi sua experiência</h3><label>Nota<select name="nota"><option value="5">5 — Excelente</option><option value="4">4 — Muito boa</option><option value="3">3 — Boa</option><option value="2">2 — Regular</option><option value="1">1 — Difícil</option></select></label><label>Comentário<textarea name="comentario" maxlength="2000" placeholder="Como foi o percurso? Tem alguma dica para a próxima pessoa?" rows="4"></textarea></label><button class="button primary">Publicar avaliação</button></form>` : '<p class="review-signin"><a href="/?page=login">Entre na sua conta</a> para deixar uma avaliação.</p>'}
    </section>
    ${user?`<section class="trail-section"><h2>Concluir trilha</h2><form class="panel form-grid" id="history-form" data-trail="${id}"><label>Data<input type="date" name="dataRealizacao" value="${new Date().toISOString().slice(0,10)}" required></label><label>Tempo realizado (minutos)<input type="number" name="tempo" min="0" step="1"></label><label>Avaliação pessoal<select name="avaliacaoPessoal"><option value="">Sem nota</option>${[5,4,3,2,1].map(n=>`<option value="${n}">${n} / 5</option>`).join('')}</select></label><button class="button primary">Registrar conclusão</button></form></section><button class="button ghost" data-action="report" data-category="TRILHA" data-id="${id}">Reportar problema nesta trilha</button>`:''}
  </div></section>`;
  if (points.length && window.maplibregl) {
    startTrailMap(points);
  } else if (points.length) {
    loadMapLibrary().then(() => startTrailMap(points)).catch((error) => {
      const status = document.getElementById('trail-map-message');
      if (status) status.textContent = `${error.message} Os checkpoints continuam listados abaixo.`;
    });
  }
}
function startTrailMap(points) {
  const mapScript = document.createElement('script');
  mapScript.src = 'static/js/trail-detail.js';
  mapScript.dataset.checkpoints = JSON.stringify(points);
  document.body.append(mapScript);
  mapScript.onerror = () => {
    const status = document.getElementById('trail-map-message');
    if (status) status.textContent = 'Não foi possível iniciar o mapa. Os checkpoints continuam listados abaixo.';
  };
}
async function eventsPage() {
  const d=await api('/events');
  app.innerHTML=`<section class="section"><div class="container"><h1>Expedições</h1>${user?`<form class="panel form-grid" id="event-form"><h2>Criar expedição</h2><label>Título<input name="titulo" required></label><label>Descrição<textarea name="descricao"></textarea></label><label>Trilha<select name="idTrilha">${d.trails.map(t=>`<option value="${t.idTrilha}">${escapeHtml(t.nome)}</option>`).join('')}</select></label><label>Data<input name="data" type="date"></label><label>Horário<input name="horario" type="time"></label><label>Vagas<input name="vagas" type="number" min="1"></label><label>Tipo<select name="tipo"><option value="GRUPO">Grupo</option><option value="INDIVIDUAL">Individual</option></select></label><button class="button primary">Criar</button></form>`:''}<div class="event-list">${d.items.map(e=>{const participating=d.participating.includes(e.idEvento), owner=user?.idUsuario===e.idCriador;return `<article class="panel event-card" data-event="${e.idEvento}" data-event-date="${e.data||''}" data-event-time="${e.horarioSaida?e.horarioSaida.slice(11,16):''}" data-event-spots="${e.vagas||''}"><div class="event-row"><div><strong>${escapeHtml(e.titulo)}</strong><p>${escapeHtml(e.descricao||'')}</p><p class="muted">${escapeHtml(e.data||'Data a definir')} ${e.horarioSaida?`· ${escapeHtml(e.horarioSaida.slice(11,16))}`:''} · ${escapeHtml(e.tipo)} · ${e.participantesAtuais} participante(s) · Organizador: ${escapeHtml(e.nomeCriador||'')}</p></div><div>${user?`<button class="button primary" data-action="${participating?'leave':'join'}" data-id="${e.idEvento}">${participating?'Sair':'Participar'}</button>`:'<a class="button ghost" href="/?page=login">Entrar para participar</a>'} ${owner?`<button class="button ghost" data-action="edit-event" data-id="${e.idEvento}">Editar</button><button class="button danger" data-action="delete-event" data-id="${e.idEvento}">Cancelar</button>`:''}</div></div><details><summary>Participantes confirmados (${e.participantes.length})</summary><p>${e.participantes.map(escapeHtml).join(', ')||'Nenhum participante'}</p></details><details><summary>Comentários (${e.comentarios.length})</summary><div class="review-list">${e.comentarios.map(c=>`<p><strong>${escapeHtml(c.nomeUsuario)}:</strong> ${escapeHtml(c.texto)}</p>`).join('')}</div>${participating?`<form class="form-grid event-comment-form" data-id="${e.idEvento}"><textarea name="texto" required maxlength="2000" placeholder="Combine os detalhes da expedição"></textarea><button class="button ghost">Comentar</button></form>`:''}</details>${user?`<button class="button ghost" data-action="report" data-category="EVENTO" data-id="${e.idEvento}">Reportar evento</button>`:''}</article>`;}).join('')||'<div class="empty">Nenhuma expedição disponível.</div>'}</div></div></section>`;
}
async function favoritesPage() { const d=await api('/favorites'); app.innerHTML=`<section class="section"><div class="container"><h1>Favoritos</h1>${d.items.length?`<div class="cards">${d.items.map(t=>card({...t,favorito:true})).join('')}</div>`:'<div class="empty">Você ainda não salvou trilhas.</div>'}</div></section>`; }
async function profilePage() {
  const [h]=await Promise.all([api('/history')]);
  app.innerHTML=`<section class="section"><div class="container"><h1>Perfil</h1>${user?.fotoPerfil?`<img src="${escapeHtml(user.fotoPerfil)}" alt="Foto de ${escapeHtml(user.nome)}" style="width:96px;height:96px;object-fit:cover;border-radius:50%">`:''}<form class="panel form-grid" id="profile-form"><label>Nome<input name="nome" maxlength="100" required value="${escapeHtml(user?.nome||'')}"></label><label>E-mail<input name="email" type="email" required value="${escapeHtml(user?.email||'')}"></label><label>Foto (URL)<input name="fotoPerfil" type="url" value="${escapeHtml(user?.fotoPerfil||'')}"></label><button class="button primary">Salvar perfil</button></form><h2 style="margin-top:30px">Histórico de trilhas</h2>${h.items.length?h.items.map(x=>`<article class="panel"><strong>${escapeHtml(x.nomeTrilha)}</strong><p>${escapeHtml(x.dataRealizacao||'')} · ${x.tempo??'—'} min · Avaliação pessoal: ${x.avaliacaoPessoal??'—'}</p></article>`).join(''):'<p class="muted">Você ainda não registrou trilhas.</p>'}</div></section>`;
}
function resetPage() {
  const page=new URLSearchParams(location.search).get('page');
  if(page==='forgot-password') app.innerHTML=`<section class="section"><div class="container"><form id="forgot-form" class="panel form-grid"><h1>Recuperar senha</h1><label>E-mail<input type="email" name="email" required></label><button class="button primary">Enviar link de recuperação</button></form></div></section>`;
  else app.innerHTML=`<section class="section"><div class="container"><form id="reset-form" class="panel form-grid"><h1>Definir nova senha</h1><input type="hidden" name="token" value="${escapeHtml(new URLSearchParams(location.search).get('token')||'')}"><label>Nova senha<input type="password" name="senha" minlength="6" required></label><button class="button primary">Salvar nova senha</button></form></div></section>`;
}
async function render() {
  try { user=(await api('/session')).user; navRender(); const p=new URLSearchParams(location.search); const page=p.get('page'); if(page==='login') authPage(); else if(page==='register') authPage(true); else if(page==='forgot-password'||page==='reset-password') resetPage(); else if(page==='trail') await trailPage(p.get('id')); else if(page==='events') await eventsPage(); else if(page==='favorites') await favoritesPage(); else if(page==='profile') user?await profilePage():authPage(); else await home(); } catch(e) { app.innerHTML=`<section class="section"><div class="container empty">${escapeHtml(e.message)}</div></section>`; }
}
app.addEventListener('submit', async e => {
  const f=e.target; if(!f.matches('form')) return; e.preventDefault(); const d=Object.fromEntries(new FormData(f));
  try {
    if(f.id==='search'||f.id==='trail-filters') { location.href=`/?${new URLSearchParams(Object.fromEntries(Object.entries(d).filter(([,v])=>v)))}`; return; }
    if(f.id==='auth-form') { const reg=new URLSearchParams(location.search).get('page')==='register'; if(reg)d.aceitouTermo=f.elements.aceitouTermo.checked; const out=await api(`/auth/${reg?'register':'login'}`,{method:'POST',body:JSON.stringify(d)}); user=out.user; location.href='/'; return; }
    if(f.id==='event-form') { await api('/events',{method:'POST',body:JSON.stringify(d)}); notice('Expedição criada.','success'); await render(); return; }
    if(f.id==='review-form') { await api(`/trails/${f.dataset.id}/reviews`,{method:'POST',body:JSON.stringify(d)}); notice('Avaliação publicada.','success'); await render(); return; }
    if(f.id==='history-form') { d.idTrilha=Number(f.dataset.trail); d.tempo=d.tempo?Number(d.tempo):null; d.avaliacaoPessoal=d.avaliacaoPessoal?Number(d.avaliacaoPessoal):null; await api('/history',{method:'POST',body:JSON.stringify(d)}); notice('Trilha registrada no histórico.','success'); await render(); return; }
    if(f.id==='profile-form') { user=(await api('/profile',{method:'PATCH',body:JSON.stringify(d)})).user; notice('Perfil atualizado.','success'); await render(); return; }
    if(f.id==='forgot-form') { const result=await api('/auth/password-reset',{method:'POST',body:JSON.stringify(d)}); notice(result.resetLink?`Link de desenvolvimento: ${result.resetLink}`:result.message,'success'); return; }
    if(f.id==='reset-form') { await api('/auth/password-reset/confirm',{method:'POST',body:JSON.stringify(d)}); notice('Senha atualizada. Entre com a nova senha.','success'); location.href='/?page=login'; return; }
    if(f.matches('.event-comment-form')) { await api(`/events/${f.dataset.id}/comments`,{method:'POST',body:JSON.stringify(d)}); notice('Comentário publicado.','success'); await render(); }
  } catch(err) { notice(err.message,'danger'); }
});
app.addEventListener('change', e=>{const box=e.target.closest('[data-checklist]');if(!box)return;try{const id=new URLSearchParams(location.search).get('id');const state=readChecklistState(id);state[box.dataset.checklist]=box.checked;localStorage.setItem(checklistStorageKey(id),JSON.stringify(state));}catch{box.checked=!box.checked;notice('Não foi possível salvar as marcações neste navegador.','danger');}});
app.addEventListener('click', async e => {
  const b=e.target.closest('[data-action]'); if(!b)return; const id=b.dataset.id;
  try {
    if(b.dataset.action==='logout') {await api('/auth/logout',{method:'POST'});location.href='/';return;}
    if(b.dataset.action==='favorite') await api(`/trails/${id}/favorite`,{method:b.dataset.fav==='true'?'DELETE':'POST'});
    else if(b.dataset.action==='join') await api(`/events/${id}/participation`,{method:'POST'});
    else if(b.dataset.action==='leave') await api(`/events/${id}/participation`,{method:'DELETE'});
    else if(b.dataset.action==='nearby') { if(!navigator.geolocation) throw new Error('Este navegador não oferece geolocalização.'); navigator.geolocation.getCurrentPosition(pos=>{const p=new URLSearchParams(location.search);p.set('lat',pos.coords.latitude);p.set('lon',pos.coords.longitude);location.href=`/?${p}`;},()=>notice('Não foi possível obter sua localização.','danger'));return; }
    else if(b.dataset.action==='delete-review') {if(!confirm('Excluir sua avaliação?'))return;await api(`/reviews/${id}`,{method:'DELETE'});}
    else if(b.dataset.action==='edit-review') {const comentario=prompt('Edite seu comentário:',b.dataset.comment||'');if(comentario===null)return;const nota=prompt('Nota de 1 a 5:',b.dataset.note);if(nota===null)return;await api(`/reviews/${id}`,{method:'PUT',body:JSON.stringify({nota,comentario})});}
    else if(b.dataset.action==='delete-event') {if(!confirm('Cancelar e excluir esta expedição?'))return;await api(`/events/${id}`,{method:'DELETE'});}
    else if(b.dataset.action==='edit-event') {const card=b.closest('.event-card');const titulo=prompt('Título da expedição:',card.querySelector('strong').textContent);if(titulo===null)return;const descricao=prompt('Descrição:',card.querySelector('.event-row p')?.textContent||'');if(descricao===null)return;const data=prompt('Data (AAAA-MM-DD; vazio remove):',card.dataset.eventDate);if(data===null)return;const horario=prompt('Horário (HH:MM; vazio remove):',card.dataset.eventTime);if(horario===null)return;const vagas=prompt('Número de vagas (vazio sem limite):',card.dataset.eventSpots);if(vagas===null)return;await api(`/events/${id}`,{method:'PUT',body:JSON.stringify({titulo,descricao,data,horario,vagas})});}
    else if(b.dataset.action==='report') {const descricao=prompt('Descreva o problema:');if(!descricao)return;await api('/reports',{method:'POST',body:JSON.stringify({categoria:b.dataset.category,idTrilha:b.dataset.category==='TRILHA'?Number(id):undefined,idEvento:b.dataset.category==='EVENTO'?Number(id):undefined,descricao})});notice('Relato enviado. Obrigado.','success');return;}
    await render();
  } catch(err) { notice(err.message,'danger'); }
});
window.addEventListener('popstate', render);
render();
