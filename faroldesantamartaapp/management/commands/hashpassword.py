from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Generates a hashed password from a plain text password'

    def add_arguments(self, parser):
        parser.add_argument('password', type=str, help='The plain text password to hash')

    def handle(self, *args, **options):
        password = options['password']
        hashed_password = make_password(password)
        self.stdout.write(self.style.SUCCESS(f'Hashed Password: {hashed_password}'))
