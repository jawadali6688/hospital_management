from django.core.management.base import BaseCommand
from users.models import TemporaryRole
from django.utils.timezone import now

class Command(BaseCommand):
    help = "Revoke expired temporary roles"

    def handle(self, *args, **kwargs):
        expired_roles = TemporaryRole.objects.filter(expires_at__lte=now())
        for role in expired_roles:
            role.user.groups.remove(role.role)  # Role remove karo
            role.delete()  # Entry delete karo
            print(f"Revoked {role.role} from {role.user.username}")
