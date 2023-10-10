from django.core.management.base import BaseCommand
from tenants.models import Client, Domain
from user.models import User
from decouple import config
import logging

tenant_data = {
        "currency_name": "dollars",
        "currency_code": "USD",
        "currency_symbol": "$",
        "username": "admin"
}

user_data = {
        "first_name": "admin",
        "last_name": "admin",
        "username": "admin",
        "email": "admin@google.com",
        "password": config("admin_password"),
}

class Command(BaseCommand):

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
              '--host',
               action='store',
               dest='host',
               type=str,
               help='Max value'
        )


    def handle(self, *args, **options):
        tenant, created = Client.objects.get_or_create(schema_name="public", **tenant_data)
        
        # Add one or more domains for the tenant
        domain = Domain.objects.get_or_create(
            domain=options['host'], 
            tenant=tenant
        )


        tenant.activate()
        try:                    
            User.objects.create_superuser(user_data.pop('username'), **user_data)
        except Exception as e:
            logging.debug(e)            