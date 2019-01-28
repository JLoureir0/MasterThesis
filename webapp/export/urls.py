from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_export, name='export-home'),
    path('<database>/', views.database_export, name='export-database'),
]
