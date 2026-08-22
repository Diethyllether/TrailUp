import 'dart:convert';
import 'dart:io';
import 'dart:math' as math;

import 'package:http/http.dart' as http;
import 'package:path_provider/path_provider.dart';

import '../core/config/map_config.dart';
import '../models/checkpoint.dart';
import 'api_client.dart';

class OfflineMapDownloadResult {
  final String tileTemplate;
  final int tileCount;
  final int bytesDownloaded;

  const OfflineMapDownloadResult({
    required this.tileTemplate,
    required this.tileCount,
    required this.bytesDownloaded,
  });
}

class OfflineMapService {
  OfflineMapService._();

  static const _minZoom = 12;
  static const _preferredMaxZoom = 16;
  static const _maxTiles = 650;

  static Future<Directory> _trailDirectory(int idTrilha) async {
    final base = await getApplicationDocumentsDirectory();
    return Directory('${base.path}/trailup_offline/trilha_$idTrilha');
  }

  static Future<File> _manifestFile(int idTrilha) async {
    final dir = await _trailDirectory(idTrilha);
    return File('${dir.path}/manifest.json');
  }

  static bool _validCoord(Checkpoint c) {
    return c.latitude >= -85.05112878 &&
        c.latitude <= 85.05112878 &&
        c.longitude >= -180 &&
        c.longitude <= 180 &&
        !(c.latitude == 0 && c.longitude == 0);
  }

  static int _tileX(double longitude, int zoom) {
    final n = 1 << zoom;
    final x = (((longitude + 180.0) / 360.0) * n).floor();
    return x.clamp(0, n - 1);
  }

  static int _tileY(double latitude, int zoom) {
    final n = 1 << zoom;
    final lat = latitude.clamp(-85.05112878, 85.05112878);
    final latRad = lat * math.pi / 180.0;
    final y = ((1.0 -
                math.log(math.tan(latRad) + 1 / math.cos(latRad)) /
                    math.pi) /
            2.0 *
            n)
        .floor();
    return y.clamp(0, n - 1);
  }

  static List<(int, int, int)> _tilesForBounds(
    List<Checkpoint> checkpoints,
    int maxZoom,
  ) {
    final latitudes = checkpoints.map((c) => c.latitude).toList();
    final longitudes = checkpoints.map((c) => c.longitude).toList();
    final minLat = latitudes.reduce(math.min);
    final maxLat = latitudes.reduce(math.max);
    final minLng = longitudes.reduce(math.min);
    final maxLng = longitudes.reduce(math.max);

    final tiles = <(int, int, int)>[];
    for (var z = _minZoom; z <= maxZoom; z++) {
      final n = 1 << z;
      final x0 = (_tileX(minLng, z) - 1).clamp(0, n - 1);
      final x1 = (_tileX(maxLng, z) + 1).clamp(0, n - 1);
      final y0 = (_tileY(maxLat, z) - 1).clamp(0, n - 1);
      final y1 = (_tileY(minLat, z) + 1).clamp(0, n - 1);

      for (var x = x0; x <= x1; x++) {
        for (var y = y0; y <= y1; y++) {
          tiles.add((z, x, y));
        }
      }
    }
    return tiles;
  }

  static Future<String?> localTileTemplate(int idTrilha) async {
    try {
      final manifest = await _manifestFile(idTrilha);
      if (!await manifest.exists()) return null;
      final data = jsonDecode(await manifest.readAsString()) as Map<String, dynamic>;
      final template = data['tileTemplate'] as String?;
      if (template == null || template.isEmpty) return null;
      return template;
    } catch (_) {
      return null;
    }
  }

  static Future<bool> isDownloaded(int idTrilha) async {
    return await localTileTemplate(idTrilha) != null;
  }

  static Future<OfflineMapDownloadResult> downloadTrail({
    required int idTrilha,
    required List<Checkpoint> checkpoints,
    void Function(double progress)? onProgress,
  }) async {
    final valid = checkpoints.where(_validCoord).toList();
    if (valid.isEmpty) {
      throw StateError('A trilha não possui checkpoints GPS válidos para baixar.');
    }

    var maxZoom = _preferredMaxZoom;
    var tiles = _tilesForBounds(valid, maxZoom);
    while (tiles.length > _maxTiles && maxZoom > _minZoom) {
      maxZoom--;
      tiles = _tilesForBounds(valid, maxZoom);
    }
    if (tiles.length > _maxTiles) {
      throw StateError('A área da trilha é grande demais para o download offline automático.');
    }

    final dir = await _trailDirectory(idTrilha);
    if (await dir.exists()) {
      await dir.delete(recursive: true);
    }
    await dir.create(recursive: true);

    var completed = 0;
    var bytesDownloaded = 0;

    for (final tile in tiles) {
      final (z, x, y) = tile;
      final tileDir = Directory('${dir.path}/$z/$x');
      await tileDir.create(recursive: true);
      final file = File('${tileDir.path}/$y.jpg');
      final url = MapConfig.satelliteTileUrl
          .replaceAll('{z}', '$z')
          .replaceAll('{x}', '$x')
          .replaceAll('{y}', '$y');

      final response = await http.get(
        Uri.parse(url),
        headers: const {'User-Agent': MapConfig.userAgent},
      );
      if (response.statusCode < 200 || response.statusCode >= 300) {
        throw HttpException('Falha ao baixar tile $z/$x/$y (${response.statusCode})');
      }
      await file.writeAsBytes(response.bodyBytes, flush: false);
      bytesDownloaded += response.bodyBytes.length;
      completed++;
      onProgress?.call(completed / tiles.length);
    }

    final tileTemplate = '${dir.path}/{z}/{x}/{y}.jpg';
    final manifest = await _manifestFile(idTrilha);
    await manifest.writeAsString(jsonEncode({
      'idTrilha': idTrilha,
      'tileTemplate': tileTemplate,
      'minZoom': _minZoom,
      'maxZoom': maxZoom,
      'tileCount': tiles.length,
      'bytesDownloaded': bytesDownloaded,
      'downloadedAt': DateTime.now().toIso8601String(),
    }));

    // Mantém o registro do download também no backend para o modelo ER.
    try {
      await ApiClient.post('/trilhas/$idTrilha/mapas-offline', {
        'arquivoUrl': tileTemplate,
        'tamanhoArquivo': bytesDownloaded / (1024 * 1024),
      });
    } catch (_) {
      // O mapa local continua válido mesmo se o registro remoto falhar.
    }

    return OfflineMapDownloadResult(
      tileTemplate: tileTemplate,
      tileCount: tiles.length,
      bytesDownloaded: bytesDownloaded,
    );
  }

  static Future<void> remove(int idTrilha) async {
    final dir = await _trailDirectory(idTrilha);
    if (await dir.exists()) await dir.delete(recursive: true);
  }
}
