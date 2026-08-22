import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import '../core/config/map_config.dart';
import '../core/theme/app_theme.dart';

class MapPin {
  final LatLng position;
  final String? label;
  final Color color;
  final IconData icon;
  final VoidCallback? onTap;

  const MapPin({
    required this.position,
    this.label,
    this.color = AppColors.greenLight,
    this.icon = Icons.place,
    this.onTap,
  });
}

class SatelliteMapWidget extends StatefulWidget {
  final List<MapPin> pins;
  final List<LatLng> route;
  final LatLng? center;
  final double? zoom;
  final bool satellite;
  final bool interactive;
  final bool fitBounds;
  final EdgeInsets fitPadding;
  final String? offlineTileTemplate;

  const SatelliteMapWidget({
    super.key,
    this.pins = const [],
    this.route = const [],
    this.center,
    this.zoom,
    this.satellite = true,
    this.interactive = true,
    this.fitBounds = true,
    this.fitPadding = const EdgeInsets.all(40),
    this.offlineTileTemplate,
  });

  @override
  State<SatelliteMapWidget> createState() => _SatelliteMapWidgetState();
}

class _SatelliteMapWidgetState extends State<SatelliteMapWidget> {
  final _mapController = MapController();
  final _networkTileProvider = NetworkTileProvider();

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) => _fitToContent());
  }

  @override
  void didUpdateWidget(SatelliteMapWidget oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.pins != widget.pins ||
        oldWidget.route != widget.route ||
        oldWidget.center != widget.center ||
        oldWidget.offlineTileTemplate != widget.offlineTileTemplate) {
      WidgetsBinding.instance.addPostFrameCallback((_) => _fitToContent());
    }
  }

  void _fitToContent() {
    if (!widget.fitBounds) return;

    final points = <LatLng>[
      ...widget.pins.map((p) => p.position),
      ...widget.route,
    ];
    if (points.isEmpty) return;

    if (points.length == 1) {
      _mapController.move(points.first, widget.zoom ?? 14);
      return;
    }

    _mapController.fitCamera(
      CameraFit.bounds(
        bounds: LatLngBounds.fromPoints(points),
        padding: widget.fitPadding,
        maxZoom: 16,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final initialCenter = widget.center ?? MapConfig.defaultCenter;
    final initialZoom = widget.zoom ?? MapConfig.defaultZoom;
    final offline = widget.offlineTileTemplate != null;

    return FlutterMap(
      mapController: _mapController,
      options: MapOptions(
        initialCenter: initialCenter,
        initialZoom: initialZoom,
        minZoom: offline ? 12 : 2,
        maxZoom: offline ? 16 : 19,
        interactionOptions: InteractionOptions(
          flags: widget.interactive ? InteractiveFlag.all : InteractiveFlag.none,
        ),
      ),
      children: [
        TileLayer(
          urlTemplate: offline
              ? widget.offlineTileTemplate!
              : (widget.satellite ? MapConfig.satelliteTileUrl : MapConfig.streetTileUrl),
          userAgentPackageName: offline ? null : MapConfig.userAgent,
          minZoom: offline ? 12 : 2,
          maxZoom: offline ? 16 : 19,
          maxNativeZoom: offline ? 16 : 19,
          tileProvider: offline ? FileTileProvider() : _networkTileProvider,
          errorTileCallback: (tile, error, stackTrace) {
            debugPrint('TrailUp: falha ao carregar tile ${tile.coordinates}: $error');
          },
        ),
        if (widget.route.length > 1)
          PolylineLayer(
            polylines: [
              Polyline(
                points: widget.route,
                color: AppColors.greenLight,
                strokeWidth: 4,
                borderColor: Colors.white.withOpacity(0.6),
                borderStrokeWidth: 1.5,
              ),
            ],
          ),
        MarkerLayer(
          markers: [
            for (final pin in widget.pins) _buildMarker(pin),
            if (widget.pins.isEmpty)
              for (var i = 0; i < widget.route.length; i++) _buildRouteMarker(i),
          ],
        ),
        RichAttributionWidget(
          alignment: AttributionAlignment.bottomRight,
          attributions: [
            TextSourceAttribution(
              offline || widget.satellite ? 'Esri World Imagery' : 'OpenStreetMap contributors',
              onTap: () {},
            ),
          ],
        ),
      ],
    );
  }

  Marker _buildMarker(MapPin pin) {
    return Marker(
      point: pin.position,
      width: 140,
      height: 58,
      alignment: Alignment.topCenter,
      child: GestureDetector(
        onTap: pin.onTap,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              width: 32,
              height: 32,
              decoration: BoxDecoration(
                color: pin.color,
                shape: BoxShape.circle,
                border: Border.all(color: Colors.white, width: 2),
                boxShadow: [
                  BoxShadow(color: Colors.black.withOpacity(0.35), blurRadius: 4, offset: const Offset(0, 2)),
                ],
              ),
              child: Icon(pin.icon, size: 16, color: Colors.white),
            ),
            if (pin.label != null)
              Flexible(
                child: Container(
                  margin: const EdgeInsets.only(top: 2),
                  padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                  decoration: BoxDecoration(
                    color: AppColors.bgDark.withOpacity(0.85),
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: Text(
                    pin.label!,
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: const TextStyle(color: AppColors.textPrimary, fontSize: 9, fontWeight: FontWeight.bold),
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }

  Marker _buildRouteMarker(int index) {
    final point = widget.route[index];
    final isStart = index == 0;
    final isEnd = index == widget.route.length - 1;
    final color = isStart
        ? AppColors.greenLight
        : isEnd
            ? AppColors.amber
            : AppColors.green.withOpacity(0.8);

    return Marker(
      point: point,
      width: 20,
      height: 20,
      child: Container(
        decoration: BoxDecoration(
          color: color,
          shape: BoxShape.circle,
          border: Border.all(color: Colors.white, width: 2),
        ),
      ),
    );
  }
}
