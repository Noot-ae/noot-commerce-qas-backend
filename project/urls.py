"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.conf.urls.static import static


schema_view = get_schema_view(
   openapi.Info(
      title="Noot API",
      default_version='1'
   ),
   public=True,
   permission_classes=[AllowAny],
)
        

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('products/', include('product.urls')),
    path('payment/', include('payment.urls')),
    path('translations/', include('translations.urls')),
    path('orders/', include('orders.urls')),
    path('vender/', include('vender.urls')),
    path('tenants/', include('tenants.urls')),
    path('category/', include('category.urls')),
    path('chat/', include('chat.urls')),
    path('rating/', include('rating.urls')),
    path('pages/', include('page.urls')),
    path('gateway/', include('gateway.urls')),
    path('overview/', include('overview.urls')),
    path('blog/', include('blog.urls')),
    
    path('', include('utils.urls')),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0)),

]

urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))] 

urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

