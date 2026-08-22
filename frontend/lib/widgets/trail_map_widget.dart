import 'dart:async';

import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';
import 'package:latlong2/latlong.dart';
import '../core/theme/app_theme.dart';
import '../models/checkpoint.dart';
import 'satellite_map_widget.dart';

class TrailMapWidget extends StatefulWidget {
  final List<Checkpoint> checkpoints;
  final String? localizacao;
  final String? offlineTileTemplate;

  const TrailMapWidget({
    super.key,
    required this.checkpoints,
    this.localizacao,
    this.offlineTileTemplate,
  });

  @override
  State<TrailMapWidget> createState() => _TrailMapWidgetState();
}

class _TrailMapWidgetState extends State<TrailMapWidget> {
  StreamSubscription<Position>? _positionSubscription;
  LatLng? _currentPosition;
  String? _locationError;

  @override
  void initState() {
    super.initState();
    _startLocationTracking();
  }

  @override
  void dispose() {
    _positionSubscription?.cancel();
    super.dispose();
  }

  Future<void> _startLocationTracking() async {
    try {
      final serviceEnabled = await Geolocator.isLocationServiceEnabled();
      if (!serviceEnabled) {
        if (mounted) setState(() => _locationError = 'Ative o GPS para ver sua posição');
        return;
      }

      var permission = await Geolocator.checkPermission();
      if (permission == LocationPermission.denied) {
        permission = await Geolocator.requestPermission();
      }
      if (permission == LocationPermission.denied || permission == LocationPermission.deniedForever) {
        if (mounted) setState(() => _locationError = 'Permita a localização para navegar');
        return;
      }

      final firstPosition = await Geolocator.getCurrentPosition();
      if (mounted) {
        setState(() {
          _currentPosition = LatLng(firstPosition.latitude, firstPosition.longitude);
          _locationError = null;
        });
      }

      _positionSubscription = Geolocator.getPositionStream(
        locationSettings: const LocationSettings(
          accuracy: LocationAccuracy.high,
          distanceFilter: 5,
        ),
      ).listen((position) {
        if (!mounted) return;
        setState(() {
          _currentPosition = LatLng(position.latitude, position.longitude);
          _locationError = null;
        });
      });
    } catch (_) {
      if (mounted) setState(() => _locationError = 'Localização indisponível');
    }
  }

  bool _isValidCoord(double lat, double lng) {
    return lat >= -90 && lat <= 90 && lng >= -180 && lng <= 180 && !(lat == 0 && lng == 0);
  }

  List<LatLng> get _route {
    return widget.checkpoints
        .where((c) => _isValidCoord(c.latitude, c.longitude))
        .map((c) => LatLng(c.latitude, c.longitude))
        .toList();
  }

  List<MapPin> _checkpointPins(List<LatLng> route) {
    return List.generate(route.length, (i) {
      final isStart = i == 0;
      final isEnd = i == route.length - 1;
      return MapPin(
        position: route[i],
        label: isStart ? 'Início' : isEnd ? 'Fim' : 'Checkpoint ${i + 1}',
        color: isStart ? AppColors.greenLight : isEnd ? AppColors.amber : AppColors.green,
        icon: isStart ? Icons.flag : isEnd ? Icons.flag_circle : Icons.location_on,
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    final route = _route;
    final pins = _checkpointPins(route);
    final offline = widget.offlineTileTemplate != null;

    if (_currentPosition != null) {
      pins.add(
        MapPin(
          position: _currentPosition!,
          label: 'Você está aqui',
          color: Colors.blue,
          icon: Icons.navigation,
        ),
      );
    }

    return Container(
      height: 320,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: AppColors.greenLight.withOpacity(0.35)),
      ),
      clipBehavior: Clip.antiAlias,
      child: Stack(
        children: [
          if (route.isNotEmpty)
            SatelliteMapWidget(
              route: route,
              pins: pins,
              center: route.first,
              zoom: 15,
              fitBounds: route.length > 1,
              fitPadding: const EdgeInsets.fromLTRB(42, 64, 42, 48),
              offlineTileTemplate: widget.offlineTileTemplate,
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
                    _currentPosition == null ? Icons.gps_not_fixed : Icons.gps_fixed,
                    size: 13,
                    color: Colors.white,
                  ),
                  const SizedBox(width: 5),
                  Text(
                    _locationError ?? (_currentPosition == null ? 'Obtendo localização…' : 'Localização em tempo real'),
                    style: const TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.bold),
                  ),
                ],
              ),
            ),
          ),
          if (offline)
            Positioned(
              right: 10,
              top: 10,
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 9, vertical: 6),
                decoration: BoxDecoration(
                  color: AppColors.bgDark.withOpacity(0.92),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: const Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(Icons.offline_pin, size: 13, color: AppColors.greenLight),
                    SizedBox(width: 5),
                    Text('Mapa offline',
                        style: TextStyle(color: AppColors.greenLight, fontSize: 10, fontWeight: FontWeight.bold)),
                  ],
                ),
              ),
            ),
          if (widget.localizacao != null && widget.localizacao!.isNotEmpty)
            Positioned(
              left: 10,
              bottom: 10,
              child: Container(
                constraints: const BoxConstraints(maxWidth: 230),
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
                    Flexible(
                      child: Text(
                        widget.localizacao!,
                        overflow: TextOverflow.ellipsis,
                        style: const TextStyle(color: AppColors.textDim, fontSize: 10),
                      ),
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
