from django.urls import include, path
from rest_framework import routers
from users import views
from django.contrib import admin
from users import urls as users_urls
from upload import urls as upload_urls
from reports import urls as report_urls
from dataset import urls as dataset_urls
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [    
    path('admin/', admin.site.urls),    
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('users/', include(users_urls)),
    path('upload/',include(upload_urls)),    
    path('reports/',include(report_urls)),    
    path('dataset/',include(dataset_urls)),    
    # url(r'^upload/(?P<filename>[^/]+)$', FileUploadView.as_view())
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
