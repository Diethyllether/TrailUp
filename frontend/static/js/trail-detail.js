const trailMapScript = document.currentScript;
const trailMapContainer = document.getElementById('trail-map');

if (trailMapContainer) {
  const trailPoints = JSON.parse(trailMapScript.dataset.checkpoints || '[]')
    .map((point) => [Number(point.longitude), Number(point.latitude)])
    .filter((point) => Number.isFinite(point[0]) && Number.isFinite(point[1]));

  if (trailPoints.length) {
    const map = new maplibregl.Map({ container: trailMapContainer, style: 'https://tiles.openfreemap.org/styles/liberty', center: trailPoints[0], zoom: 14, attributionControl: true });
    map.addControl(new maplibregl.NavigationControl(), 'top-right');
    map.on('load', () => {
      map.addSource('trail-route', { type: 'geojson', data: { type: 'Feature', properties: {}, geometry: { type: 'LineString', coordinates: trailPoints } } });
      map.addLayer({ id: 'trail-route-line', type: 'line', source: 'trail-route', layout: { 'line-join': 'round', 'line-cap': 'round' }, paint: { 'line-color': '#3DB861', 'line-width': 6, 'line-opacity': 1 } });
      new maplibregl.Marker({ color: '#3DB861' }).setLngLat(trailPoints[0]).setPopup(new maplibregl.Popup({ offset: 20 }).setText('Início')).addTo(map);

      if (trailPoints.length > 1) {
        new maplibregl.Marker({ color: '#EB9E2E' }).setLngLat(trailPoints[trailPoints.length - 1]).setPopup(new maplibregl.Popup({ offset: 20 }).setText('Fim')).addTo(map);
        const bounds = new maplibregl.LngLatBounds(trailPoints[0], trailPoints[0]);
        trailPoints.forEach((point) => bounds.extend(point));
        map.fitBounds(bounds, { padding: 55, maxZoom: 16 });
        const southwest = bounds.getSouthWest();
        const northeast = bounds.getNorthEast();
        const longitudeMargin = Math.max((northeast.lng - southwest.lng) * 0.6, 0.015);
        const latitudeMargin = Math.max((northeast.lat - southwest.lat) * 0.6, 0.015);
        map.setMaxBounds([[southwest.lng - longitudeMargin, southwest.lat - latitudeMargin], [northeast.lng + longitudeMargin, northeast.lat + latitudeMargin]]);
      }
    });
  }
}
