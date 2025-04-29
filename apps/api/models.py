from django.db import models


__all__ = ["UserInfo"]


class UserInfo(models.Model):
    user = models.CharField(max_length=32)
    pwd = models.CharField(max_length=64)
    proj = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        verbose_name = "Auth用户验证UserInfo(非默认用户管理)"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.proj or '无项目'} - {self.user}"


class UserToken(models.Model):
    user = models.OneToOneField(to="UserInfo", on_delete=models.CASCADE)
    token = models.CharField(max_length=64)

    class Meta:
        verbose_name = "Auth用户验证Token"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.user)
