import '../models/trilha.dart';
import '../models/avaliacao.dart';
import '../models/foto.dart';
import 'api_client.dart';

class TrilhaService {
  TrilhaService._();

  static Future<List<Trilha>> listar({String? busca, String? dificuldade}) async {
    final query = <String>[];
    if (busca != null && busca.isNotEmpty) {
      query.add('busca=${Uri.encodeQueryComponent(busca)}');
    }
    if (dificuldade != null && dificuldade != 'Todas') {
      query.add('dificuldade=${Uri.encodeQueryComponent(dificuldade)}');
    }
    final qs = query.isNotEmpty ? '?${query.join('&')}' : '';
    final data = await ApiClient.get('/trilhas$qs') as List;
    return data.map((e) => Trilha.fromJson(e as Map<String, dynamic>)).toList();
  }

  static Future<Trilha> buscarPorId(int idTrilha) async {
    final data = await ApiClient.get('/trilhas/$idTrilha');
    return Trilha.fromJson(data as Map<String, dynamic>);
  }

  static Future<List<Avaliacao>> listarAvaliacoes(int idTrilha) async {
    final data = await ApiClient.get('/trilhas/$idTrilha/avaliacoes') as List;
    return data.map((e) => Avaliacao.fromJson(e as Map<String, dynamic>)).toList();
  }

  static Future<Avaliacao> avaliar(Avaliacao avaliacao) async {
    final data = await ApiClient.post(
      '/trilhas/${avaliacao.idTrilha}/avaliacoes',
      avaliacao.toJson(),
    );
    return Avaliacao.fromJson(data as Map<String, dynamic>);
  }

  static Future<List<Foto>> listarFotos(int idTrilha) async {
    final data = await ApiClient.get('/trilhas/$idTrilha/fotos') as List;
    return data.map((e) => Foto.fromJson(e as Map<String, dynamic>)).toList();
  }
}
