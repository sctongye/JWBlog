"""
URL configuration for django_main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django_main.settings import MEDIA_ROOT
from rest_framework.routers import DefaultRouter
from frontend.views import LoginView, RegisterView, Profile_edit, LogoutView, get_visit_count
from frontend.proj_views import RefereeRecordsView, update_ref_data
from article.views import ArticleViewSet, CategoryViewSet, TagViewSet, AvatarViewSet
from article.userviews import UserViewSet
from comment.views import CommentViewSet
from django.conf import settings
from django.conf.urls.static import static

try:
    from django_main.settings import STATIC_ROOT
except:
    from django_main.settings import STATICFILES_DIRS
    STATIC_ROOT = STATICFILES_DIRS[0]

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'article', ArticleViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'tag', TagViewSet)
router.register(r'avatar', AvatarViewSet)
router.register(r'comment', CommentViewSet)


urlpatterns = [
    path('admin/', admin.site.urls, name="djangoadmin"),
    path('api/visit-count/article/<str:page_url>/', get_visit_count, name='article-visit-count'),
    path('api/visit-count/home/', get_visit_count, name='home-visit-count'),
    path('api/', include(router.urls)),
    path('api/article/', include('article.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include('frontend.urls', namespace='frontend')),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
    path('edit/<int:id>/', Profile_edit.as_view(), name='edit'),
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),
    re_path(r'^api/(?P<version>\w+)/', include('api.urls')),
    path('rr/', RefereeRecordsView.as_view(), name="referee_records"),
    path('update-ref-data/', update_ref_data, name='update_ref_data'),
]

# # 在开发环境下，将所有未匹配的 URL 重定向到前端开发服务器
# if settings.DEBUG:
#     urlpatterns += [
#         re_path(r'^blog/.*$', TemplateView.as_view(template_name='index.html')),
#         re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
#     ]

handler404 = 'frontend.views.custom_404'
# 把媒体文件的路由注册了
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
