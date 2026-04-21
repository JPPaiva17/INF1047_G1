from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('notification/<int:pk>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('admin/', admin.site.urls),
    path('players/', include('players.urls')),
    path('teams/', include('teams.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
