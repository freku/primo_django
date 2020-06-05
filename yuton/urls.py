from django.contrib import admin
from django.urls import path, include
from blogs.views import ProfileView
from django.conf import settings
from django.conf.urls.static import static
from blogs.views import RegisterView

urlpatterns = [
    path('', include('main.urls')),
    path('v/', include('blogs.urls')),
    path('admin/', admin.site.urls),
    path('acc/', include('django.contrib.auth.urls')),
    path('acc/profile/<slug:slug>', ProfileView.as_view(), name='profile-view'),
    path('acc/register', RegisterView.as_view(), name='register-view'),
    path('summernote/', include('django_summernote.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)