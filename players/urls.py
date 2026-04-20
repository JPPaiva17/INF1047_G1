from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot_password/', views.forgot_password_view, name='forgot_password'),
    path('list/', views.players_list_view, name='players_list'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
]