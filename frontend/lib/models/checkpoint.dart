class Checkpoint {
  final int? idCheckpoint;
  final double latitude;
  final double longitude;
  final DateTime? horario;
  final int idTrilha;

  Checkpoint({
    this.idCheckpoint,
    required this.latitude,
    required this.longitude,
    this.horario,
    required this.idTrilha,
  });

  factory Checkpoint.fromJson(Map<String, dynamic> json) {
    return Checkpoint(
      idCheckpoint: json['idCheckpoint'] as int?,
      latitude: (json['latitude'] as num).toDouble(),
      longitude: (json['longitude'] as num).toDouble(),
      horario: json['horario'] != null ? DateTime.tryParse(json['horario']) : null,
      idTrilha: json['idTrilha'] as int,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'latitude': latitude,
      'longitude': longitude,
      'horario': horario?.toIso8601String(),
      'idTrilha': idTrilha,
    };
  }
}
