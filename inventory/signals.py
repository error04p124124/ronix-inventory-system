"""
Сигналы для приложения inventory.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Component


@receiver(post_save, sender=Component)
def check_low_stock(sender, instance, created, **kwargs):
    """
    Проверка низкого остатка при изменении комплектующей.
    """
    # Не проверяем при создании нового товара
    if created:
        return
    
    # Здесь можно добавить другую логику при достижении минимального остатка
    # if instance.quantity <= instance.min_quantity:
    #     pass
