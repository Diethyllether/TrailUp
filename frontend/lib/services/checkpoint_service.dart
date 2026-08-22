import '../models/checkpoint.dart';
import 'api_client.dart';
import 'offline_map_service.dart';

class CheckpointService {
  CheckpointService._();

  static Future<List<Checkpoint>> listarPorTrilha(int idTrilha) async {
    final data = await ApiClient.get('/trilhas/$idTrilha/checkpoints') as List;
    return data.map((e) => Checkpoint.fromJson(e as Map<String, dynamic>)).toList();
  }

  static Future<Checkpoint> registrar(Checkpoint checkpoint) async {
    final data = await ApiClient.post(
      '/trilhas/${checkpoint.idTrilha}/checkpoints',
      checkpoint.toJson(),
    );
    return Checkpoint.fromJson(data as Map<String, dynamic>);
  }

  /// Baixa os tiles de satélite da região ocupada pelos checkpoints da trilha
  /// e os persiste no armazenamento do aplicativo para navegação sem rede.
  static Future<OfflineMapDownloadResult> baixarMapaOffline(
    int idTrilha, {
    void Function(double progress)? onProgress,
  }) async {
    final checkpoints = await listarPorTrilha(idTrilha);
    return OfflineMapService.downloadTrail(
      idTrilha: idTrilha,
      checkpoints: checkpoints,
      onProgress: onProgress,
    );
  }
}
