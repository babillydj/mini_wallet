import sys

from django.apps import apps


def create_wallet(sender, instance, created, **kwargs):
    if 'migrate' in sys.argv:
        return

    if hasattr(instance, '_dirty'):
        return

    Balance = apps.get_model('wallet', 'Balance')
    Balance.objects.create(
        customer=instance
    )
