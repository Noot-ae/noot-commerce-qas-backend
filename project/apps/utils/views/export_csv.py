import csv
from rest_framework.exceptions import ValidationError
from django.http import HttpResponse
from user.models import User
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.serializers import Serializer

class ExportView(GenericAPIView):
    serializer_class = Serializer
    permission_classes = (IsAdminUser,)
    
    models = {
        "users" : {
            "queryset" : User.objects.annotate(*User.export_annotations).values(*User.export_fields),
            "filterset_fields" : User.export_fields,
        }
    }
    
    def is_valid_key(self, key = None):
        if not key in self.models:
            raise ValidationError("model query parameter is not valid")
        return True

    @property
    def model_key(self):
        return self.request.GET.get("model")
    
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        self.is_valid_key(self.model_key)
        self.set_queryset(self.model_key)
        qs = self.filter_queryset(self.get_queryset())
        self.write_rows(response, qs)
        return response
    
    def set_queryset(self, key):
        model_object = self.models[key]
        self.queryset = model_object['queryset']
        self.filterset_fields = model_object['filterset_fields']
        
    def get_model(self):
        return self.models[self.model_key]['queryset'].model
        
    def write_rows(self, response, queryset):
        writer = csv.writer(response)
        writer.writerow(self.get_model().export_fields)
        for object in queryset:
            row = [str(value) for value in object.values()]
            writer.writerow(row)