from django.urls import path
from article import views

app_name = 'article'

urlpatterns = [
    path('upload_image/', views.upload_image, name='upload_image'),
    path('upload_image', views.upload_image, name='upload_image_no_slash'),
]
