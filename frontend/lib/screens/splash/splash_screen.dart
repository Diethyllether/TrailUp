import 'package:flutter/material.dart';
import '../../core/theme/app_theme.dart';
import '../../services/auth_service.dart';
import '../auth/login_screen.dart';
import '../auth/register_screen.dart';
import '../home/home_screen.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  bool _restoringSession = true;

  @override
  void initState() {
    super.initState();
    _restoreSession();
  }

  Future<void> _restoreSession() async {
    try {
      final usuario = await AuthService.restoreSession();
      if (!mounted) return;
      if (usuario != null) {
        Navigator.pushAndRemoveUntil(
          context,
          MaterialPageRoute(builder: (_) => HomeScreen(usuario: usuario)),
          (route) => false,
        );
        return;
      }
    } catch (_) {
      // If the local session cannot be restored, show the normal auth screen.
    }

    if (mounted) setState(() => _restoringSession = false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.bgDark,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 32),
          child: Column(
            children: [
              const Spacer(flex: 3),
              Container(
                width: 96,
                height: 96,
                decoration: BoxDecoration(
                  color: AppColors.greenLight.withOpacity(0.15),
                  shape: BoxShape.circle,
                ),
                child: const Icon(Icons.terrain_rounded, color: AppColors.greenLight, size: 48),
              ),
              const SizedBox(height: 24),
              const Text(
                'TrailUp',
                style: TextStyle(color: AppColors.textPrimary, fontSize: 36, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 12),
              Text(
                _restoringSession ? 'Restaurando sua sessão...' : 'Sua próxima trilha começa aqui.',
                textAlign: TextAlign.center,
                style: const TextStyle(color: AppColors.textDim, fontSize: 15),
              ),
              const SizedBox(height: 16),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                decoration: BoxDecoration(
                  color: AppColors.green.withOpacity(0.2),
                  borderRadius: BorderRadius.circular(20),
                ),
                child: const Text(
                  '🏕  Conecte. Explore. Evolua.',
                  style: TextStyle(color: AppColors.greenLight, fontSize: 12, fontWeight: FontWeight.w600),
                ),
              ),
              const Spacer(flex: 4),
              if (_restoringSession)
                const Padding(
                  padding: EdgeInsets.only(bottom: 32),
                  child: CircularProgressIndicator(color: AppColors.greenLight),
                )
              else ...[
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                    onPressed: () =>
                        Navigator.push(context, MaterialPageRoute(builder: (_) => const RegisterScreen())),
                    child: const Text('Criar conta'),
                  ),
                ),
                const SizedBox(height: 12),
                SizedBox(
                  width: double.infinity,
                  child: OutlinedButton(
                    style: OutlinedButton.styleFrom(
                      backgroundColor: AppColors.bgCard,
                      foregroundColor: AppColors.greenLight,
                      side: BorderSide.none,
                    ),
                    onPressed: () =>
                        Navigator.push(context, MaterialPageRoute(builder: (_) => const LoginScreen())),
                    child: const Text('Já tenho conta', style: TextStyle(fontWeight: FontWeight.w600)),
                  ),
                ),
                const SizedBox(height: 32),
              ],
            ],
          ),
        ),
      ),
    );
  }
}
