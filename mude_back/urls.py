from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from mude_back import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mart.urls')),
    path('', include('orders.urls')),
    path('', include('customers.urls')),
    path('', include('notifications.urls')),
    path('', include('notifications.urls')),
    path('', include('admin.urls')),

    # path('', TemplateView.as_view(template_name='index.html')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
