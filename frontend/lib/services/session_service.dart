import 'dart:convert';

import 'package:shared_preferences/shared_preferences.dart';

import '../models/usuario.dart';

class SessionService {
  SessionService._();

  static const _tokenKey = 'trailup_auth_token';
  static const _userKey = 'trailup_auth_user';

  static Future<void> saveSession({
    required String token,
    required Usuario usuario,
  }) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_tokenKey, token);
    await prefs.setString(_userKey, jsonEncode(usuario.toJson()));
  }

  static Future<({String token, Usuario usuario})?> restoreSession() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString(_tokenKey);
    final userJson = prefs.getString(_userKey);

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
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_userKey, jsonEncode(usuario.toJson()));
  }

  static Future<void> clear() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_tokenKey);
    await prefs.remove(_userKey);
  }
}
