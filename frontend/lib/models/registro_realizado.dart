class RegistroRealizado {
  final int? idRegistro;
  final double latitude;
  final double longitude;
  final DateTime? horario;
  final String? observacao;
  final int idHistorico;

  RegistroRealizado({
    this.idRegistro,
    required this.latitude,
    required this.longitude,
    this.horario,
    this.observacao,
    required this.idHistorico,
  });

  factory RegistroRealizado.fromJson(Map<String, dynamic> json) {
    return RegistroRealizado(
      idRegistro: json['idRegistro'] as int?,
      latitude: (json['latitude'] as num).toDouble(),
      longitude: (json['longitude'] as num).toDouble(),
      horario: json['horario'] != null ? DateTime.tryParse(json['horario']) : null,
      observacao: json['observacao'] as String?,
      idHistorico: json['idHistorico'] as int,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'latitude': latitude,
      'longitude': longitude,
      'horario': horario?.toIso8601String(),
      'observacao': observacao,
      'idHistorico': idHistorico,
    };
  }
}
