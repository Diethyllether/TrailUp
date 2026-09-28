const expeditionMapScript = document.currentScript;
const expeditionMapContainer = document.getElementById('expedition-map');

if (expeditionMapContainer) {
  const expeditions = JSON.parse(expeditionMapScript.dataset.expeditions || '[]')
    .filter((expedition) => Number.isFinite(Number(expedition.latitude)) && Number.isFinite(Number(expedition.longitude)));

  if (expeditions.length) {
    const first = [Number(expeditions[0].longitude), Number(expeditions[0].latitude)];
    const map = new maplibregl.Map({ container: expeditionMapContainer, style: 'https://tiles.openfreemap.org/styles/liberty', center: first, zoom: 11 });
    map.addControl(new maplibregl.NavigationControl(), 'top-right');

    const bounds = new maplibregl.LngLatBounds(first, first);
    expeditions.forEach((expedition) => {
      const point = [Number(expedition.longitude), Number(expedition.latitude)];
      const title = String(expedition.titulo).replace(/[&<>"']/g, (character) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[character]);
      bounds.extend(point);
      new maplibregl.Marker({ color: '#3DB861' }).setLngLat(point).setPopup(new maplibregl.Popup({ offset: 20 }).setHTML(`<strong>${title}</strong><br>${String(expedition.participantesAtuais)} participante(s)`)).addTo(map);
    });

    if (expeditions.length > 1) map.fitBounds(bounds, { padding: 70, maxZoom: 14 });
  }
}
