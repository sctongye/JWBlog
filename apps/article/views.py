# -*- coding: utf-8 -*-
from .models import Article, Category, Tag, Avatar
from rest_framework import viewsets
from .serializers import ArticleSerializer, CategorySerializer, CategoryDetailSerializer, TagSerializer, ArticleDetailSerializer, AvatarSerializer
from .permissions import IsAdminUserOrReadOnly
from rest_framework import filters
from frontend.models import PageVisitCount
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import uuid
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count


@api_view(['GET'])
def get_visit_count(request, page_url):
    try:
        count_obj = PageVisitCount.objects.get(page_url=page_url)
        return Response({'count': count_obj.visit_count})
    except PageVisitCount.DoesNotExist:
        return Response({'count': 0})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_image(request):
    print(f"Request method: {request.method}")
    print(f"Request headers: {request.headers}")
    print(f"Request body: {request.body}")
    print(f"Request FILES: {request.FILES}")
    print(f"Request path: {request.path}")
    print(f"Request META: {request.META}")
    
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            image_file = request.FILES['image']
            # 生成唯一的文件名
            ext = os.path.splitext(image_file.name)[1]
            filename = f"{uuid.uuid4()}{ext}"
            
            # 确保上传目录存在
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            
            # 保存文件
            path = default_storage.save(f'uploads/{filename}', ContentFile(image_file.read()))
            # 获取文件的URL，强制使用 www 域名
            url = request.build_absolute_uri(default_storage.url(path))
            url = url.replace('http://wangjiayu.com', 'http://www.wangjiayu.com')
            print(f"File saved at: {path}")
            print(f"File URL: {url}")
            return Response({'url': url})
        except Exception as e:
            print(f"Error uploading image: {str(e)}")
            return Response({'error': str(e)}, status=500)
    return Response({'error': 'No image file provided'}, status=400)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'body']

    def perform_create(self, serializer):
        article = serializer.save()
        # 创建文章时同时创建访问计数记录
        article_url = f"/article/{article.id}/"
        PageVisitCount.objects.create(
            page_url=article_url,
            visit_count=0  # 初始访问量为0
        )
        return article

    def get_queryset(self):
        queryset = self.queryset
        username = self.request.query_params.get('username', None)
        tag = self.request.query_params.get('tag', None)
        category = self.request.query_params.get('category', None)

        if username is not None:
            queryset = queryset.filter(author__username=username)
        
        if tag is not None:
            queryset = queryset.filter(tags__text=tag)
            
        if category is not None:
            queryset = queryset.filter(category_id=category)

        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleSerializer
        else:
            return ArticleDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        # 获取文章详情时增加访问计数
        instance = self.get_object()
        ip = request.META.get('REMOTE_ADDR')
        
        # 构建文章页面的URL
        article_url = f"/article/{instance.id}/"
        
        try:
            count_obj = PageVisitCount.objects.get(page_url=article_url)
            if count_obj.should_increment_count(ip):
                count_obj.visit_count += 1
                count_obj.last_ip = ip
                count_obj.last_visit_time = timezone.now()
                count_obj.save()
        except PageVisitCount.DoesNotExist:
            PageVisitCount.objects.create(
                page_url=article_url,
                visit_count=1,
                last_ip=ip,
                last_visit_time=timezone.now()
            )
            
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    """分类视图集"""
    queryset = Category.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = None

    def get_queryset(self):
        # 只返回至少有一篇文章的分类，并包含文章计数
        return Category.objects.annotate(
            count=Count('articles')
        ).filter(count__gt=0)

    def get_serializer_class(self):
        if self.action == 'list':
            return CategorySerializer
        else:
            return CategoryDetailSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = None
    serializer_class = TagSerializer

    def get_queryset(self):
        # 只返回至少有一篇文章使用的标签，并包含文章计数
        return Tag.objects.annotate(
            count=Count('articles')
        ).filter(count__gt=0)


class AvatarViewSet(viewsets.ModelViewSet):
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer
    permission_classes = [IsAdminUserOrReadOnly]


# class ArticleList(generics.ListCreateAPIView):
#     queryset = Article.objects.all()
#     serializer_class = ArticleListSerializer
#     permission_classes = [IsAdminUserOrReadOnly]

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)


# class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Article.objects.all()
#     serializer_class = ArticleDetailSerializer
#     permission_classes = [IsAdminUserOrReadOnly]
