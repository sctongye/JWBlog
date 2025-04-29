from django.urls import path
from . import views

app_name = 'frontend'

urlpatterns = [
    path('', views.index, name='index'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('visit-count/<str:page_url>/', views.get_visit_count, name='visit-count'),
]
