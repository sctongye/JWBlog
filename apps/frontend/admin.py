from django.contrib import admin, auth
import django.contrib.auth.models
from .models import VisitLog, UserInfo, PageVisitCount


@admin.register(VisitLog)
class VisitLogAdmin(admin.ModelAdmin):
    list_display = ('ip', 'path', 'is_bot', 'browser', 'os',
                    'device', 'country', 'city', 'timestamp')
    list_filter = ('is_bot', 'browser', 'os', 'country', 'timestamp')
    search_fields = ('ip', 'path', 'user_agent', 'country', 'city')
    ordering = ('-timestamp',)


@admin.register(PageVisitCount)
class PageVisitCountAdmin(admin.ModelAdmin):
    list_display = ('page_url', 'visit_count', 'last_visit',
                    'last_ip', 'last_visit_time')
    list_filter = ('last_visit',)
    search_fields = ('page_url', 'last_ip')
    ordering = ('-visit_count',)


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ("username", "mobile", "addr", "avatar", "bio")


admin.site.register(UserInfo, UserInfoAdmin)
