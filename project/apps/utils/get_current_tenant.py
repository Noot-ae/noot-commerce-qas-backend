from django.db import connection

def get_current_tenant():
    return connection.tenant