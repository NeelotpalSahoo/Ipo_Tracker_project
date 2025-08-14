from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include('ipo_app.urls')),
    path('admin-panel/', include('admin_panel.urls', namespace='admin_panel')), # your admin panel
    # your other paths
    path('auth/', include('social_django.urls', namespace='social')),
    path('', include('ipo_app.urls')),
]

# Add this only when DEBUG is True (for development)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
