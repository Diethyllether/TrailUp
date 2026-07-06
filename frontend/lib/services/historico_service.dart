import '../models/historico_trilha.dart';
import '../models/registro_realizado.dart';
import 'api_client.dart';

class HistoricoService {
  HistoricoService._();

  static Future<List<HistoricoTrilha>> listarPorUsuario(int idUsuario) async {
    final data = await ApiClient.get('/usuarios/$idUsuario/historico') as List;
    return data.map((e) => HistoricoTrilha.fromJson(e as Map<String, dynamic>)).toList();
  }

  static Future<HistoricoTrilha> registrar(HistoricoTrilha historico) async {
    final data = await ApiClient.post('/historico', historico.toJson());
    return HistoricoTrilha.fromJson(data as Map<String, dynamic>);
  }

  static Future<RegistroRealizado> registrarPosicao(RegistroRealizado registro) async {
    final data = await ApiClient.post(
      '/historico/${registro.idHistorico}/registros',
      registro.toJson(),
    );
    return RegistroRealizado.fromJson(data as Map<String, dynamic>);
  }
}
