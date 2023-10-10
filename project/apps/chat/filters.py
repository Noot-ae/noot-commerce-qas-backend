import django_filters
from django.db.models import Q


class ChatFilter(django_filters.FilterSet):
    user = django_filters.NumberFilter(method='other_user_filter')


    def other_user_filter(self, qs, name, remote_user_id):

        if not remote_user_id: return qs
        
        return qs.filter(
            Q(
                Q(
                    sender=self.request.user, receiver_id = remote_user_id
                    
                ) | Q(
                        receiver=self.request.user,
                        sender_id=remote_user_id
                    )
            )
        )
