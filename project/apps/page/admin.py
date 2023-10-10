from django.contrib import admin
from .models import Section, Title, SectionContent

# Register your models here.
admin.site.register([Section, Title, SectionContent])