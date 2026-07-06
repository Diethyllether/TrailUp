class HistoricoTrilha {
  final int? idHistorico;
  final DateTime? dataRealizacao;
  final double? tempo;
  final int? avaliacaoPessoal;

  final int? idUsuario;
  final int? idEvento;
  final int idTrilha;

  final String? nomeTrilha;

  HistoricoTrilha({
    this.idHistorico,
    this.dataRealizacao,
    this.tempo,
    this.avaliacaoPessoal,
    this.idUsuario,
    this.idEvento,
    required this.idTrilha,
    this.nomeTrilha,
  });

  factory HistoricoTrilha.fromJson(Map<String, dynamic> json) {
    return HistoricoTrilha(
      idHistorico: json['idHistorico'] as int?,
      dataRealizacao:
          json['dataRealizacao'] != null ? DateTime.tryParse(json['dataRealizacao']) : null,
      tempo: (json['tempo'] as num?)?.toDouble(),
      avaliacaoPessoal: json['avaliacaoPessoal'] as int?,
      idUsuario: json['idUsuario'] as int?,
      idEvento: json['idEvento'] as int?,
      idTrilha: json['idTrilha'] as int,
      nomeTrilha: json['nomeTrilha'] as String?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'dataRealizacao': dataRealizacao?.toIso8601String(),
      'tempo': tempo,
      'avaliacaoPessoal': avaliacaoPessoal,
      if (idEvento != null) 'idEvento': idEvento,
      'idTrilha': idTrilha,
    };
  }
}
