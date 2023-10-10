from datetime import datetime
from django.db.models.query import QuerySet

class BaseChartMixin:
    def is_pre_available(self):
        self.raw_date_1 = self.request.GET.get('created_at_before')
        self.raw_date_2 = self.request.GET.get('created_at_after')
        return all((self.raw_date_1, self.raw_date_2))
    
    def filter_pre_queryset(self, queryset : QuerySet):
        filter_kwargs = self.get_pre_dates_filter_kwargs()
        queryset = queryset.filter(**filter_kwargs)
        return queryset
    
    def get_pre_dates_filter_kwargs(self, date_filter_key = "created_at"):
        date_1 = self.convert_string_to_date(self.raw_date_1)
        date_2 = self.convert_string_to_date(self.raw_date_2)
        kwargs = {}
        kwargs[f'{date_filter_key}__gte'] = self.get_dates_difference(date_1, self.get_dates_difference(date_1, date_2))
        kwargs[f'{date_filter_key}__lte'] = date_1
        return kwargs

    def convert_string_to_date(self, date_string : str):
        date_format = "%Y-%m-%d"
        date_obj = datetime.strptime(date_string, date_format)
        return date_obj
    
    def get_dates_difference(self, date_1 : datetime, date_2):
        return date_1 - date_2
    