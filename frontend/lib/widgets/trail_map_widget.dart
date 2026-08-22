import 'package:flutter/material.dart';
import 'package:latlong2/latlong.dart';
import '../core/theme/app_theme.dart';
import '../models/checkpoint.dart';
import 'satellite_map_widget.dart';

class TrailMapWidget extends StatelessWidget {
  final List<Checkpoint> checkpoints;
  final String? localizacao;

  const TrailMapWidget({super.key, required this.checkpoints, this.localizacao});

  bool get _temCoordenadasValidas {
    return checkpoints.any((c) => _isValidCoord(c.latitude, c.longitude));
  }

  bool _isValidCoord(double lat, double lng) {
    return lat.abs() > 1 && lng.abs() > 1;
  }

  List<LatLng> get _route {
    final valid = checkpoints
        .where((c) => _isValidCoord(c.latitude, c.longitude))
        .map((c) => LatLng(c.latitude, c.longitude))
        .toList();
    return valid;
  }

  @override
  Widget build(BuildContext context) {
    final route = _route;

    return Container(
      height: 220,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: AppColors.greenLight.withOpacity(0.15)),
      ),
      clipBehavior: Clip.antiAlias,
      child: Stack(
        children: [
          if (route.isNotEmpty)
            SatelliteMapWidget(
              route: route,
              pins: [
                MapPin(
                  position: route.first,
                  label: 'Início',
                  color: AppColors.greenLight,
                  icon: Icons.flag,
                ),
                if (route.length > 1)
                  MapPin(
                    position: route.last,
                    label: 'Fim',
                    color: AppColors.amber,
                    icon: Icons.place,
                  ),
              ],
              center: route.first,
              zoom: 14,
              fitBounds: route.length > 1,
              fitPadding: const EdgeInsets.all(48),
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
          if (!_temCoordenadasValidas && route.isEmpty)
            Positioned(
              right: 10,
              top: 10,
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: AppColors.bgDark.withOpacity(0.9),
                  borderRadius: BorderRadius.circular(6),
                ),
                child: const Text(
                  'Sem rota GPS',
                  style: TextStyle(color: AppColors.textDim, fontSize: 9),
                ),
              ),
            ),
        ],
      ),
    );
  }
}
