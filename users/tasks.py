from celery import shared_task
from django.utils.timezone import now
from .models import TemporaryRole

@shared_task
def revoke_expired_roles():
    expired_roles = TemporaryRole.objects.filter(expires_at__lte=now())
    for role in expired_roles:
        role.user.groups.remove(role.role)  # Role remove karein
        role.delete()  # Entry delete karein
# from celery.schedules import crontab
# from celery import Celery
# from .tasks import revoke_expired_roles

# app = Celery('hospital_portal2')

# app.conf.beat_schedule = {
#     'auto-revoke-temporary-roles': {
#         'task': 'users.tasks.revoke_expired_roles',
#         'schedule': crontab(minute='*/5'),  # Har 5 min baad chale ga
#     },
# }
