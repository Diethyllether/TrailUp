import 'dart:convert';
import 'package:http/http.dart' as http;
import '../core/config/api_config.dart';

class ApiClient {
  ApiClient._();

  static String? authToken;

  static Map<String, String> get _headers => {
        'Content-Type': 'application/json; charset=UTF-8',
        if (authToken != null) 'Authorization': 'Bearer $authToken',
      };

  static Uri _uri(String endpoint) => Uri.parse('${ApiConfig.baseUrl}$endpoint');

  static Future<dynamic> get(String endpoint) async {
    final res = await http.get(_uri(endpoint), headers: _headers).timeout(ApiConfig.timeout);
    return _handle(res);
  }

  static Future<dynamic> post(String endpoint, Map<String, dynamic> body) async {
    final res = await http
        .post(_uri(endpoint), headers: _headers, body: jsonEncode(body))
        .timeout(ApiConfig.timeout);
    return _handle(res);
  }

  static Future<dynamic> put(String endpoint, Map<String, dynamic> body) async {
    final res = await http
        .put(_uri(endpoint), headers: _headers, body: jsonEncode(body))
        .timeout(ApiConfig.timeout);
    return _handle(res);
  }

  static Future<dynamic> delete(String endpoint) async {
    final res = await http.delete(_uri(endpoint), headers: _headers).timeout(ApiConfig.timeout);
    return _handle(res);
  }

  static dynamic _handle(http.Response res) {
    if (res.statusCode >= 200 && res.statusCode < 300) {
      if (res.body.isEmpty) return null;
      return jsonDecode(utf8.decode(res.bodyBytes));
    }
    throw ApiException(res.statusCode, res.body);
  }
}

class ApiException implements Exception {
  final int statusCode;
  final String body;
  ApiException(this.statusCode, this.body);

  @override
  String toString() => 'ApiException($statusCode): $body';
}
