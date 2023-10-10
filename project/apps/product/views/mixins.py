from rest_framework.response import Response
from rest_framework.exceptions import ValidationError


class CustomCreateDeleteViewMixin:
    serializer_class = None
    queryset = None
    create_key = None
    
    def post(self, request, *args, **kwargs):
        if 'to_delete' in request.GET:                
            self.delete_images(request.GET.getlist('to_delete'))
        if self.create_key in request.data:                
            self.create_images(request.data)
        return Response(status=201)

    def create_images(self, data):
        serializer = self.serializer_class(data=data, context={"request" : self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def delete_images(self, data : list[int] = None):

        for d in data:
            try:
                int(d)
            except:
                raise ValidationError("to_delete is not a valid list of integers")
        
        self.get_queryset().filter(
            id__in=data
        ).delete()
        
    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(
            product_variant__product__user = self.request.user
        )