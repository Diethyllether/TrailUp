import 'package:flutter/material.dart';
import '../../core/theme/app_theme.dart';
import '../auth/login_screen.dart';
import '../auth/register_screen.dart';

class SplashScreen extends StatelessWidget {
  const SplashScreen({super.key});

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
              const Text(
                'Sua próxima trilha começa aqui.',
                textAlign: TextAlign.center,
                style: TextStyle(color: AppColors.textDim, fontSize: 15),
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
          ),
        ),
      ),
    );
  }
}
