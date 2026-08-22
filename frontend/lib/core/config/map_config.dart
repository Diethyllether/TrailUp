import 'package:latlong2/latlong.dart';

class MapConfig {
  MapConfig._();

  /// Esri World Imagery — satellite tiles, free for app use with attribution.
  static const satelliteTileUrl =
      'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}';

  /// OpenStreetMap — street map fallback.
  static const streetTileUrl = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png';

  static const userAgent = 'com.trailup.trailup_app';

  /// Centro padrão: Brasil.
  static const LatLng defaultCenter = LatLng(-15.7801, -47.9292);
  static const double defaultZoom = 4.5;

  static const LatLng rioDeJaneiro = LatLng(-22.9068, -43.1729);
}
