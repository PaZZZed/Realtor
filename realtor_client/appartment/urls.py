from django.urls import path
from . import views

app_name = 'appartment'
urlpatterns = [
    path('<int:appart_id>', views.create, name='create'),
    path('', views.apartAll, name='index'),
]
