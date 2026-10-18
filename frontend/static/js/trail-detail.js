const trailMapScript = document.currentScript;
const trailMapContainer = document.getElementById('trail-map');

if (trailMapContainer) {
  const trailPoints = JSON.parse(trailMapScript.dataset.checkpoints || '[]')
    .map((point) => [Number(point.longitude), Number(point.latitude)])
    .filter((point) => Number.isFinite(point[0]) && Number.isFinite(point[1]));

  if (trailPoints.length) {
    const map = new maplibregl.Map({
      container: trailMapContainer,
      style: {
        version: 8,
        sources: { osm: { type: 'raster', tiles: ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'], tileSize: 256, attribution: '© OpenStreetMap contributors' } },
        layers: [{ id: 'osm-tiles', type: 'raster', source: 'osm' }],
      },
      center: trailPoints[0], zoom: 14, attributionControl: true,
    });
    map.addControl(new maplibregl.NavigationControl(), 'top-right');
    const mapMessage = document.getElementById('trail-map-message');
    map.on('error', () => {
      if (mapMessage && !map.isStyleLoaded()) mapMessage.textContent = 'Não foi possível carregar o mapa-base. Verifique a conexão e tente novamente.';
    });
    map.on('load', () => {
      if (mapMessage) mapMessage.remove();
      if (trailPoints.length > 1) {
        map.addSource('trail-route', { type: 'geojson', data: { type: 'Feature', properties: {}, geometry: { type: 'LineString', coordinates: trailPoints } } });
        map.addLayer({ id: 'trail-route-line', type: 'line', source: 'trail-route', layout: { 'line-join': 'round', 'line-cap': 'round' }, paint: { 'line-color': '#3DB861', 'line-width': 6, 'line-opacity': 1 } });
      }
      const bounds = new maplibregl.LngLatBounds(trailPoints[0], trailPoints[0]);
      trailPoints.forEach((point, index) => {
        bounds.extend(point);
        const isStart = index === 0;
        const isEnd = index === trailPoints.length - 1;
        const marker = new maplibregl.Marker({ color: isStart ? '#3DB861' : isEnd ? '#EB9E2E' : '#4D99FF' })
          .setLngLat(point)
          .setPopup(new maplibregl.Popup({ offset: 20 }).setText(isStart ? 'Início' : isEnd ? 'Fim' : `Checkpoint ${index + 1}`));
        marker.addTo(map);
      });
      if (trailPoints.length > 1) map.fitBounds(bounds, { padding: 55, maxZoom: 16 });
    });
  }
}
