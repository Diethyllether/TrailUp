enum TipoEvento { individual, grupo }

extension TipoEventoX on TipoEvento {
  String get valor => this == TipoEvento.individual ? 'INDIVIDUAL' : 'GRUPO';

  static TipoEvento fromString(String? value) {
    return value == 'INDIVIDUAL' ? TipoEvento.individual : TipoEvento.grupo;
  }
}

class Evento {
  final int? idEvento;
  final String titulo;
  final String? descricao;
  final DateTime? data;
  final DateTime? horarioSaida;
  final bool imediata;
  final int? vagas;
  final TipoEvento tipo;
  final double? latitude;
  final double? longitude;
  final int idCriador;

  final List<int>? trilhasIds;
  final int? participantesAtuais;
  final String? nomeCriador;
  final String? dificuldadeTrilha;

  Evento({
    this.idEvento,
    required this.titulo,
    this.descricao,
    this.data,
    this.horarioSaida,
    this.imediata = false,
    this.vagas,
    this.tipo = TipoEvento.grupo,
    this.latitude,
    this.longitude,
    required this.idCriador,
    this.trilhasIds,
    this.participantesAtuais,
    this.nomeCriador,
    this.dificuldadeTrilha,
  });

  factory Evento.fromJson(Map<String, dynamic> json) {
    return Evento(
      idEvento: json['idEvento'] as int?,
      titulo: json['titulo'] as String,
      descricao: json['descricao'] as String?,
      data: json['data'] != null ? DateTime.tryParse(json['data']) : null,
      horarioSaida:
          json['horarioSaida'] != null ? DateTime.tryParse(json['horarioSaida']) : null,
      imediata: json['imediata'] as bool? ?? false,
      vagas: json['vagas'] as int?,
      tipo: TipoEventoX.fromString(json['tipo'] as String?),
      latitude: (json['latitude'] as num?)?.toDouble(),
      longitude: (json['longitude'] as num?)?.toDouble(),
      idCriador: json['idCriador'] as int,
      trilhasIds: json['trilhasIds'] != null ? List<int>.from(json['trilhasIds']) : null,
      participantesAtuais: json['participantesAtuais'] as int?,
      nomeCriador: json['nomeCriador'] as String?,
      dificuldadeTrilha: json['dificuldadeTrilha'] as String?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'titulo': titulo,
      'descricao': descricao,
      'data': data?.toIso8601String(),
      'horarioSaida': horarioSaida?.toIso8601String(),
      'imediata': imediata,
      'vagas': vagas,
      'tipo': tipo.valor,
      'latitude': latitude,
      'longitude': longitude,
    };
  }

  String get vagasFormatadas => '${participantesAtuais ?? 0}/${vagas ?? '-'}';
}
