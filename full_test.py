import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.core.management import call_command
from django.conf import settings

if __name__ == '__main__':
    for app in settings.PROJECT_APPS:
        if "." in app:
            app = app.split(".")[0]
        print(f"============ starting test for app {app} ============")
        call_command("test", app, no_input=True)
