class Denuncia {
  final int? idDenuncia;
  final String descricao;
  final DateTime? dataEnvio;
  final String status;
  final int idEvento;

  final int? idUsuarioDenunciante;

  final int? idUsuarioDenunciado;

  Denuncia({
    this.idDenuncia,
    required this.descricao,
    this.dataEnvio,
    this.status = 'PENDENTE',
    required this.idEvento,
    this.idUsuarioDenunciante,
    this.idUsuarioDenunciado,
  });

  factory Denuncia.fromJson(Map<String, dynamic> json) {
    return Denuncia(
      idDenuncia: json['idDenuncia'] as int?,
      descricao: json['descricao'] as String,
      dataEnvio: json['dataEnvio'] != null ? DateTime.tryParse(json['dataEnvio']) : null,
      status: json['status'] as String? ?? 'PENDENTE',
      idEvento: json['idEvento'] as int,
      idUsuarioDenunciante: json['idUsuarioDenunciante'] as int?,
      idUsuarioDenunciado: json['idUsuarioDenunciado'] as int?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'descricao': descricao,
      if (idUsuarioDenunciado != null) 'idUsuarioDenunciado': idUsuarioDenunciado,
    };
  }
}
