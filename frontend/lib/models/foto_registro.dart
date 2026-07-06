class FotoRegistro {
  final int? idFotoRegistro;
  final String url;
  final String? legenda;
  final int idRegistro;

  FotoRegistro({
    this.idFotoRegistro,
    required this.url,
    this.legenda,
    required this.idRegistro,
  });

  factory FotoRegistro.fromJson(Map<String, dynamic> json) {
    return FotoRegistro(
      idFotoRegistro: json['idFotoRegistro'] as int?,
      url: json['url'] as String,
      legenda: json['legenda'] as String?,
      idRegistro: json['idRegistro'] as int,
    );
  }

  Map<String, dynamic> toJson() {
    return {'url': url, 'legenda': legenda, 'idRegistro': idRegistro};
  }
}
