class MapaOffline {
  final int? idMapa;
  final String arquivoUrl;
  final double? tamanhoArquivo;
  final DateTime? dataDownload;
  final int idTrilha;

  MapaOffline({
    this.idMapa,
    required this.arquivoUrl,
    this.tamanhoArquivo,
    this.dataDownload,
    required this.idTrilha,
  });

  factory MapaOffline.fromJson(Map<String, dynamic> json) {
    return MapaOffline(
      idMapa: json['idMapa'] as int?,
      arquivoUrl: json['arquivoUrl'] as String? ?? '',
      tamanhoArquivo: (json['tamanhoArquivo'] as num?)?.toDouble(),
      dataDownload:
          json['dataDownload'] != null ? DateTime.tryParse(json['dataDownload']) : null,
      idTrilha: json['idTrilha'] as int,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'arquivoUrl': arquivoUrl,
      'tamanhoArquivo': tamanhoArquivo,
      'idTrilha': idTrilha,
    };
  }
}
