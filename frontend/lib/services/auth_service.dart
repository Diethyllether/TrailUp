import '../models/usuario.dart';
import 'api_client.dart';
import 'session_service.dart';

class AuthService {
  AuthService._();

  static Future<Usuario> login(String email, String senha) async {
    final data = await ApiClient.post('/login', {'email': email, 'senha': senha});
    final token = data['token'] as String?;
    if (token == null || token.isEmpty) {
      throw StateError('Token de autenticação ausente.');
    }

    final usuario = Usuario.fromJson(data['usuario'] as Map<String, dynamic>);
    ApiClient.authToken = token;
    await SessionService.saveSession(token: token, usuario: usuario);
    return usuario;
  }

  static Future<Usuario?> restoreSession() async {
    final session = await SessionService.restoreSession();
    if (session == null) return null;

    ApiClient.authToken = session.token;
    return session.usuario;
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
    final atualizado = Usuario.fromJson(data as Map<String, dynamic>);
    await SessionService.updateUser(atualizado);
    return atualizado;
  }

  static Future<void> logout() async {
    ApiClient.authToken = null;
    await SessionService.clear();
  }
}
