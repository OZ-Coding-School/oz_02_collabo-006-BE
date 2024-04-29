from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates a superuser with predefined credentials'

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'admin'
        phone = '1234567890'  # 예시 전화번호

        # 전화번호가 이미 존재하는지 확인
        if User.objects.filter(phone=phone).exists():
            self.stdout.write(self.style.WARNING(f'A user with phone {phone} already exists'))
        else:
            # 존재하지 않는 경우에만 사용자 생성
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(username, 'admin@example.com', '1234', phone=phone)
                self.stdout.write(self.style.SUCCESS('Successfully created a new superuser'))
            else:
                self.stdout.write(self.style.WARNING('A superuser with this username already exists'))
