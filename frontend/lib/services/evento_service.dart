import '../models/evento.dart';
import 'api_client.dart';

class EventoService {
  EventoService._();

  static Future<List<Evento>> listarProximos({bool apenasNoMapa = false}) async {
    final query = apenasNoMapa ? '?mapa=true' : '';
    final data = await ApiClient.get('/eventos$query') as List;
    return data.map((e) => Evento.fromJson(e as Map<String, dynamic>)).toList();
  }

  static Future<List<Evento>> listarPorTrilha(int idTrilha) async {
    final data = await ApiClient.get('/trilhas/$idTrilha/eventos') as List;
    return data.map((e) => Evento.fromJson(e as Map<String, dynamic>)).toList();
  }

  static Future<Evento> criar(Evento evento, List<int> idsTrilha) async {
    final body = evento.toJson()..['trilhas'] = idsTrilha;
    final data = await ApiClient.post('/eventos', body);
    return Evento.fromJson(data as Map<String, dynamic>);
  }

  static Future<void> participar(int idEvento, int idUsuario) async {
    await ApiClient.post('/eventos/$idEvento/entrar', {});
  }

  static Future<void> sair(int idEvento) async {
    await ApiClient.post('/eventos/$idEvento/sair', {});
  }
}
