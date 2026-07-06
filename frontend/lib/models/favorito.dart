class Favorito {
  final int? idFavorito;
  final DateTime? dataSalvo;
  final int idUsuario;
  final int idTrilha;

  Favorito({
    this.idFavorito,
    this.dataSalvo,
    required this.idUsuario,
    required this.idTrilha,
  });

  factory Favorito.fromJson(Map<String, dynamic> json) {
    return Favorito(
      idFavorito: json['idFavorito'] as int?,
      dataSalvo: json['dataSalvo'] != null ? DateTime.tryParse(json['dataSalvo']) : null,
      idUsuario: json['idUsuario'] as int,
      idTrilha: json['idTrilha'] as int,
    );
  }
}
