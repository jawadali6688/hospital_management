from django.shortcuts import redirect

class RoleRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            current_path = request.path

            if current_path in ["/", "/admin/", "/users/login/", "/users/register", "/users/logout/"]:
                return self.get_response(request)

            if current_path.startswith("/admin/") and not request.user.is_superuser:
                return redirect("/users/login/")

            role_redirects = {
                "doctor": "/users/doctor/dashboard",
                "patient": "/users/patient/dashboard",
                "guardian": "/users/guardian/dashboard",
            }

            if request.user.role in role_redirects and not current_path.startswith(role_redirects[request.user.role]):
                return redirect(role_redirects[request.user.role])

        return self.get_response(request)
