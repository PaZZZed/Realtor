from django.urls import path
from . import views
from .views import IndexView

app_name = 'connection_config'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login', views.login_new, name='login'),
    path('logout', views.logout_view, name='logout'),
]
