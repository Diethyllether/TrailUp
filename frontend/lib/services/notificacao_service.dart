import '../models/notificacao.dart';
import 'api_client.dart';

class NotificacaoService {
  NotificacaoService._();

  static Future<List<Notificacao>> listar(int idUsuario) async {
    final data = await ApiClient.get('/usuarios/$idUsuario/notificacoes') as List;
    return data.map((e) => Notificacao.fromJson(e as Map<String, dynamic>)).toList();
  }

  static Future<void> marcarComoLida(int idNotificacao) async {
    await ApiClient.put('/notificacoes/$idNotificacao/lida', {});
  }
}
