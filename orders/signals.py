from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, OrderItem


@receiver(post_save, sender=OrderItem)
def order_item_saved(sender, instance, **kwargs):
    """
    Signal to update the total price of the order when an order item is saved.
    """
    order = instance.order
    order.total_price = sum(item.get_cost() for item in order.items.all())
    order.save()


@receiver(post_save, sender=Order)
def order_saved(sender, instance, **kwargs):
    """
    Signal to update the total price of the order when an order is saved.
    """
    instance.total_price = sum(item.get_cost() for item in instance.items.all())
    instance.save()
