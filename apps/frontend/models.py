from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class VisitLog(models.Model):
    ip = models.GenericIPAddressField()
    path = models.CharField(max_length=500)
    user_agent = models.TextField()
    is_bot = models.BooleanField(default=False)
    browser = models.CharField(max_length=100)
    os = models.CharField(max_length=100)
    device = models.CharField(max_length=100)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip} @ {self.timestamp} -> {self.path}"


class UserInfo(AbstractUser):

    mobile = models.CharField(max_length=11, null=True, blank=True)
    addr = models.CharField(max_length=128, null=True, blank=True)
    avatar = models.FileField(
        upload_to="avatars/%Y%m%d/", default="avatars/default.png", verbose_name="头像")
    # 个人简介
    bio = models.TextField(max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = "【全站用户管理】"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def get_full_name(self):
        if self.first_name and self.last_name:
            return self.first_name + self.last_name
        return self.username


class PageVisitCount(models.Model):
    page_url = models.CharField(max_length=255, unique=True)
    visit_count = models.PositiveIntegerField(default=0)
    last_visit = models.DateTimeField(auto_now=True)
    last_ip = models.GenericIPAddressField(null=True, blank=True)
    last_visit_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "页面访问计数"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.page_url}: {self.visit_count} visits"

    def should_increment_count(self, ip):
        """检查是否应该增加访问计数"""
        if not self.last_visit_time:
            return True
        
        # 如果是本地测试IP，不增加计数
        if ip in ['127.0.0.1', 'localhost', '::1']:
            return False
            
        # 如果同一IP在5分钟内重复访问，不增加计数
        time_diff = timezone.now() - self.last_visit_time
        if time_diff.total_seconds() < 300 and ip == self.last_ip:  # 5分钟 = 300秒
            return False
            
        return True
