import django_filters 
from django.db.models import Q
from user.models import User, Region, ShipmentProfile
from django.forms import CharField

class RegionNameFilter(django_filters.CharFilter):
    field_class = CharField

    def filter(self, qs, value):
        if not value: return qs
        return qs.filter(name__text__icontainss = value).distinct()
    

class UserMailFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(lookup_expr='icontainss')

    class Meta:
        model = User
        fields = ['email']


class CustomFKFilter(django_filters.Filter):
    def filter(self, queryset, value):
        if bool(value) and value != "-1":
            value = True
        elif value == "-1":
            return queryset
        else:
            value = False
        kwargs = {f"parent_region__isnull": value}
        return queryset.filter(**kwargs)


class RegionsFilter(django_filters.FilterSet):
    parent_region__isnull = CustomFKFilter()
    name = RegionNameFilter()
    
    class Meta:
        model = Region
        fields = ['parent_region__isnull', 'parent_region', 'name']


class ProfileFilter(django_filters.FilterSet):
    
    class ProfileFilter(django_filters.CharFilter):
        def filter(self, qs, value):
            if not value: return qs
            qs = qs.filter(
                Q(
                    Q(
                        Q(email__icontains=value) | Q(first_name__icontains=value) | Q(last_name__icontains=value) | Q(phone_number__phone__icontains=value)
                    )
                    |
                    Q(
                        Q(user__email__icontains=value) | Q(user__first_name__icontains=value) | Q(user__last_name__icontains=value)
                    )
                )
            ).distinct('id').order_by('id')
            return qs
    
    q = ProfileFilter()

    class Meta:
        model = ShipmentProfile
        fields = ['q']


class UserListFilter(django_filters.FilterSet):
    
    class UserFilter(django_filters.CharFilter):
        def filter(self, qs, value):
            if not value: return qs
            qs = qs.filter(
                Q(
                        Q(email__icontains=value) | Q(first_name__icontains=value) | Q(last_name__icontains=value) | Q(username__icontains=value) | Q(user_phone_set__phone__icontains=value)
                )
            ).distinct('id').order_by('id')
            return qs
    
    q = UserFilter()

    class Meta:
        model = User
        fields = ['q', "username", "email", "is_blocked", "is_active"]

