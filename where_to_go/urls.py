from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from where_to_go.views import place_detail, show_map

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('', show_map),
    path('places/<int:place_id>/', place_detail, name='place-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
