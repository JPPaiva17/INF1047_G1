from django.urls import path
from . import views

urlpatterns = [
    path('', views.team_list, name='team_list'),
    path('create/', views.team_create, name='team_create'),
    path('invites/', views.my_invites, name='my_invites'),
    path('invite/<int:player_pk>/', views.invite_player, name='invite_player'),
    path('invite/<int:invite_pk>/respond/', views.respond_invite, name='respond_invite'),
    path('request/<int:req_pk>/respond/', views.respond_request, name='respond_request'),
    path('<int:pk>/', views.team_detail, name='team_detail'),
    path('<int:pk>/manage/', views.team_manage, name='team_manage'),
    path('<int:pk>/set-role/', views.owner_set_role, name='owner_set_role'),
    path('<int:pk>/edit/', views.team_edit, name='team_edit'),
    path('<int:pk>/delete/', views.team_delete, name='team_delete'),
    path('<int:team_pk>/request/', views.request_join, name='request_join'),
    path('invite/<int:invite_pk>/cancel/', views.cancel_invite, name='cancel_invite'),
]
