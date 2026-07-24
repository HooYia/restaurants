from celery import shared_task

from .models import User


@shared_task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()

@shared_task()
def send_new_order_admin_notification_task(order_id):
    from restaurants.meal.models import Order
    from restaurants.users.utils.emails import EmailUtil
    try:
        order = Order.objects.get(id=order_id)
        EmailUtil().send_new_order_admin_notification(order)
    except Order.DoesNotExist:
        pass

@shared_task()
def send_order_status_update_task(order_id):
    from restaurants.meal.models import Order
    from restaurants.users.utils.emails import EmailUtil
    try:
        order = Order.objects.get(id=order_id)
        EmailUtil().send_order_status_update(order)
    except Order.DoesNotExist:
        pass
