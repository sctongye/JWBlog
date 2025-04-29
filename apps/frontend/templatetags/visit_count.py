from django import template
from ..models import PageVisitCount
from django.utils import timezone

register = template.Library()


@register.simple_tag(takes_context=True)
def get_visit_count(context):
    request = context['request']
    ip = request.META.get('REMOTE_ADDR')

    # 关键：区分首页和 /blog/ 计数
    path = request.path
    if path == '/':
        page_key = '__home__'
    elif path.startswith('/blog'):
        page_key = '__blog__'
    else:
        page_key = path

    try:
        count_obj = PageVisitCount.objects.get(page_url=page_key)

        # 检查是否应该增加计数
        if count_obj.should_increment_count(ip):
            count_obj.visit_count += 1
            count_obj.last_ip = ip
            count_obj.last_visit_time = timezone.now()
            count_obj.save()

        return count_obj.visit_count
    except PageVisitCount.DoesNotExist:
        # 创建新的计数记录
        count_obj = PageVisitCount.objects.create(
            page_url=page_key,
            visit_count=1,
            last_ip=ip,
            last_visit_time=timezone.now()
        )
        return 1
