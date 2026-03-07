"""
Django management команда для тестирования email-уведомлений.
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from core.notifications import notify_new_order
from orders.models import Order


class Command(BaseCommand):
    help = 'Тестирует отправку email-уведомлений'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('=== Email Configuration Test ===\n'))
        
        # 1. Проверяем настройки
        self.stdout.write(f'EMAIL_BACKEND: {settings.EMAIL_BACKEND}')
        self.stdout.write(f'EMAIL_HOST: {settings.EMAIL_HOST}')
        self.stdout.write(f'EMAIL_PORT: {settings.EMAIL_PORT}')
        self.stdout.write(f'EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}')
        self.stdout.write(f'EMAIL_HOST_USER: {settings.EMAIL_HOST_USER or "❌ НЕ УСТАНОВЛЕНО"}')
        self.stdout.write(f'EMAIL_HOST_PASSWORD: {"✅ Установлено" if settings.EMAIL_HOST_PASSWORD else "❌ НЕ УСТАНОВЛЕНО"}')
        self.stdout.write(f'DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}\n')
        
        # 2. Проверяем, какой backend используется
        if settings.EMAIL_BACKEND == 'django.core.mail.backends.console.EmailBackend':
            self.stdout.write(self.style.ERROR(
                '❌ Используется console backend - письма НЕ отправляются!'
            ))
            self.stdout.write(self.style.WARNING(
                'Добавьте на Railway переменные:\n'
                '  EMAIL_HOST_USER = error04p@gmail.com\n'
                '  EMAIL_HOST_PASSWORD = yylwzszlqrmniixd'
            ))
        else:
            self.stdout.write(self.style.SUCCESS('✅ Используется SMTP backend'))
        
        self.stdout.write('')
        
        # 3. Проверяем получателей
        from users.models import User
        workers = User.objects.filter(role='worker', email__isnull=False).exclude(email='')
        superusers = User.objects.filter(is_superuser=True, email__isnull=False).exclude(email='')
        
        self.stdout.write(f'Работники с email: {workers.count()}')
        for worker in workers:
            self.stdout.write(f'  - {worker.username}: {worker.email}')
        
        self.stdout.write(f'\nАдминистраторы с email: {superusers.count()}')
        for admin in superusers:
            self.stdout.write(f'  - {admin.username}: {admin.email}')
        
        if not workers.exists() and not superusers.exists():
            self.stdout.write(self.style.ERROR(
                '\n❌ Нет получателей с email адресами!'
            ))
            self.stdout.write(self.style.WARNING(
                'Добавьте email пользователю worker в админ-панели'
            ))
            return
        
        self.stdout.write('')
        
        # 4. Тестовая отправка
        if self.confirm_send():
            self.stdout.write('\n--- Отправка тестового уведомления ---')
            
            # Берем первую заявку для теста
            order = Order.objects.first()
            if not order:
                self.stdout.write(self.style.ERROR('❌ Нет заявок для теста'))
                return
            
            self.stdout.write(f'Заявка для теста: #{order.id}')
            
            try:
                result = notify_new_order(order)
                if result:
                    self.stdout.write(self.style.SUCCESS('✅ Email отправлен успешно!'))
                    self.stdout.write('Проверьте почту получателей (включая папку Спам)')
                else:
                    self.stdout.write(self.style.ERROR('❌ Email не отправлен'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Ошибка: {e}'))
    
    def confirm_send(self):
        """Спрашивает подтверждение перед отправкой."""
        if settings.EMAIL_HOST_USER:
            answer = input('\nОтправить тестовое уведомление? (y/n): ')
            return answer.lower() in ['y', 'yes', 'д', 'да']
        return False
