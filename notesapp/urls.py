from django.urls import path, re_path
from notesapp import views

app_name = 'notesapp'

urlpatterns = [
    path(r'user', views.user, name='user'),
    path(r'auth', views.auth, name='auth'),
    re_path(r'sites/list/(?P<user_id>\d+)', views.listnotes, name='listnotes'),
    re_path(r'sites/(?P<user_id>\d+)', views.sites, name='sites'),
]
