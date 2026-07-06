import '../models/usuario.dart';
import 'api_client.dart';

class AuthService {
  AuthService._();

  static Future<Usuario> login(String email, String senha) async {
    final data = await ApiClient.post('/login', {'email': email, 'senha': senha});
    ApiClient.authToken = data['token'] as String?;
    return Usuario.fromJson(data['usuario'] as Map<String, dynamic>);
  }

  static Future<Usuario> cadastrar(Usuario usuario) async {
    final data = await ApiClient.post('/usuarios', usuario.toJson());
    return Usuario.fromJson(data as Map<String, dynamic>);
  }

  static Future<void> recuperarSenha(String email) async {
    await ApiClient.post('/recuperar-senha', {'email': email});
  }

  static Future<Usuario> atualizarPerfil(Usuario usuario) async {
    final data = await ApiClient.put('/usuarios/${usuario.idUsuario}', usuario.toJson());
    return Usuario.fromJson(data as Map<String, dynamic>);
  }

  static void logout() {
    ApiClient.authToken = null;
  }
}
