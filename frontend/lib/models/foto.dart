class Foto {
  final int? idFoto;
  final String url;
  final String? legenda;
  final int idTrilha;

  Foto({this.idFoto, required this.url, this.legenda, required this.idTrilha});

  factory Foto.fromJson(Map<String, dynamic> json) {
    return Foto(
      idFoto: json['idFoto'] as int?,
      url: json['url'] as String,
      legenda: json['legenda'] as String?,
      idTrilha: json['idTrilha'] as int,
    );
  }

  Map<String, dynamic> toJson() {
    return {'url': url, 'legenda': legenda, 'idTrilha': idTrilha};
  }
}
