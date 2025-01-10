# dans etudiant/management/commands/send_test_email.py
from django.core.management.base import BaseCommand
from django.core.mail import send_mail

class Command(BaseCommand):
    help = 'Send a test email'

    def handle(self, *args, **kwargs):
        send_mail(
            'Test Subject',
            'This is a test email.',
            'ton.email@kurl.com',  # L'adresse email de l'expéditeur
            ['destinataire@example.com'],  # L'adresse email du destinataire
            fail_silently=False,
        )
        self.stdout.write(self.style.SUCCESS('Test email has been sent!'))
