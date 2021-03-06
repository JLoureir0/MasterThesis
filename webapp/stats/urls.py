from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_stats, name='stats-home'),
    path('<database>/', views.database_stats, name='stats-database'),
    path('<database>/<collection>', views.collection_stats, name='stats-collection'),
    path('<database>/<collection>/<attribute>', views.attribute_stats, name='stats-attribute'),
    path('about/', views.about, name='stats-about')
]
