import 'dart:async';
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
  static const _tileRadius = 1; // corredor 3x3 em torno de cada checkpoint
  static const _requestTimeout = Duration(seconds: 12);
  static const _maxAttempts = 3;

  static Future<Directory> _baseDirectory() async {
    final base = await getApplicationDocumentsDirectory();
    return Directory('${base.path}/trailup_offline');
  }

  static Future<Directory> _trailDirectory(int idTrilha) async {
    final base = await _baseDirectory();
    return Directory('${base.path}/trilha_$idTrilha');
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
    return x.clamp(0, n - 1).toInt();
  }

  static int _tileY(double latitude, int zoom) {
    final n = 1 << zoom;
    final lat = latitude.clamp(-85.05112878, 85.05112878).toDouble();
    final latRad = lat * math.pi / 180.0;
    final y = ((1.0 -
                math.log(math.tan(latRad) + 1 / math.cos(latRad)) /
                    math.pi) /
            2.0 *
            n)
        .floor();
    return y.clamp(0, n - 1).toInt();
  }

  /// Em vez de baixar o retângulo inteiro entre o ponto mais distante e o
  /// restante da rota, cria um corredor de tiles em torno dos checkpoints.
  /// Isso evita que um único checkpoint fora da rota faça o download explodir.
  static List<(int, int, int)> _tilesForRoute(
    List<Checkpoint> checkpoints,
    int maxZoom,
  ) {
    final unique = <String, (int, int, int)>{};

    for (var z = _minZoom; z <= maxZoom; z++) {
      final n = 1 << z;
      for (final checkpoint in checkpoints) {
        final cx = _tileX(checkpoint.longitude, z);
        final cy = _tileY(checkpoint.latitude, z);

        for (var dx = -_tileRadius; dx <= _tileRadius; dx++) {
          for (var dy = -_tileRadius; dy <= _tileRadius; dy++) {
            final x = (cx + dx).clamp(0, n - 1).toInt();
            final y = (cy + dy).clamp(0, n - 1).toInt();
            unique['$z/$x/$y'] = (z, x, y);
          }
        }
      }
    }

    final values = unique.values.toList()
      ..sort((a, b) {
        final z = a.$1.compareTo(b.$1);
        if (z != 0) return z;
        final x = a.$2.compareTo(b.$2);
        if (x != 0) return x;
        return a.$3.compareTo(b.$3);
      });
    return values;
  }

  static Future<String?> localTileTemplate(int idTrilha) async {
    try {
      final manifest = await _manifestFile(idTrilha);
      if (!await manifest.exists()) return null;
      final data = jsonDecode(await manifest.readAsString()) as Map<String, dynamic>;
      final template = data['tileTemplate'] as String?;
      if (template == null || template.isEmpty) return null;

      final sample = data['sampleTile'] as String?;
      if (sample != null && sample.isNotEmpty && !await File(sample).exists()) {
        return null;
      }
      return template;
    } catch (_) {
      return null;
    }
  }

  static Future<bool> isDownloaded(int idTrilha) async {
    return await localTileTemplate(idTrilha) != null;
  }

  static Future<http.Response> _downloadWithRetry(Uri uri) async {
    Object? lastError;

    for (var attempt = 1; attempt <= _maxAttempts; attempt++) {
      try {
        final response = await http
            .get(
              uri,
              headers: const {
                'User-Agent': MapConfig.userAgent,
                'Accept': 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8',
              },
            )
            .timeout(_requestTimeout);

        if (response.statusCode >= 200 && response.statusCode < 300 && response.bodyBytes.isNotEmpty) {
          return response;
        }
        lastError = HttpException('HTTP ${response.statusCode}');
      } on TimeoutException catch (e) {
        lastError = e;
      } on SocketException catch (e) {
        lastError = e;
      } catch (e) {
        lastError = e;
      }

      if (attempt < _maxAttempts) {
        await Future.delayed(Duration(milliseconds: 350 * attempt));
      }
    }

    throw StateError('Não foi possível baixar os tiles do mapa. Verifique sua conexão. ($lastError)');
  }

  static Future<OfflineMapDownloadResult> downloadTrail({
    required int idTrilha,
    required List<Checkpoint> checkpoints,
    void Function(double progress)? onProgress,
  }) async {
    final valid = checkpoints.where(_validCoord).toList();
    if (valid.isEmpty) {
      throw StateError(
        'Esta trilha ainda não possui checkpoints GPS válidos. Não há região suficiente para gerar o mapa offline.',
      );
    }

    var maxZoom = _preferredMaxZoom;
    var tiles = _tilesForRoute(valid, maxZoom);
    while (tiles.length > _maxTiles && maxZoom > _minZoom) {
      maxZoom--;
      tiles = _tilesForRoute(valid, maxZoom);
    }
    if (tiles.isEmpty) {
      throw StateError('Nenhum tile pôde ser calculado para esta trilha.');
    }
    if (tiles.length > _maxTiles) {
      throw StateError(
        'Esta trilha possui muitos checkpoints espalhados. O download offline ultrapassaria $_maxTiles tiles.',
      );
    }

    final base = await _baseDirectory();
    await base.create(recursive: true);

    final finalDir = await _trailDirectory(idTrilha);
    final tempDir = Directory('${base.path}/trilha_${idTrilha}_tmp');
    if (await tempDir.exists()) await tempDir.delete(recursive: true);
    await tempDir.create(recursive: true);

    var completed = 0;
    var bytesDownloaded = 0;
    String? firstTilePath;

    try {
      for (final tile in tiles) {
        final (z, x, y) = tile;
        final tileDir = Directory('${tempDir.path}/$z/$x');
        await tileDir.create(recursive: true);
        final file = File('${tileDir.path}/$y.jpg');

        final url = MapConfig.satelliteTileUrl
            .replaceAll('{z}', '$z')
            .replaceAll('{x}', '$x')
            .replaceAll('{y}', '$y');

        final response = await _downloadWithRetry(Uri.parse(url));
        await file.writeAsBytes(response.bodyBytes, flush: false);

        firstTilePath ??= file.path;
        bytesDownloaded += response.bodyBytes.length;
        completed++;
        onProgress?.call(completed / tiles.length);
      }

      if (firstTilePath == null) {
        throw StateError('O servidor não retornou imagens para esta região.');
      }

      // Só substitui um mapa antigo depois que o novo download terminou.
      if (await finalDir.exists()) {
        await finalDir.delete(recursive: true);
      }
      await tempDir.rename(finalDir.path);

      final tileTemplate = '${finalDir.path}/{z}/{x}/{y}.jpg';
      final sampleTile = firstTilePath.replaceFirst(tempDir.path, finalDir.path);
      final manifest = File('${finalDir.path}/manifest.json');
      await manifest.writeAsString(jsonEncode({
        'idTrilha': idTrilha,
        'tileTemplate': tileTemplate,
        'sampleTile': sampleTile,
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
    } catch (e) {
      if (await tempDir.exists()) {
        await tempDir.delete(recursive: true);
      }
      rethrow;
    }
  }

  static Future<void> remove(int idTrilha) async {
    final dir = await _trailDirectory(idTrilha);
    if (await dir.exists()) await dir.delete(recursive: true);
  }
}
