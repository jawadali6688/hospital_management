from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver

@receiver(post_migrate)
def create_roles_and_permissions(sender, **kwargs):
    if sender.name == "users":
        roles = {
            "Super Admin": [],
            "Portal Admin": ["add_user", "change_user", "delete_user", "view_user"],
            "Doctor": ["view_patient", "add_note", "view_note"],
            "Guardian": ["view_patient"],
        }
        
        for role, perms in roles.items():
            group, created = Group.objects.get_or_create(name=role)
            for perm_codename in perms:
                permission = Permission.objects.filter(codename=perm_codename).first()
                if permission:
                    group.permissions.add(permission)
