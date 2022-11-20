import sys


def update_balance(sender, instance, created, **kwargs):
    if 'migrate' in sys.argv:
        return

    if hasattr(instance, '_dirty'):
        return

    balance = instance.balance
    if instance.type == 0:
        balance.amount -= instance.amount
    elif instance.type == 1:
        balance.amount += instance.amount
    balance.save()
