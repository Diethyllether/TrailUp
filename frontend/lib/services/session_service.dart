import 'dart:convert';

import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import '../models/usuario.dart';

class SessionService {
  SessionService._();

  static const _storage = FlutterSecureStorage();
  static const _tokenKey = 'trailup_auth_token';
  static const _userKey = 'trailup_auth_user';

  static Future<void> saveSession({
    required String token,
    required Usuario usuario,
  }) async {
    await _storage.write(key: _tokenKey, value: token);
    await _storage.write(key: _userKey, value: jsonEncode(usuario.toJson()));
  }

  static Future<({String token, Usuario usuario})?> restoreSession() async {
    final token = await _storage.read(key: _tokenKey);
    final userJson = await _storage.read(key: _userKey);

    if (token == null || token.isEmpty || userJson == null || userJson.isEmpty) {
      return null;
    }

    try {
      final usuario = Usuario.fromJson(jsonDecode(userJson) as Map<String, dynamic>);
      return (token: token, usuario: usuario);
    } catch (_) {
      await clear();
      return null;
    }
  }

  static Future<void> updateUser(Usuario usuario) async {
    await _storage.write(key: _userKey, value: jsonEncode(usuario.toJson()));
  }

  static Future<void> clear() async {
    await _storage.delete(key: _tokenKey);
    await _storage.delete(key: _userKey);
  }
}
