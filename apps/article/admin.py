from django.contrib import admin
from .models import Article, Category

# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'created', 'updated')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
