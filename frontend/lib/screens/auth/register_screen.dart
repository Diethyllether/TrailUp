import 'package:flutter/material.dart';
import '../../core/theme/app_theme.dart';
import '../../models/usuario.dart';
import '../../services/auth_service.dart';
import '../home/home_screen.dart';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final _nomeController = TextEditingController();
  final _emailController = TextEditingController();
  final _senhaController = TextEditingController();
  bool _loading = false;
  String? _erro;

  Future<void> _criarConta() async {
    setState(() {
      _loading = true;
      _erro = null;
    });
    try {
      final novoUsuario = Usuario(
        nome: _nomeController.text.trim(),
        email: _emailController.text.trim(),
        senha: _senhaController.text,
      );
      await AuthService.cadastrar(novoUsuario);
      final usuario = await AuthService.login(_emailController.text.trim(), _senhaController.text);
      if (!mounted) return;
      Navigator.pushAndRemoveUntil(
        context,
        MaterialPageRoute(builder: (_) => HomeScreen(usuario: usuario)),
        (route) => false,
      );
    } catch (e) {
      setState(() => _erro = 'Não foi possível criar a conta. Tente novamente.');
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.bgDark,
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              IconButton(
                onPressed: () => Navigator.pop(context),
                icon: const Icon(Icons.arrow_back, color: AppColors.textPrimary),
              ),
              const SizedBox(height: 8),
              const Text(
                'Criar conta',
                style: TextStyle(color: AppColors.textPrimary, fontSize: 26, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 6),
              const Text('Junte-se à comunidade TrailUp.', style: TextStyle(color: AppColors.textDim)),
              const SizedBox(height: 32),
              TextField(
                controller: _nomeController,
                style: const TextStyle(color: AppColors.textPrimary),
                decoration: const InputDecoration(
                  hintText: 'Nome completo',
                  prefixIcon: Icon(Icons.person_outline, color: AppColors.textDim),
                ),
              ),
              const SizedBox(height: 16),
              TextField(
                controller: _emailController,
                style: const TextStyle(color: AppColors.textPrimary),
                decoration: const InputDecoration(
                  hintText: 'E-mail',
                  prefixIcon: Icon(Icons.email_outlined, color: AppColors.textDim),
                ),
              ),
              const SizedBox(height: 16),
              TextField(
                controller: _senhaController,
                obscureText: true,
                style: const TextStyle(color: AppColors.textPrimary),
                decoration: const InputDecoration(
                  hintText: 'Senha',
                  prefixIcon: Icon(Icons.lock_outline, color: AppColors.textDim),
                ),
              ),
              if (_erro != null) ...[
                const SizedBox(height: 12),
                Text(_erro!, style: const TextStyle(color: AppColors.red, fontSize: 12)),
              ],
              const SizedBox(height: 24),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _loading ? null : _criarConta,
                  child: _loading
                      ? const SizedBox(
                          height: 18,
                          width: 18,
                          child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                      : const Text('Criar conta'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
