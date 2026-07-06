class Avaliacao {
  final int? idAvaliacao;
  final int nota;
  final String? comentario;
  final DateTime? data;
  final int idUsuario;
  final int idTrilha;

  final String? nomeUsuario;

  Avaliacao({
    this.idAvaliacao,
    required this.nota,
    this.comentario,
    this.data,
    required this.idUsuario,
    required this.idTrilha,
    this.nomeUsuario,
  });

  factory Avaliacao.fromJson(Map<String, dynamic> json) {
    return Avaliacao(
      idAvaliacao: json['idAvaliacao'] as int?,
      nota: json['nota'] as int,
      comentario: json['comentario'] as String?,
      data: json['data'] != null ? DateTime.tryParse(json['data']) : null,
      idUsuario: json['idUsuario'] as int,
      idTrilha: json['idTrilha'] as int,
      nomeUsuario: json['nomeUsuario'] as String?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'nota': nota,
      'comentario': comentario,
      'idUsuario': idUsuario,
      'idTrilha': idTrilha,
    };
  }
}
