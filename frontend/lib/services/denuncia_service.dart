import '../models/denuncia.dart';
import 'api_client.dart';

class DenunciaService {
  DenunciaService._();

  static Future<Denuncia> criar(Denuncia denuncia) async {
    final data = await ApiClient.post(
      '/eventos/${denuncia.idEvento}/denuncias',
      denuncia.toJson(),
    );
    return Denuncia.fromJson(data as Map<String, dynamic>);
  }
}
