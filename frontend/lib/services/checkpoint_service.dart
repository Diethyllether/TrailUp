import '../models/checkpoint.dart';
import 'api_client.dart';

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
}
