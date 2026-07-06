import 'package:flutter/material.dart';
import '../../core/theme/app_theme.dart';
import '../../services/auth_service.dart';
import '../home/home_screen.dart';
import 'register_screen.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _emailController = TextEditingController();
  final _senhaController = TextEditingController();
  bool _loading = false;
  String? _erro;

  Future<void> _entrar() async {
    setState(() {
      _loading = true;
      _erro = null;
    });
    try {
      final usuario = await AuthService.login(_emailController.text.trim(), _senhaController.text);
      if (!mounted) return;
      Navigator.pushAndRemoveUntil(
        context,
        MaterialPageRoute(builder: (_) => HomeScreen(usuario: usuario)),
        (route) => false,
      );
    } catch (e) {
      setState(() => _erro = 'Não foi possível entrar. Verifique suas credenciais.');
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  void _abrirRecuperarSenha() {
    final controller = TextEditingController(text: _emailController.text);
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: AppColors.bgCard,
        title: const Text('Recuperar senha', style: TextStyle(color: AppColors.textPrimary)),
        content: TextField(
          controller: controller,
          style: const TextStyle(color: AppColors.textPrimary),
          decoration: const InputDecoration(hintText: 'Seu e-mail cadastrado'),
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Cancelar')),
          TextButton(
            onPressed: () async {
              await AuthService.recuperarSenha(controller.text.trim());
              if (ctx.mounted) Navigator.pop(ctx);
            },
            child: const Text('Enviar'),
          ),
        ],
      ),
    );
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
                'Bem-vindo de volta',
                style: TextStyle(color: AppColors.textPrimary, fontSize: 26, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 6),
              const Text('Entre para continuar suas trilhas.', style: TextStyle(color: AppColors.textDim)),
              const SizedBox(height: 32),
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
              Align(
                alignment: Alignment.centerRight,
                child: TextButton(
                  onPressed: _abrirRecuperarSenha,
                  child: const Text('Esqueci minha senha',
                      style: TextStyle(color: AppColors.greenLight, fontSize: 12)),
                ),
              ),
              if (_erro != null) ...[
                const SizedBox(height: 8),
                Text(_erro!, style: const TextStyle(color: AppColors.red, fontSize: 12)),
              ],
              const SizedBox(height: 16),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _loading ? null : _entrar,
                  child: _loading
                      ? const SizedBox(
                          height: 18,
                          width: 18,
                          child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                      : const Text('Entrar'),
                ),
              ),
              const SizedBox(height: 20),
              Center(
                child: TextButton(
                  onPressed: () => Navigator.pushReplacement(
                      context, MaterialPageRoute(builder: (_) => const RegisterScreen())),
                  child: const Text.rich(
                    TextSpan(
                      text: 'Não tem conta? ',
                      style: TextStyle(color: AppColors.textDim),
                      children: [
                        TextSpan(
                            text: 'Criar agora',
                            style: TextStyle(color: AppColors.greenLight, fontWeight: FontWeight.bold)),
                      ],
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
