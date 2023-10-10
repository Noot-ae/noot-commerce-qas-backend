from .models import Client, Domain
from django.contrib import admin
from django_tenants.utils import get_public_schema_name


class TenantsAdmin(admin.ModelAdmin):
    
    def is_public_schema(self, request):
        return request.tenant.schema_name == get_public_schema_name()
    
    def has_view_permission(self,request, view=None):
        return self.is_public_schema(request)
    
    def has_add_permission(self,request, view=None):
        return self.is_public_schema(request)
    
    def has_change_permission(self,request, view=None):
        return self.is_public_schema(request)
    
    def has_delete_permission(self,request, view=None):
        return self.is_public_schema(request)
    
    def has_view_or_change_permission(self, request, view=None):
        return self.is_public_schema(request)

    
for model in [Client, Domain]:
    admin.site.register(model, TenantsAdmin)