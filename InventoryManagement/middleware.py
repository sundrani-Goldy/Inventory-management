from django.db.utils import DatabaseError
from django.http import HttpResponseForbidden
from django.template import loader
from django_tenants.middleware.main import TenantMainMiddleware


class CustomTenantMiddleware(TenantMainMiddleware):
    def get_tenant(self, domain_model, hostname):
        tenant = super().get_tenant(domain_model, hostname)
        if not tenant.is_active:
            raise DatabaseError("Tenant is inactive")
        return tenant

    def process_request(self, request):
        try:
            return super().process_request(request)
        except DatabaseError as e:
            if "Tenant is inactive" in str(e):
                html_message = loader.render_to_string('inactive.html')
                return HttpResponseForbidden(html_message)
            raise
            