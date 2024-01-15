from django.contrib import admin
from django.urls import path, include, re_path

from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rentalapp.views.home import handle_unmatched
from django.views.generic import TemplateView

handler404 = 'rentalapp.views.home.handle_unmatched'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("rentalapp.urls")),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('<str:unmatched_path>/', handle_unmatched, name='handle_unmatched'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

urlpatterns += [re_path(r'^.*$', TemplateView.as_view(template_name='frontend/not_found.html'), name='not_found')]
