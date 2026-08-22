# TrailUp — App Flutter (Base)

Scaffold completo do frontend do TrailUp, pronto para conectar em uma API
Flask separada. Os `services/*.dart` concentram as chamadas HTTP nos
contratos descritos abaixo.

## Como rodar

```bash
flutter pub get
flutter run
```

Antes de rodar contra um backend real, edite a URL base em:

```
lib/core/config/api_config.dart
```

## Estrutura

```
lib/
  core/
    config/api_config.dart
    theme/app_theme.dart
  models/
  services/
  screens/
  widgets/
  main.dart
```

## Telas incluídas

| Tela | Requisitos atendidos |
|---|---|
| Splash / Onboarding | — |
| Login / Cadastro | cadastro, login, recuperação de senha |
| Home (Descobrir) | busca, filtro por dificuldade, trilhas em destaque, expedições ativas |
| Detalhe da Trilha | distância/duração/dificuldade, checkpoints, avaliações, eventos, mapa offline |
| Mapa & Expedições | expedições abertas perto do usuário, reportar comportamento inadequado |
| Perfil | edição de perfil, histórico de trilhas, notificações, logout |

## Pontos de integração com o Flask

Toda chamada de API está isolada em `lib/services/*.dart`. Segue o contrato
esperado (todos em JSON, seguindo `create_database.sql`):

| Método | Endpoint | Service |
|---|---|---|
| POST | `/login` | `auth_service.dart` |
| POST | `/usuarios` | `auth_service.dart` |
| POST | `/recuperar-senha` | `auth_service.dart` |
| PUT | `/usuarios/<idUsuario>` | `auth_service.dart` |
| GET | `/trilhas?busca=&dificuldade=` | `trilha_service.dart` |
| GET | `/trilhas/<idTrilha>` | `trilha_service.dart` |
| GET | `/trilhas/<idTrilha>/avaliacoes` | `trilha_service.dart` |
| POST | `/avaliacoes` | `trilha_service.dart` |
| GET | `/trilhas/<idTrilha>/fotos` | `trilha_service.dart` |
| GET | `/trilhas/<idTrilha>/checkpoints` | `checkpoint_service.dart` |
| POST | `/checkpoints` | `checkpoint_service.dart` |
| POST | `/trilhas/<idTrilha>/mapa-offline` | `checkpoint_service.dart` |
| GET | `/eventos?lat=&lng=` | `evento_service.dart` |
| GET | `/trilhas/<idTrilha>/eventos` | `evento_service.dart` |
| POST | `/eventos` | `evento_service.dart` |
| POST | `/eventos/<idEvento>/participantes` | `evento_service.dart` |
| GET | `/usuarios/<idUsuario>/historico` | `historico_service.dart` |
| POST | `/historico` | `historico_service.dart` |
| POST | `/registros` | `historico_service.dart` |
| GET | `/usuarios/<idUsuario>/notificacoes` | `notificacao_service.dart` |
| PUT | `/notificacoes/<idNotificacao>` | `notificacao_service.dart` |
| POST | `/denuncias` | `denuncia_service.dart` |

Todas as URLs acima são relativas a `ApiConfig.baseUrl` (ex:
`http://10.0.2.2:5000/api`), definido em `lib/core/config/api_config.dart`.

## Integrações pendentes

- **`screens/map/map_screen.dart`** e **`widgets/trail_map_widget.dart`** usam
  `flutter_map` com tiles de satélite Esri (World Imagery). Requer conexão
  com a internet. O botão no canto superior direito alterna satélite / ruas
  (OpenStreetMap).
- **`screens/trilha/trilha_detail_screen.dart`** — o botão "Iniciar Trilha"
  registra um checkpoint com coordenadas placeholder `(0.0, 0.0)`. Adicione
  um pacote de geolocalização (ex: `geolocator`) para capturar a posição real
  do dispositivo.

## Dependências

Apenas `http` (chamadas REST) e `intl` (formatação de data) além do padrão
Flutter — sem gerenciamento de estado externo (Provider/Riverpod/Bloc) para
manter o scaffold simples de entender e estender.
