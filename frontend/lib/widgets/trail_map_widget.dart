import 'package:flutter/material.dart';
import 'package:latlong2/latlong.dart';
import '../core/theme/app_theme.dart';
import '../models/checkpoint.dart';
import 'satellite_map_widget.dart';

class TrailMapWidget extends StatelessWidget {
  final List<Checkpoint> checkpoints;
  final String? localizacao;
  final LatLng? currentPosition;
  final bool navigationMode;

  const TrailMapWidget({
    super.key,
    required this.checkpoints,
    this.localizacao,
    this.currentPosition,
    this.navigationMode = false,
  });

  bool _isValidCoord(double lat, double lng) {
    return lat >= -90 && lat <= 90 && lng >= -180 && lng <= 180 && !(lat == 0 && lng == 0);
  }

  List<LatLng> get _route {
    return checkpoints
        .where((c) => _isValidCoord(c.latitude, c.longitude))
        .map((c) => LatLng(c.latitude, c.longitude))
        .toList();
  }

  List<MapPin> _checkpointPins(List<LatLng> route) {
    final pins = <MapPin>[];
    for (var i = 0; i < route.length; i++) {
      final isStart = i == 0;
      final isEnd = i == route.length - 1;
      pins.add(
        MapPin(
          position: route[i],
          label: isStart ? 'Início' : isEnd ? 'Fim' : 'Checkpoint ${i + 1}',
          color: isStart ? AppColors.greenLight : isEnd ? AppColors.amber : AppColors.green,
          icon: isStart ? Icons.flag : isEnd ? Icons.flag_circle : Icons.location_on,
        ),
      );
    }
    return pins;
  }

  @override
  Widget build(BuildContext context) {
    final route = _route;
    final pins = _checkpointPins(route);

    if (navigationMode && currentPosition != null) {
      pins.add(
        MapPin(
          position: currentPosition!,
          label: 'Você está aqui',
          color: Colors.blue,
          icon: Icons.navigation,
        ),
      );
    }

    return Container(
      height: navigationMode ? 360 : 220,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(14),
        border: Border.all(
          color: navigationMode ? AppColors.greenLight.withOpacity(0.5) : AppColors.greenLight.withOpacity(0.15),
        ),
      ),
      clipBehavior: Clip.antiAlias,
      child: Stack(
        children: [
          if (route.isNotEmpty)
            SatelliteMapWidget(
              route: route,
              pins: pins,
              center: route.first,
              zoom: navigationMode ? 15 : 14,
              fitBounds: route.length > 1,
              fitPadding: EdgeInsets.fromLTRB(42, navigationMode ? 64 : 48, 42, 48),
            )
          else
            Container(
              color: const Color(0xFF16201A),
              alignment: Alignment.center,
              child: const Text(
                'Sem coordenadas GPS para esta trilha.',
                style: TextStyle(color: AppColors.textDim, fontSize: 12),
              ),
            ),
          if (navigationMode)
            Positioned(
              left: 10,
              top: 10,
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                decoration: BoxDecoration(
                  color: AppColors.green.withOpacity(0.94),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(
                      currentPosition == null ? Icons.gps_off : Icons.gps_fixed,
                      size: 13,
                      color: Colors.white,
                    ),
                    const SizedBox(width: 5),
                    Text(
                      currentPosition == null ? 'Obtendo localização…' : 'Trilha em andamento',
                      style: const TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
              ),
            ),
          if (localizacao != null && localizacao!.isNotEmpty)
            Positioned(
              left: 10,
              bottom: 10,
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                decoration: BoxDecoration(
                  color: AppColors.bgDark.withOpacity(0.9),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Icon(Icons.location_on, size: 12, color: AppColors.greenLight),
                    const SizedBox(width: 4),
                    Text(
                      localizacao!,
                      style: const TextStyle(color: AppColors.textDim, fontSize: 10),
                    ),
                  ],
                ),
              ),
            ),
        ],
      ),
    );
  }
}
