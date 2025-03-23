from django.shortcuts import redirect

class RoleRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            current_path = request.path

            # Allowed common paths
            allowed_paths = ["/", "/admin/", "/users/login/", "/users/register", "/users/logout/"]
            if current_path in allowed_paths:
                return self.get_response(request)

            # Restrict access to the Django admin panel for non-superusers
            if current_path.startswith("/admin/") and not request.user.is_superuser:
                return redirect("/users/login/")

            # Define role-based allowed URL prefixes
            role_prefixes = {
                "doctor": "/users/doctor/dashboard",
                "patient": "/users/patient/dashboard",
                "guardian": "/users/guardian/dashboard",
            }

            # Special case: Allow doctors and guardians to access patient URLs
            if request.user.role in ["doctor", "guardian"] and current_path.startswith("/users/patient/"):
                return self.get_response(request)

            # Check if the user is accessing an allowed section
            if request.user.role in role_prefixes:
                allowed_prefix = role_prefixes[request.user.role]

                # Redirect only if the user is trying to access a different role's section
                if not current_path.startswith(allowed_prefix):
                    return redirect(allowed_prefix)

        return self.get_response(request)
