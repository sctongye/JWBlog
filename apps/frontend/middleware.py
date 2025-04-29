import geoip2.database
import user_agents
from django.utils.deprecation import MiddlewareMixin
from .models import VisitLog
import os
from django.conf import settings

EXCLUDED_IPS = {'127.0.0.1', '71.142.126.4'}
GEOIP_PATH = os.path.join(settings.BASE_DIR, 'geo', 'GeoLite2-City.mmdb')
GEO_READER = geoip2.database.Reader(GEOIP_PATH)


def is_local_network(ip):
    return ip.startswith('192.168.') or ip.startswith('10.') or ip.startswith('172.')


def get_client_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        ip = x_forwarded.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class VisitorLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip = get_client_ip(request)

        if (
            ip in EXCLUDED_IPS
            or is_local_network(ip)
            or request.path.startswith('/admin/')
            or getattr(request.user, 'is_staff', False)
        ):
            return

        ua_string = request.META.get('HTTP_USER_AGENT', '')
        ua = user_agents.parse(ua_string)

        country = city = None
        try:
            geo_data = GEO_READER.city(ip)
            country = geo_data.country.name
            city = geo_data.city.name
        except:
            pass

        VisitLog.objects.create(
            ip=ip,
            path=request.path,
            user_agent=ua_string,
            is_bot=ua.is_bot,
            browser=f"{ua.browser.family} {ua.browser.version_string}",
            os=f"{ua.os.family} {ua.os.version_string}",
            device=ua.device.family,
            country=country,
            city=city,
        )


class PageVisitCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # 只统计成功的页面访问
        if response.status_code == 200 and not request.path.startswith('/static/') and not request.path.startswith('/media/'):
            # 关键：将首页和 /blog/ 显式区分
            if request.path == '/':
                page_key = '__home__'
            elif request.path.startswith('/blog'):
                page_key = '__blog__'
            else:
                page_key = request.path

            from .models import PageVisitCount
            from django.db.models import F

            PageVisitCount.objects.get_or_create(
                page_url=page_key,
                defaults={'visit_count': 1}
            )[0].save()
            PageVisitCount.objects.filter(page_url=page_key).update(
                visit_count=F('visit_count') + 1
            )
        return response
