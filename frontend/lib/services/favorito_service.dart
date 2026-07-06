import '../models/favorito.dart';
import 'api_client.dart';

class FavoritoService {
  FavoritoService._();

  static Future<List<Favorito>> listar(int idUsuario) async {
    final data = await ApiClient.get('/usuarios/$idUsuario/favoritos') as List;
    return data.map((e) => Favorito.fromJson(e as Map<String, dynamic>)).toList();
  }

  static Future<Favorito> adicionar(int idTrilha) async {
    final data = await ApiClient.post('/favoritos', {'idTrilha': idTrilha});
    return Favorito.fromJson(data as Map<String, dynamic>);
  }

  static Future<void> remover(int idTrilha) async {
    await ApiClient.delete('/favoritos/$idTrilha');
  }
}
